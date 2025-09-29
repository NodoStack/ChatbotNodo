from chatbot_app.logica.flujos.menu import manejar_menu
from chatbot_app.models import Cliente, Consulta
from django.utils import timezone
from chatbot_app.logica.flujos.temas_dinamicos import generar_menu_temas
from chatbot_app.logica.flujos.estado import TEMP_DATA

def iniciar_conversacion(usuario_id=None):
    if usuario_id and usuario_id in TEMP_DATA:
        del TEMP_DATA[usuario_id]

    mensaje = "¡Hola! Bienvenido a NodoStack 👋. ¿Cuál es tu nombre?"
    estado = "esperando_nombre"
    return mensaje, estado

def procesar_mensaje_usuario(mensaje, estado_actual, usuario_id):
    mensaje = mensaje.strip()
    respuesta = ""
    estado_actual = TEMP_DATA.get(usuario_id, {}).get("estado", estado_actual)
    nuevo_estado = estado_actual

    if estado_actual == "esperando_nombre":
        if not mensaje.replace(" ", "").isalpha():
            return "Por favor ingresá un nombre válido 🙏", "esperando_nombre"

        TEMP_DATA.setdefault(usuario_id, {})
        TEMP_DATA[usuario_id]["nombre"] = mensaje
        TEMP_DATA[usuario_id]["telefono"] = usuario_id  # Simulado

        cliente, creado = Cliente.objects.get_or_create(
            tel=usuario_id,
            defaults={"nombre": mensaje, "apellido": "", "correo": ""}
        )

        consulta = Consulta.objects.create(
            cliente=cliente,
            estado="pendiente",
            observaciones_usuario="Inicio de conversación desde NodoBot",
            fecha_creacion=timezone.now()
        )
        TEMP_DATA[usuario_id]["consulta_id"] = consulta.id_consulta

        respuesta = (
            f"¡Bienvenido/a {mensaje} 🙌! ¿En qué podemos ayudarte?\n\n"
            "1️⃣ Conocer nuestros servicios\n"
            "2️⃣ Contactar con alguien del equipo"
        )
        nuevo_estado = "menu_principal"

    elif estado_actual == "menu_principal":
        if mensaje == "1":
            tema_padre_id = 1  # ID del tema "Conocer nuestros servicios"
            texto_menu, temas = generar_menu_temas(tema_padre_id)
            TEMP_DATA[usuario_id]["servicios_disponibles"] = temas
            TEMP_DATA[usuario_id]["tema_padre_id"] = tema_padre_id

            respuesta = (
                f"📂 Subtemas de Conocer nuestros servicios:\n{texto_menu}\n\n"
                "Podés responder con los números de los servicios que te interesan (por ejemplo: 1,3 o 1,2,3)"
            )
            nuevo_estado = "servicios_seleccionados"

        elif mensaje == "2":
            respuesta = (
                "¿Preferís que te contactemos por...?\n📧 Mail\n📱 WhatsApp"
            )
            nuevo_estado = "contacto"

        else:
            respuesta = (
                "❌ Opción no válida. Por favor seleccioná una opción:\n"
                "1️⃣ Conocer nuestros servicios\n"
                "2️⃣ Contactar con alguien del equipo"
            )
            nuevo_estado = "menu_principal"

    elif estado_actual == "servicios_seleccionados":
        seleccion = mensaje.replace(" ", "").split(",")
        temas_disponibles = TEMP_DATA[usuario_id].get("servicios_disponibles", [])
        seleccionados = []

        try:
            for indice in seleccion:
                i = int(indice) - 1
                if i < 0 or i >= len(temas_disponibles):
                    raise ValueError
                seleccionados.append(temas_disponibles[i])
        except ValueError:
            texto_menu, _ = generar_menu_temas(TEMP_DATA[usuario_id].get("tema_padre_id"))
            return (
                f"❌ Opción no válida. Por favor seleccioná números válidos.\n\n"
                f"📌 Servicios disponibles:\n{texto_menu}",
                "servicios_seleccionados"
            )

        nombres_servicios = [t.nombre_tema for t in seleccionados]
        TEMP_DATA[usuario_id]["servicios_elegidos"] = nombres_servicios

        # Guardar el primer tema como tema principal de la consulta
        if seleccionados:
            tema_principal = seleccionados[0]
            consulta_id = TEMP_DATA[usuario_id].get("consulta_id")
            consulta = Consulta.objects.filter(id_consulta=consulta_id).first()
            if consulta:
                consulta.tema = tema_principal
                consulta.save()

        respuesta = (
            f"Perfecto 🙌. Registramos tu interés en: {', '.join(nombres_servicios)}.\n\n"
            "¿Querés solicitar un presupuesto?\n✅ Sí\n❌ No"
        )
        nuevo_estado = "presupuesto_confirmacion"

    elif estado_actual == "presupuesto_confirmacion":
        if mensaje.lower() in ["sí", "si", "✅"]:
            respuesta = "Contanos brevemente de qué trata tu proyecto 📝"
            nuevo_estado = "solicitar_presupuesto_descripcion"
        elif mensaje.lower() in ["no", "❌"]:
            respuesta = "No hay problema 😊. Si querés explorar más sobre lo que hacemos, visitá nodostack.netlify.app o escribinos cuando lo necesites."
            nuevo_estado = "finalizado"
        else:
            respuesta = "Por favor respondé con ✅ Sí o ❌ No."
            nuevo_estado = "presupuesto_confirmacion"

    elif estado_actual == "solicitar_presupuesto_descripcion":
        TEMP_DATA[usuario_id]["descripcion_proyecto"] = mensaje
        respuesta = "Perfecto. Ahora dejanos tu correo electrónico 📧"
        nuevo_estado = "solicitar_presupuesto_correo"

    elif estado_actual == "solicitar_presupuesto_correo":
        TEMP_DATA[usuario_id]["correo"] = mensaje

        cliente = Cliente.objects.filter(tel=usuario_id).first()
        if cliente:
            cliente.correo = mensaje
            cliente.save()

        consulta_id = TEMP_DATA[usuario_id].get("consulta_id")
        consulta = Consulta.objects.filter(id_consulta=consulta_id).first()

        servicios = TEMP_DATA[usuario_id].get("servicios_elegidos", [])
        descripcion = TEMP_DATA[usuario_id].get("descripcion_proyecto", "")
        observaciones = descripcion #esto guarda la descripcion del proyecto que ingresa el cliente

        if consulta:
            consulta.observaciones_usuario = observaciones
            consulta.save()

        respuesta = "¡Gracias por compartir tu proyecto! Nuestro equipo te va a contactar pronto con una propuesta 💼"
        nuevo_estado = "finalizado"

    elif estado_actual == "contacto":
        if mensaje.lower() in ["mail", "📧"]:
            respuesta = "Dejanos tu correo y te escribimos en menos de 24 hs."
            nuevo_estado = "contacto_mail"
        elif mensaje.lower() in ["whatsapp", "📱"]:
            respuesta = "Perfecto. ¿Podés dejarnos tu número de WhatsApp?"
            nuevo_estado = "contacto_whatsapp"
        else:
            respuesta = "Por favor elegí 📧 Mail o 📱 WhatsApp."
            nuevo_estado = "contacto"

    elif estado_actual == "contacto_mail":
        cliente = Cliente.objects.filter(tel=usuario_id).first()
        if cliente:
            cliente.correo = mensaje
            cliente.save()

        respuesta = "¡Gracias! Te escribiremos por mail en menos de 24 hs 📬"
        nuevo_estado = "finalizado"

    elif estado_actual == "contacto_whatsapp":
        cliente = Cliente.objects.filter(tel=usuario_id).first()
        if cliente:
            cliente.tel = mensaje
            cliente.save()

        respuesta = "¡Perfecto! Te vamos a contactar por WhatsApp en breve 📱"
        nuevo_estado = "finalizado"

    else:
        respuesta = (
            "❌ Opción no válida. Por favor seleccioná una opción:\n"
            "1️⃣ Conocer nuestros servicios\n"
            "2️⃣ Contactar con alguien del equipo"
        )
        nuevo_estado = "menu_principal"

    TEMP_DATA.setdefault(usuario_id, {})
    TEMP_DATA[usuario_id]["estado"] = nuevo_estado
    return respuesta, nuevo_estado