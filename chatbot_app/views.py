from rest_framework import viewsets
from django.http import JsonResponse
from .models import Cliente, Consulta, Tema, HistorialInteraccion, Usuario, Rol
from .serializers import (
    ClienteSerializer, ConsultaSerializer, TemaSerializer, HistorialInteraccionSerializer,
    UsuarioSerializer, RolSerializer
)
from .chatbot_logica import iniciar_conversacion, procesar_mensaje_usuario
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TemaForm
from django.contrib import messages
from datetime import datetime, timedelta
from collections import OrderedDict
import json
from django.db.models import Q  # Para búsquedas avanzadas en filtros
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone
from datetime import time
from django.db.models import Count



# 📌 Vista principal de prueba de API
def home(request):
    """
    Muestra mensaje de bienvenida y lista de endpoints disponibles.
    """
    data = {
        "message": "Bienvenido al API del Chatbot RRHH",
        "endpoints": {
            "clientes": "/api/clientes/",
            "consultas": "/api/consultas/",
            "temas": "/api/temas/",
            "usuarios": "/api/usuarios/",
        }
    }
    return JsonResponse(data)

# 📌 Vista que carga el panel de administración
def panel_admin(request):
    """
    Renderiza la plantilla principal del panel de administración.
    """
    return render(request, 'chatbot_app/template_admin.html')

# 📊 Vista de inicio del panel con métricas de uso
def vista_inicio(request):
    """
    Muestra estadísticas básicas: consultas por día (últimos 7 días), cantidad de consultas hoy,
    y cantidad de temas activos de primer nivel.
    """
    hoy = timezone.localdate()
    fechas = [hoy - timedelta(days=i) for i in range(6, -1, -1)]

    # Datos de consultas por día
    datos = OrderedDict()
    for fecha in fechas:
        inicio = timezone.make_aware(datetime.combine(fecha, time.min))
        fin = timezone.make_aware(datetime.combine(fecha, time.max))
        cantidad = Consulta.objects.filter(fecha_creacion__range=(inicio, fin)).count()
        datos[fecha.strftime('%d/%m')] = cantidad

    # Consultas de hoy con rango horario
    inicio_hoy = timezone.make_aware(datetime.combine(hoy, time.min))
    fin_hoy = timezone.make_aware(datetime.combine(hoy, time.max))
    cantidad_consultas_hoy = Consulta.objects.filter(fecha_creacion__range=(inicio_hoy, fin_hoy)).count()

    # Temas activos de primer nivel
    cantidad_temas = Tema.objects.filter(tema_padre__isnull=True, activo_tema=True).count()

    context = {
        'labels': list(datos.keys()),
        'valores': list(datos.values()),
        'consultas_hoy': cantidad_consultas_hoy,
        'cantidad_temas': cantidad_temas,
    }

    return render(request, 'chatbot_app/inicio.html', context)


# 📂 Vista de consultas con filtros
def vista_consultas(request):
    """
    Lista las últimas consultas y permite filtrarlas por:
    ID, DNI, nombre o apellido de agente, estado, tipo y tema.
    """

    # Recuperar parámetros de búsqueda
    estado_filtro = request.GET.get('estado')
    tipo_filtro = request.GET.get('tipo')
    tema_filtro = request.GET.get('tema')
    id_filtro = request.GET.get('id')
    dni_filtro = request.GET.get('dni')
    agente_filtro = request.GET.get('cliente')

    # Consultas optimizadas con relaciones cargadas
    consultas = Consulta.objects.select_related('cliente', 'tema').order_by('-fecha_creacion')

    # Aplicar filtros
    if estado_filtro:
        consultas = consultas.filter(estado=estado_filtro)

    if tipo_filtro:
        consultas = consultas.filter(tipo=tipo_filtro)

    if tema_filtro:
        consultas = consultas.filter(tema__id_tema=tema_filtro)

    if id_filtro:
        consultas = consultas.filter(id_consulta=id_filtro)

    if dni_filtro:
        consultas = consultas.filter(agente__dni__icontains=dni_filtro)

    if agente_filtro:
        consultas = consultas.filter(
            Q(agente__nombre__icontains=agente_filtro) |
            Q(agente__apellido__icontains=agente_filtro)
        )

    # Contexto para template
    context = {
        'consultas': consultas[:50],  # Solo mostrar las 50 más recientes
        'estados': Consulta.ESTADO_CHOICES,
        'tipos': Consulta.TIPO_CONSULTA_CHOICES,
        'temas': Tema.objects.all(),
        'filtros': {
            'id': id_filtro or '',
            'agente': agente_filtro or '',
            'estado': estado_filtro or '',
            'tipo': tipo_filtro or '',
            'tema': tema_filtro or '',
        }
    }

    return render(request, 'chatbot_app/consultas.html', context)

