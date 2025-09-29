# cDevuelve los temas activos desde la base de datos, filtrando por jerarquía 
# si se indica un padre. Generar_menu_temas, genera el texto del menú para mostrar
#al usuario y devuelve tambien la lista de temas para que el bot sepa como interpretarlos.

from chatbot_app.models import Tema

def obtener_temas_activos(tema_padre_id=None):
    if tema_padre_id:
        return Tema.objects.filter(tema_padre_id=tema_padre_id, activo_tema=True).order_by("orden")
    return Tema.objects.filter(tema_padre__isnull=True, activo_tema=True).order_by("orden")

def generar_menu_temas(tema_padre_id=None):
    temas = obtener_temas_activos(tema_padre_id)
    
    # 🧮 Construye el menú con emojis numerados:
    texto = "\n".join([f"{i+1}️⃣ {t.nombre_tema}" for i, t in enumerate(temas)])
    
    # 🔙 Si estamos en un subnivel, agregamos opción para volver atrás:
    if tema_padre_id is not None:
      texto += f"\n🔙 0️⃣ Volver al menú anterior"

    return texto, list(temas)