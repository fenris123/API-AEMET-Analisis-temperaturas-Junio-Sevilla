# -*- coding: utf-8 -*-
"""

@author: fenris123
"""

# pip install python-dotenv requests

import json
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt



def obtener_datos_aemet( mes : str, idema: str):
    """
    Descarga datos diarios de AEMET para el mes y estación indicados durante los últimos 50 años.

    Parámetros:
        mes (str): Nombre del mes en minúsculas (ej: 'julio').
        idema (str): Código de estación meteorológica (ej: '5387').

    Guardará:
        - Archivos JSON por año en carpeta mes_idema.
        - Un archivo combinado con todos los datos.
    """

    # PASO 1: CARGA DE TOKEN
    load_dotenv("C:/espaciopython/enviroments/tokens.env")
    Token_aemet = os.getenv("TOKEN_AEMET")

    headers = {
        "accept": "application/json",
        "api_key": Token_aemet
    }

    # Año actual
    año_actual = datetime.utcnow().year

    # Carpeta para guardar los datos individuales
    carpeta_salida = f"{mes}_{idema}"
    os.makedirs(carpeta_salida, exist_ok=True)


    # Ver qué años ya han sido guardados
    años_guardados = {
        int(nombre_archivo.split("_")[-1].split(".")[0])
        for nombre_archivo in os.listdir(carpeta_salida)
        if nombre_archivo.startswith(f"{mes}_") and nombre_archivo.endswith(".json")
    }

    # URL base
    URL_BASE = "https://opendata.aemet.es/opendata"

    # Conversión de mes a número y días (simplificado, no contempla bisiestos)
    meses_dict = {
        "enero": ("01", 31),
        "febrero": ("02", 28),
        "marzo": ("03", 31),
        "abril": ("04", 30),
        "mayo": ("05", 31),
        "junio": ("06", 30),
        "julio": ("07", 31),
        "agosto": ("08", 31),
        "septiembre": ("09", 30),
        "octubre": ("10", 31),
        "noviembre": ("11", 30),
        "diciembre": ("12", 31)
        }



    mes_num, dias_mes = meses_dict[mes]

    # Iterar sobre los últimos 50 años





    for año in range(año_actual - 50, año_actual + 1):    #### WARNING:  PUEDE NO HABER DATOS.  QUITAR + 1 para año anterior
        if año in años_guardados:
            print(f"Ya existen datos de {mes} {año}, saltando...")
            continue

        fecha_ini = f"{año}-{mes_num}-01T00:00:00UTC"
        fecha_fin = f"{año}-{mes_num}-{dias_mes}T23:59:59UTC"
        print(f"\nObteniendo datos de {mes.upper()} {año}...")

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
                        # Guardar individualmente
                        nombre_archivo = os.path.join(carpeta_salida, f"{mes}_{año}.json")
                        with open(nombre_archivo, "w", encoding="utf-8") as f:
                            json.dump(datos_finales, f, indent=4, ensure_ascii=False)
                        print(f"Datos de {mes} {año} guardados en {nombre_archivo}")
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar los datos de {mes} {año}: {e}")
                else:
                    print(f"No se encontró la clave 'datos' en {mes} {año}.")
            except json.JSONDecodeError as e:
                print(f"Error al decodificar respuesta de {mes} {año}: {e}")
        else:
            print(f"Error en la petición de {mes} {año}: Código {respuesta.status_code}")

        sleep(10)  # Pausa para evitar saturar la API

    print(f"\nProceso terminado. Archivos almacenados en la carpeta: {carpeta_salida}")

    # Unir todos los archivos individuales en uno solo
    datos_unificados = []

    for archivo in sorted(os.listdir(carpeta_salida)):
        if archivo.startswith(f"{mes}_") and archivo.endswith(".json"):
            ruta = os.path.join(carpeta_salida, archivo)
            with open(ruta, "r", encoding="utf-8") as f:
                try:
                    datos = json.load(f)
                    datos_unificados.extend(datos)
                except json.JSONDecodeError as e:
                    print(f"Error al leer {archivo}: {e}")

    # Ruta de salida final
    ruta_salida_final = os.path.join(carpeta_salida, f"datos_{mes}_ultimos_50_anos.json")

    # Guardar el archivo combinado
    with open(ruta_salida_final, "w", encoding="utf-8") as f:
        json.dump(datos_unificados, f, indent=4, ensure_ascii=False)

    print(f"\nArchivo combinado guardado en: {ruta_salida_final}")


