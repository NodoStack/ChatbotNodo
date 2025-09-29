from chatbot_app.logica.core import iniciar_conversacion, procesar_mensaje_usuario





# from .models import Agente, Consulta, Tema
# from django.utils import timezone

# TEMP_DATA = {}
# def iniciar_conversacion(usuario_id=None):
#     """
#     Inicia la conversación, devuelve el mensaje de bienvenida y el estado inicial.
#     Si se pasa un usuario_id, limpia sus datos previos del diccionario TEMP_DATA.
#     """
#     if usuario_id and usuario_id in TEMP_DATA:
#         del TEMP_DATA[usuario_id]

#     mensaje = "¡Hola! Bienvenido al asistente de RRHH. Por favor, ingresá tu número de DNI para comenzar."
#     estado = "esperando_dni"
#     return mensaje, estado


# def procesar_mensaje_usuario(mensaje, estado_actual, usuario_id):
#     mensaje = mensaje.strip().lower()
#     respuesta = ""
#     nuevo_estado = estado_actual

#     # Evitar que se cambie el DNI en medio de una sesión activa
#     if estado_actual not in ["esperando_dni", "finalizado"]:
#         if usuario_id in TEMP_DATA and TEMP_DATA[usuario_id].get("dni"):
#             if mensaje.isdigit() and len(mensaje) >= 7 and mensaje != TEMP_DATA[usuario_id]["dni"]:
#                 agente_nombre = TEMP_DATA[usuario_id]["nombre"]
#                 return (
#                     f"Ya ingresaste el DNI {TEMP_DATA[usuario_id]['dni']} ({agente_nombre}). "
#                     f"Si querés iniciar una nueva consulta, escribí *hola*.\n\n"
#                     "📌 *Temas disponibles:*\n"
#                     "1️⃣ Ausentismo\n"
#                     "2️⃣ Trámites Generales en RR.HH.\n"
#                     "3️⃣ Becarios y Monotributistas\n"
#                     "4️⃣ Liquidación de Haberes\n"
#                     "5️⃣ Contacto con el Ministerio",
#                     estado_actual
#                 )

#     # DNI
#     if estado_actual == "esperando_dni":
#         try:
#             agente = Agente.objects.get(dni=mensaje)
#             consulta = Consulta.objects.create(agente=agente, tipo='consulta', estado='pendiente')

#             TEMP_DATA[usuario_id] = {
#                 "dni": mensaje,
#                 "nombre": agente.nombre,
#                 "apellido": agente.apellido,
#                 "agente_id": agente.id_agente,
#                 "consulta_id": consulta.id_consulta
#             }

#             respuesta = (
#                 f"Hola {agente.nombre}, ¿en qué puedo ayudarte hoy?\n\n"
#                 "📌 *Temas disponibles:*\n"
#                 "1️⃣ Ausentismo\n"
#                 "2️⃣ Trámites Generales en RR.HH.\n"
#                 "3️⃣ Becarios y Monotributistas\n"
#                 "4️⃣ Liquidación de Haberes\n"
#                 "5️⃣ Contacto con el Ministerio"
#             )
#             nuevo_estado = "menu_principal"

#         except Agente.DoesNotExist:
#             respuesta = "❌ El DNI ingresado no está registrado. Por favor, verificalo e intentá nuevamente."
#             nuevo_estado = "esperando_dni"

#     elif estado_actual == "menu_principal":
#         if mensaje == "1":
#             respuesta = (
#                 "📝 *AUSENTISMO*\n"
#                 "Indicá el número correspondiente al edificio donde prestás funciones:\n\n"
#                 "1️⃣ Edificio Alvear N°15\n"
#                 "2️⃣ Vélez Sarsfield N°771\n"
#                 "3️⃣ Tránsito Cáceres de Allende\n"
#                 "4️⃣ Área 52\n"
#                 "5️⃣ Complejo Esperanza\n"
#                 "6️⃣ Residencias y Casas de Capital\n"
#                 "7️⃣ Residencias del Interior y UDER\n"
#                 "8️⃣ Salas Cuna, CIPEM y Personas Mayores\n"
#                 "9️⃣ Sitios de la Memoria"
#             )
#             nuevo_estado = "ausentismo_edificio"

