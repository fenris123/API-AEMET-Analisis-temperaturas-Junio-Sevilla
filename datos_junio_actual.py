# pip install python-dotenv requests

import json
import os
import requests
import sys
from dotenv import load_dotenv
from datetime import datetime
from time import sleep

# PASO 1: CARGA DE TOKEN
load_dotenv("C:/espaciopython/enviroments/tokens.env")
Token_aemet = os.getenv("TOKEN_AEMET")

headers = {
    "accept": "application/json",
    "api_key": Token_aemet
}

# Estación fija
idema = "5783"

# Año actual
año = datetime.utcnow().year

# Rango de fechas de junio del año actual
fecha_ini = f"{año}-06-01T00:00:00UTC"
fecha_fin = f"{año}-06-30T23:59:59UTC"
print(f"Obteniendo datos de JUNIO {año}...")

# URL base y petición
URL_BASE = "https://opendata.aemet.es/opendata"
PETICION = f"/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{idema}"

respuesta = requests.get(URL_BASE + PETICION, headers=headers)

todos_los_datos = []

if respuesta.status_code == 200:
    try:
        data = respuesta.json()
        if "datos" in data:
            datos_url = data["datos"]
            print(f"Descargando desde: {datos_url}")

            respuesta_datos = requests.get(datos_url)
            try:
                datos_finales = json.loads(respuesta_datos.text)
                todos_los_datos.extend(datos_finales)
                print(f"Datos de junio {año} obtenidos correctamente.")
            except json.JSONDecodeError as e:
                print(f"Error al decodificar los datos: {e}")
        else:
            print("No se encontró la clave 'datos'.")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta: {e}")
else:
    print(f"Error en la petición: Código {respuesta.status_code}")

# Guardar archivo
nombre_archivo = f"datos_junio_{año}.json"
with open(nombre_archivo, "w", encoding="utf-8") as f:
    json.dump(todos_los_datos, f, indent=4, ensure_ascii=False)
print(f"Datos guardados en {nombre_archivo}")