# 🔍 Función auxiliar para detectar ciclos en jerarquía de temas
def tiene_ciclo(tema):
    """
    Revisa si existe un bucle en la jerarquía de temas.
    """
    visitados = set()
    actual = tema
    while actual:
        if actual.id_tema in visitados:
            return True
        visitados.add(actual.id_tema)
        actual = actual.tema_padre
    return False

# 🌳 Construir árbol jerárquico de temas
def construir_arbol_temas():
    from chatbot_app.models import Tema

    # Recupera todos los temas en un diccionario por ID
    todos = {
        t.id_tema: {
            "id": t.id_tema, 
            "nombre": t.nombre_tema, 
            "subtemas": []
            } 
        for t in Tema.objects.all()
        }
    
    # Relaciona hijos con sus padres
    for tema in Tema.objects.all():
        if tema.tema_padre and tema.tema_padre.id_tema in todos:
            todos[tema.tema_padre.id_tema]["subtemas"].append(todos[tema.id_tema])
    return [t for t in todos.values() if not Tema.objects.get(id_tema=t["id"]).tema_padre]

# 📂 Vista para crear y editar temas
def vista_temas(request):
    """
    Permite crear o editar temas, mostrando árbol jerárquico de temas existentes.
    """
    tema_id = request.POST.get('id_tema') or request.GET.get('tema_id')
    tema_seleccionado = get_object_or_404(Tema, id_tema=tema_id) if tema_id else None

    if request.method == 'POST':
        form = TemaForm(request.POST, instance=tema_seleccionado)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tema modificado correctamente." if tema_seleccionado else "✅ Tema creado exitosamente.")
            return redirect('vista_temas')
        else:
            messages.error(request, "❌ Error al guardar el tema. Verificá los campos.")
    else:
        form = TemaForm(instance=tema_seleccionado)

    temas_jerarquicos = construir_arbol_temas()
    temas_json = json.dumps(temas_jerarquicos)

    return render(request, 'chatbot_app/temas.html', {
        'form': form,
        'tema_seleccionado': tema_seleccionado,
        'temas_json': temas_json,
    })

# ✏️ Editar un tema existente
def editar_tema(request, tema_id):
    """
    Edita un tema existente identificado por su ID.
    """
    tema = get_object_or_404(Tema, id_tema=tema_id)
    if request.method == 'POST':
        form = TemaForm(request.POST, instance=tema)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Tema modificado correctamente.")
            return redirect('vista_temas')
    else:
        form = TemaForm(instance=tema)
    return render(request, 'chatbot_app/editar_tema.html', {'form': form, 'tema': tema})

# 🗑️ Eliminar tema
def eliminar_tema(request, tema_id):
    """
    Elimina un tema por su ID.
    """
    tema = get_object_or_404(Tema, id_tema=tema_id)
    if request.method == "POST":
        tema.delete()
        messages.success(request, "🗑️ Tema eliminado correctamente.")
        return redirect('vista_temas')
    return JsonResponse({"error": "Método no permitido"}, status=405)

# 📄 Obtener datos de un tema
def obtener_tema(request, id_tema):
    """
    Devuelve en JSON los datos de un tema.
    """
    tema = Tema.objects.get(id_tema=id_tema)
    data = {
        "id_tema": tema.id_tema,
        "nombre_tema": tema.nombre_tema,
        "orden": tema.orden,
        "padre": tema.tema_padre.id_tema if tema.tema_padre else None,
        "detalle_respuesta": tema.detalle_respuesta,
        
    }
    return JsonResponse(data)

# 📦 ViewSets para API REST
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer

class TemaViewSet(viewsets.ModelViewSet):
    queryset = Tema.objects.all()
    serializer_class = TemaSerializer

class HistorialInteraccionViewSet(viewsets.ModelViewSet):
    queryset = HistorialInteraccion.objects.all()
    serializer_class = HistorialInteraccionSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer

# 💬 Chatbot webhook (API para procesar mensajes)
ESTADOS = {}
def webhook_chatbot(request):
    """
    API para recibir mensajes del usuario, procesarlos y devolver respuesta.
    """
    usuario_id = request.GET.get('usuario_id', 'anonimo')
    mensaje_usuario = request.GET.get('mensaje', '')

    estado_actual = ESTADOS.get(usuario_id)

    # Si el usuario inicia con "hola", se reinicia la conversación
    if mensaje_usuario.lower().strip() == "hola":
        respuesta, nuevo_estado = iniciar_conversacion(usuario_id)
    elif estado_actual is None:
        respuesta, nuevo_estado = iniciar_conversacion(usuario_id)
    else:
        respuesta, nuevo_estado = procesar_mensaje_usuario(mensaje_usuario, estado_actual, usuario_id)

    ESTADOS[usuario_id] = nuevo_estado

    return JsonResponse({'respuesta': respuesta})