# Si se ejecuta directamente, pedirá mes y estación
if __name__ == "__main__":
    mes_input = input("Introduce el mes a buscar (en minúsculas, ej: 'julio'): ").strip().lower()
    idema_input = input("Introduce el número de estación: ").strip()
    obtener_datos_aemet(mes_input, idema_input)




def crear_df_temperaturas(ruta_json, guardar_csv=True):
    """
    Convierte un archivo JSON de datos AEMET a un DataFrame con fecha, tmax y tmin.
    Convierte temperaturas a numérico y opcionalmente guarda en CSV.

    Parámetros:
        ruta_json (str): Ruta al archivo JSON combinado o individual.
        guardar_csv (bool): Si True, guarda el CSV en la misma carpeta.

    Retorna:
        df (pd.DataFrame): DataFrame con columnas fecha, tmax, tmin.
    """
    if not os.path.exists(ruta_json):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_json}")

    with open(ruta_json, encoding="utf-8") as f:
        datos = json.load(f)

    df = pd.DataFrame(datos)[["fecha", "tmax", "tmin"]]

    # Convertir a numérico (pueden venir como string con coma)
    df["tmax"] = pd.to_numeric(df["tmax"].astype(str).str.replace(",", "."), errors="coerce")
    df["tmin"] = pd.to_numeric(df["tmin"].astype(str).str.replace(",", "."), errors="coerce")

    # Convertir fecha a datetime
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

    if guardar_csv:
        ruta_csv = os.path.splitext(ruta_json)[0] + ".csv"
        df.to_csv(ruta_csv, index=False, encoding="utf-8")
        print(f"CSV guardado en: {ruta_csv}")

    return df


def graficar_temperaturas(ruta_completo):
    """
    Gráfica scatter de Tmax y Tmin, comparando años anteriores con el año más reciente.
    """
    # Si no existen CSV, crearlos desde JSON
    if not ruta_completo.lower().endswith(".csv"):
        crear_df_temperaturas(ruta_completo, guardar_csv=True)
        ruta_completo = os.path.splitext(ruta_completo)[0] + ".csv"

    # Cargar CSV
    df = pd.read_csv(ruta_completo, parse_dates=["fecha"])

    año_actual = df['fecha'].dt.year.max()  # Año más reciente

    df_anteriores = df[df['fecha'].dt.year < año_actual].copy()
    df_actual = df[df['fecha'].dt.year == año_actual].copy()

    df_anteriores['dia'] = df_anteriores['fecha'].dt.day
    df_actual['dia'] = df_actual['fecha'].dt.day

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.scatter(df_anteriores['dia'], df_anteriores['tmax'], facecolors='none', edgecolors='red', label=f'Tmax hasta {año_actual - 1}')
    ax.scatter(df_anteriores['dia'], df_anteriores['tmin'], facecolors='none', edgecolors='blue', label=f'Tmin hasta {año_actual - 1}')

    ax.scatter(df_actual['dia'], df_actual['tmax'], color='black', marker='^', s=100, label=f'Tmax {año_actual}')
    ax.scatter(df_actual['dia'], df_actual['tmin'], color='black', marker='v', s=100, label=f'Tmin {año_actual}')

    ax.set_xlabel('Día del mes')
    ax.set_ylabel('Temperatura (°C)')
    ax.set_title(f'Temperaturas máximas y mínimas ({año_actual} vs anteriores)')
    ax.set_xticks(range(1, df_actual['dia'].max() + 1))
    ax.legend()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout(pad=3.0)
    plt.show()


