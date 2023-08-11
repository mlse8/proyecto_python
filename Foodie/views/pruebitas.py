"""import json

# Cargar los datos de los JSON
with open("../data/eventos.json", "r") as file:
    destinos_data = json.load(file)

with open("../data/destinos.json", "r") as file:
    imagenes_data = json.load(file)

# Crear un diccionario para almacenar las rutas de las imágenes por nombre de destino
rutas_imagenes = {imagen["nombre"]: imagen["imagen"] for imagen in imagenes_data}

# Recorrer los datos de los destinos y obtener las rutas de las imágenes
for destino in destinos_data:
    nombre_destino = destino["nombre"]
    actividad = destino["actividad"]
    fecha = destino["fecha"]

    if nombre_destino in rutas_imagenes:
        ruta_imagen = rutas_imagenes[nombre_destino]
        print(f"Destino: {nombre_destino}, Actividad: {actividad}, Fecha: {fecha}, Ruta Imagen: {ruta_imagen}\n")
    else:
        print(f"No se encontró imagen para el destino: {nombre_destino}")"""

"""from datetime import datetime

fechas_iso = [
    "2023-08-12T22:30:00",
    "2023-08-18T23:00:00",
    "2023-08-19T23:00:00",
    "2023-09-18T17:00:00",
    "2023-09-20T18:00:00"
]

formato_salida = "%d/%m/%Y"
hora_salida = "%H:%M"

fechas_legibles = []

for fecha_iso in fechas_iso:
    fecha_objeto = datetime.fromisoformat(fecha_iso)
    fecha_legible = fecha_objeto.strftime(formato_salida)
    hora_legible = fecha_objeto.strftime(hora_salida)
    fechas_legibles.append((fecha_legible, hora_legible))

for fecha_legible in fechas_legibles:
    print(fecha_legible)"""
import json


with open("../data/destinos.json", encoding="utf-8") as file:
    destinos_data = json.load(file)

ingredientes = []

for ingr in destinos_data:
    ingre = ingr["ingredientes"]
    print(ingre)
    for ingred in ingre:
        ingredientes.append(ingred)

print(f"sin set: {ingredientes}")

print(f"con set:{list(set(ingredientes))}")