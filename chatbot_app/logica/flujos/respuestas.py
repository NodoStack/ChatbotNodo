# Centralizar la lógica que decide si una consulta se marca como resuelta
# o pendiente según el contenido del tema.

def responder_por_tema(consulta, tema):
    consulta.tema = tema

    requiere_referencia = tema.requiere_referencia
    referencia_valida = consulta.referencia_informada

    if requiere_referencia and not referencia_valida:
        consulta.estado = "pendiente"
        respuesta = (
            f"⚠️ El tema *{tema.nombre_tema}* requiere número de trámite.\n"
            "Por favor, ingresalo para que podamos procesar tu consulta correctamente."
        )
    elif tema.detalle_respuesta and tema.detalle_respuesta.strip():
        consulta.estado = "resuelto"
        respuesta = tema.detalle_respuesta
    else:
        consulta.estado = "pendiente"
        respuesta = (
            f"✅ Gracias por tu consulta sobre *{tema.nombre_tema}*.\n"
            "⏳ Estamos esperando instrucciones de RRHH para darte una respuesta más específica.\n"
            "📬 Mientras tanto, podés escribir a rrhhdesarrollohumano@cba.gov.ar si necesitás atención urgente."
        )

    consulta.save()
    return respuesta