#         elif mensaje == "2":
#             respuesta = (
#                 "📂 *TRÁMITES GENERALES*\n"
#                 "Seleccioná una opción:\n"
#                 "1️⃣ Tengo un trámite iniciado\n"
#                 "2️⃣ Necesito iniciar un trámite"
#             )
#             nuevo_estado = "tramites_generales"

#         elif mensaje == "3":
#             respuesta = (
#                 "✅ Gracias por tu consulta sobre *Becarios y Monotributistas*.\n"
#                 "⏳ Estamos esperando instrucciones de RRHH para darte una respuesta más específica.\n"
#                 "📬 Mientras tanto, podés escribir a rrhhdesarrollohumano@cba.gov.ar si necesitás atención urgente."
#             )
#             nuevo_estado = "finalizado"

#         elif mensaje == "4":
#             nombre_tramite = "Liquidación de Haberes"
#             try:
#                 tema_obj = Tema.objects.filter(nombre_tema=nombre_tramite).first()
#                 consulta_id = TEMP_DATA[usuario_id].get("consulta_id")
#                 consulta = Consulta.objects.get(id_consulta=consulta_id)

#                 if tema_obj:
#                     consulta.tema = tema_obj
#                     if tema_obj.detalle_respuesta:
#                         consulta.estado = "resuelto"
#                         respuesta = tema_obj.detalle_respuesta
#                     else:
#                         consulta.estado = "pendiente"
#                         respuesta = (
#                             f"📌 Para consultas sobre sueldos, comunicate al 351-2273999."

#                         )
#                     consulta.save()
#                 else:
#                     respuesta = "❌ No se encontró el tema 'Liquidación de Haberes' en la base de datos."

#             except Consulta.DoesNotExist:
#                 respuesta = "❌ No se encontró la consulta activa del usuario."

#             nuevo_estado = "finalizado"

#         elif mensaje == "5":
#             respuesta = (
#                 "📞 Para comunicarte con el Ministerio, podés llamar al 4340-0000.\n"
#                 "📬 También podés escribir a rrhhdesarrollohumano@cba.gov.ar"
#             )
#             nuevo_estado = "finalizado"

#         else:
#             respuesta = (
#                 "⚠️ Opción no válida. Por favor seleccioná un número del 1 al 5.\n\n"
#                 "📌 *Temas disponibles:*\n"
#                 "1️⃣ Ausentismo\n"
#                 "2️⃣ Trámites Generales en RR.HH.\n"
#                 "3️⃣ Becarios y Monotributistas\n"
#                 "4️⃣ Liquidación de Haberes\n"
#                 "5️⃣ Contacto con el Ministerio"
#             )
#             nuevo_estado = "menu_principal"

#     elif estado_actual == "ausentismo_edificio":
#         opciones = {
#             "1": "📌 1️⃣ SeNAF: Iniciá tu consulta\n📌 2️⃣ Personas Mayores: Iniciá tu consulta\n📌 3️⃣ Coordinación Familiar: Comunicate al 4342415\n📌 4️⃣ Derechos Humanos: Comunicate al 4342415\n📌 5️⃣ Resto de Áreas: Comunicate al 4342415",
#             "2": "📌 Comunicate al 4340000",
#             "3": "📌 Comunicate al 4342415",
#             "4": "📌 Iniciá tu consulta",
#             "5": "📌 Comunicate al 351-3758159",
#             "6": "📌 Comunicate al 4340000",
#             "7": "📌 Iniciá tu consulta",
#             "8": "📌 Iniciá tu consulta",
#             "9": "📌 Comunicate al 4342415"
#         }
#         respuesta = opciones.get(mensaje, "❌ Opción no válida. Ingresá un número del 1 al 9.")
#         if mensaje in opciones:
#             nuevo_estado = "finalizado"

