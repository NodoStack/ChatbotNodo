import os
import django
import random

# Configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chatbot.settings")
django.setup()

from chatbot_app.chatbot_logica import iniciar_conversacion, procesar_mensaje_usuario

def generar_numero_simulado():
    return f"+549351{random.randint(1000000, 9999999)}"

def main():
       
    # Simular número de teléfono
    usuario_id = generar_numero_simulado()
    print(f"(Simulando número de teléfono: {usuario_id})")

    # Iniciar conversación
    mensaje, estado = iniciar_conversacion(usuario_id)
    print(mensaje)

    # Ingresar nombre
    nombre = input("Tu nombre: ").strip()
    respuesta, estado = procesar_mensaje_usuario(nombre, estado, usuario_id)
    print(respuesta)

    # Bucle de conversación
    while estado != "finalizado":
        entrada = input("Escribí tu mensaje: ").strip()
        try:
            respuesta, estado = procesar_mensaje_usuario(entrada, estado, usuario_id)
            print(respuesta)
        except KeyError:
            print("⚠️ Se perdió el estado del usuario. El test no pudo continuar.")
            break

if __name__ == "__main__":
    main()