def graficar_banda_tmax(ruta_completo):
    """
    Grafica la banda ±2 desviaciones típicas de Tmax de años anteriores, con el mes actual superpuesto.
    """
    # Si no existen CSV, crearlos desde JSON
    if not ruta_completo.lower().endswith(".csv"):
        crear_df_temperaturas(ruta_completo, guardar_csv=True)
        ruta_completo = os.path.splitext(ruta_completo)[0] + ".csv"

    df = pd.read_csv(ruta_completo, parse_dates=['fecha'])

    año_actual = df['fecha'].dt.year.max()
    df_anteriores = df[df['fecha'].dt.year < año_actual].copy()
    df_actual = df[df['fecha'].dt.year == año_actual].copy()

    df_anteriores['dia'] = df_anteriores['fecha'].dt.day
    df_actual['dia'] = df_actual['fecha'].dt.day

    # Estadísticas Tmax
    stats = df_anteriores.groupby('dia')['tmax'].agg(['mean', 'std']).reset_index()
    stats['upper'] = stats['mean'] + 2 * stats['std']
    stats['lower'] = stats['mean'] - 2 * stats['std']

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('white')

    ax.plot(stats['dia'], stats['mean'], label='Media Tmax', color='black', linewidth=2)
    ax.plot(stats['dia'], stats['upper'], label='Media + 2 std', color='#ff9999', linestyle='--', linewidth=2)
    ax.plot(stats['dia'], stats['lower'], label='Media - 2 std', color='#99ccff', linestyle='--', linewidth=2)

    ax.fill_between(stats['dia'], stats['lower'], stats['upper'], color='#f28b82', alpha=1.0)

    ax.set_xlim(1, stats['dia'].max())

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel('Día del mes')
    ax.set_ylabel('Temperatura máxima (°C)')
    ax.set_title(f'Media y banda ±2 desviaciones típicas de Tmax (hasta {año_actual - 1})')

    ax.set_xticks(range(1, stats['dia'].max() + 1))

    ax.scatter(df_actual['dia'], df_actual['tmax'], color='red', edgecolors='black', marker='^', s=100, label=f'Tmax {año_actual}')

    ax.legend()

    plt.tight_layout(pad=3.0)
    plt.show()


def graficar_banda_tmin(ruta_completo):
    """
    Grafica la banda ±2 desviaciones típicas de Tmin de años anteriores, con el mes actual superpuesto.
    """
    # Si no existen CSV, crearlos desde JSON
    if not ruta_completo.lower().endswith(".csv"):
        crear_df_temperaturas(ruta_completo, guardar_csv=True)
        ruta_completo = os.path.splitext(ruta_completo)[0] + ".csv"

    df = pd.read_csv(ruta_completo, parse_dates=['fecha'])

    año_actual = df['fecha'].dt.year.max()
    df_anteriores = df[df['fecha'].dt.year < año_actual].copy()
    df_actual = df[df['fecha'].dt.year == año_actual].copy()

    df_anteriores['dia'] = df_anteriores['fecha'].dt.day
    df_actual['dia'] = df_actual['fecha'].dt.day

    # Estadísticas Tmin
    stats = df_anteriores.groupby('dia')['tmin'].agg(['mean', 'std']).reset_index()
    stats['upper'] = stats['mean'] + 2 * stats['std']
    stats['lower'] = stats['mean'] - 2 * stats['std']

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('white')

    ax.plot(stats['dia'], stats['mean'], label='Media Tmin', color='black', linewidth=2)
    ax.plot(stats['dia'], stats['upper'], label='Media + 2 std', color='#99ccff', linestyle='--', linewidth=2)
    ax.plot(stats['dia'], stats['lower'], label='Media - 2 std', color='#3399ff', linestyle='--', linewidth=2)

    ax.fill_between(stats['dia'], stats['lower'], stats['upper'], color='#99ccff', alpha=0.8)

    ax.set_xlim(1, stats['dia'].max())

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel('Día del mes')
    ax.set_ylabel('Temperatura mínima (°C)')
    ax.set_title(f'Media y banda ±2 desviaciones típicas de Tmin (hasta {año_actual - 1})')

    ax.set_xticks(range(1, stats['dia'].max() + 1))

    ax.scatter(df_actual['dia'], df_actual['tmin'], color='blue', edgecolors='black', marker='v', s=100, label=f'Tmin {año_actual}')

    ax.legend()

    plt.tight_layout(pad=3.0)
    plt.show()


# Ejemplo de uso
if __name__ == "__main__":


    # Descarga y guarda los datos JSON y el combinado
    obtener_datos_aemet(mes_input, idema_input)

    carpeta = f"{mes_input}_{idema_input}"
    ruta_json_completo = os.path.join(carpeta, f"datos_{mes_input}_ultimos_50_anos.json")

    # Crear CSV si no existe y cargar datos
    crear_df_temperaturas(ruta_json_completo, guardar_csv=True)

    # Graficar datos generales scatter Tmax y Tmin
    graficar_temperaturas(ruta_json_completo)

    # Graficar banda ±2 std de Tmax con mes actual
    graficar_banda_tmax(ruta_json_completo)

    # Graficar banda ±2 std de Tmin con mes actual
    graficar_banda_tmin(ruta_json_completo)