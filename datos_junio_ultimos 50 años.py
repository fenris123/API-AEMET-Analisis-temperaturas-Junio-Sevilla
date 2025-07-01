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
año_actual = datetime.utcnow().year

# Lista para guardar todos los datos
todos_los_datos = []

# URL base
URL_BASE = "https://opendata.aemet.es/opendata"

# Iterar sobre los últimos 50 años para el mes de junio
for año in range(año_actual - 50, año_actual):
    fecha_ini = f"{año}-06-01T00:00:00UTC"
    fecha_fin = f"{año}-06-30T23:59:59UTC"
    print(f"\nObteniendo datos de JUNIO {año}...")

    PETICION = f"/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{idema}"
    respuesta = requests.get(URL_BASE + PETICION, headers=headers)

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
                    print(f"Error al decodificar los datos de junio {año}: {e}")
            else:
                print(f"No se encontró la clave 'datos' en junio {año}.")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar respuesta de junio {año}: {e}")
    else:
        print(f"Error en la petición de junio {año}: Código {respuesta.status_code}")

    sleep(5)  # Pausa para evitar saturar la API

# Guardar todos los datos en un archivo JSON
nombre_archivo = "datos_junio_ultimos_50_anos.json"
with open(nombre_archivo, "w", encoding="utf-8") as f:
    json.dump(todos_los_datos, f, indent=4, ensure_ascii=False)
print(f"\nTodos los datos guardados en {nombre_archivo}")


