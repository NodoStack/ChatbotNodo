"""
📂 estado.py

Este archivo contiene el diccionario global TEMP_DATA, que se utiliza para almacenar
el estado temporal de cada usuario durante una conversación con el bot.

Se usa para guardar:
- El nivel actual de temas que se están mostrando
- El tema padre en navegación jerárquica
- El ID de la consulta activa
- Cualquier otro dato temporal necesario para el flujo

Este archivo es independiente para evitar importaciones circulares.
"""

TEMP_DATA = {}