#     elif estado_actual == "tramites_generales":
#         if mensaje == "1":
#             respuesta = "🔎 Ingresá el número de trámite (15 dígitos o formato 0412-009815/2024)."
#             nuevo_estado = "esperando_num_tramite"
#         elif mensaje == "2":
#             respuesta = (
#                 "📋 *Seleccioná el tipo de trámite que querés iniciar:*\n"
#                 "1️⃣ Pago de Título\n"
#                 "2️⃣ Cambio de Agrupamiento\n"
#                 "3️⃣ Jubilaciones/Renuncias\n"
#                 "4️⃣ Licencias sin goce\n"
#                 "5️⃣ Fallecimiento\n"
#                 "6️⃣ Otros trámites\n"
#                 "7️⃣ Descargo por Ausentismo\n"
#                 "8️⃣ Oficios Judiciales"
#             )
#             nuevo_estado = "tramite_nuevo_opcion"
#         else:
#             respuesta = "❌ Opción no válida. Elegí 1️⃣ o 2️⃣."
#             nuevo_estado = "tramites_generales"

#     elif estado_actual == "esperando_num_tramite":
#         if mensaje.replace("-", "").replace("/", "").isdigit():
#             respuesta = (
#                 "✅ Gracias. Iniciá tu consulta o esperá respuesta por email "
#                 "si ya escribiste a rrhhdesarrollohumano@cba.gov.ar"
#             )
#             nuevo_estado = "finalizado"
#         else:
#             respuesta = "❌ Número de trámite no válido. Verificá e ingresalo nuevamente."

#     elif estado_actual == "tramite_nuevo_opcion":
#         respuestas_pendientes = {
#             "1": "Pago de Título",
#             "2": "Cambio de Agrupamiento",
#             "3": "Jubilaciones/Renuncias",
#             "5": "Fallecimiento",
#             "6": "Otros trámites",
#             "7": "Descargo por Ausentismo",
#             "8": "Oficios Judiciales"
#         }

#         if mensaje in respuestas_pendientes:
#             nombre_tramite = respuestas_pendientes[mensaje]
#             consulta_id = TEMP_DATA[usuario_id].get("consulta_id")

#             try:
#                 consulta = Consulta.objects.get(id_consulta=consulta_id)
#                 tema_obj = Tema.objects.filter(nombre_tema=nombre_tramite).first()

#                 if tema_obj:
#                     consulta.tema = tema_obj

#                     if tema_obj.detalle_respuesta:
#                         consulta.estado = 'resuelto'
#                         respuesta = tema_obj.detalle_respuesta
#                     else:
#                         consulta.estado = 'pendiente'
#                         respuesta = (
#                             f"✅ Gracias por tu consulta sobre *{nombre_tramite}*.\n"
#                             "⏳ Estamos esperando instrucciones de RRHH para darte una respuesta más específica.\n"
#                             "📬 Mientras tanto, podés escribir a rrhhdesarrollohumano@cba.gov.ar si necesitás atención urgente."
#                         )

#                     consulta.save()
#                 else:
#                     respuesta = "❌ Hubo un error al registrar el tema. Por favor intentá nuevamente."

#             except Consulta.DoesNotExist:
#                 respuesta = "❌ No se encontró la consulta activa."

#             nuevo_estado = "finalizado"

#         else:
#             respuesta = "❌ Opción no válida. Por favor seleccioná una opción válida."
#             nuevo_estado = "tramite_nuevo_opcion"

#     else:
#         respuesta = "❌ Opción no válida. Por favor seleccioná una opción válida."
#         nuevo_estado = estado_actual

#     return respuesta, nuevo_estado
