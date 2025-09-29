
from chatbot_app.models import Tema, Consulta
from chatbot_app.logica.flujos.respuestas import responder_por_tema
from chatbot_app.logica.flujos.temas_dinamicos import generar_menu_temas, obtener_temas_activos

def manejar_menu(mensaje, usuario_id, temp_data):
    if mensaje == "0":
        tema_padre_id = temp_data[usuario_id].get("tema_padre_id")
        if tema_padre_id:
            tema_padre = Tema.objects.get(id_tema=tema_padre_id).tema_padre
            nuevo_padre_id = tema_padre.id_tema if tema_padre else None

            menu_texto, nuevos_temas = generar_menu_temas(nuevo_padre_id)
            temp_data[usuario_id]["nivel_temas"] = nuevos_temas
            temp_data[usuario_id]["tema_padre_id"] = nuevo_padre_id

            return f"🔙 Volviste al menú anterior:\n\n📌 *Temas disponibles:*\n{menu_texto}", "menu_principal"

    temas_actuales = temp_data[usuario_id].get("nivel_temas", [])
    try:
        indice = int(mensaje) - 1
        tema_seleccionado = temas_actuales[indice]
    except (ValueError, IndexError):
        menu_texto, _ = generar_menu_temas(temp_data[usuario_id].get("tema_padre_id"))
        return f"❌ Opción no válida. Por favor seleccioná un número válido.\n\n📌 *Temas disponibles:*\n{menu_texto}", "menu_principal"

    subtemas = obtener_temas_activos(tema_seleccionado.id_tema)
    if subtemas:
        menu_texto, nuevos_temas = generar_menu_temas(tema_seleccionado.id_tema)
        temp_data[usuario_id]["nivel_temas"] = nuevos_temas
        temp_data[usuario_id]["tema_padre_id"] = tema_seleccionado.id_tema
        return f"📂 *Subtemas de {tema_seleccionado.nombre_tema}:*\n{menu_texto}", "menu_principal"

    
    # 📝 Crear consulta ahora que tenemos el tema final
    agente_id = temp_data[usuario_id]["agente_id"]
    consulta = Consulta.objects.create(
        agente_id=agente_id,
        tipo="consulta",
        estado="pendiente",
        tema_id=tema_seleccionado.id_tema
    )
    temp_data[usuario_id]["consulta_id"] = consulta.id_consulta

    respuesta = responder_por_tema(consulta, tema_seleccionado)
    return respuesta, "finalizado"
