# pip install python-dotenv requests pandas matplotlib

import os
import json
import requests
import pandas as pd
import matplotlib.pyplot as plt

from time import sleep
from datetime import datetime
from dotenv import load_dotenv


# =========================
# CONFIG TOKEN
# =========================

TOKEN_AEMET= tu_token_aqui

headers = {
    "accept": "application/json",
    "api_key": TOKEN
}

URL_BASE = "https://opendata.aemet.es/opendata"


# =========================
# INPUT USUARIO
# =========================
mes_input = input("Introduce mes (1-12): ")
mes = int(mes_input)

estacion = input("Introduce idema (ENTER = 5783): ")
if estacion.strip() == "":
    estacion = "5783"


nombre_mes = f"{mes:02d}"


# =========================
# FUNCION DESCARGA AEMET
# =========================
def descargar_datos(año, mes, estacion):
    fecha_ini = f"{año}-{mes:02d}-01T00:00:00UTC"
    fecha_fin = f"{año}-{mes:02d}-30T23:59:59UTC"

    endpoint = f"/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{estacion}"

    try:
        r = requests.get(URL_BASE + endpoint, headers=headers, timeout=10)
    except Exception as e:
        print(f"Error conexión {año}: {e}")
        return []

    if r.status_code != 200:
        print(f"Error API {año}: {r.status_code}")
        return []

    try:
        meta = r.json()
        datos_url = meta.get("datos")

        if not datos_url:
            return []

        r2 = requests.get(datos_url)
        return json.loads(r2.text)

    except Exception as e:
        print(f"Error parseando {año}: {e}")
        return []


# =========================
# DESCARGA HISTORICA
# =========================


año_actual = datetime.utcnow().year
datos_totales = []

print("\nDescargando histórico...\n")

for año in range(año_actual - 50, año_actual):

    print(f"Año {año}")

    max_intentos = 3
    datos = []

    for intento in range(max_intentos):

        datos = descargar_datos(año, mes, estacion)

        # OK
        if datos:
            datos_totales.extend(datos)
            break

        # ERROR → retry con backoff
        print(f"  Intento {intento+1} fallido en {año}")

        sleep(2 * (intento + 1))

    else:
        print(f"  ❌ Año {año} descartado tras {max_intentos} intentos")

    # Pausa global para evitar 429
    sleep(1.5)


# =========================
# DESCARGA AÑO ACTUAL
# =========================
print("\nDescargando año actual...")

datos_actual = descargar_datos(año_actual, mes, estacion)
datos_totales.extend(datos_actual)


# =========================
# DATAFRAME
# =========================
df = pd.DataFrame(datos_totales)

df = df[["fecha", "tmax", "tmin"]]
df["fecha"] = pd.to_datetime(df["fecha"])

df["tmax"] = pd.to_numeric(df["tmax"].astype(str).str.replace(",", "."), errors="coerce")
df["tmin"] = pd.to_numeric(df["tmin"].astype(str).str.replace(",", "."), errors="coerce")

df["dia"] = df["fecha"].dt.day
df["anio"] = df["fecha"].dt.year


# =========================
# ESTADISTICAS (hasta año anterior)
# =========================
df_hist = df[df["anio"] < año_actual]

stats_max = df_hist.groupby("dia")["tmax"].agg(["mean", "std"]).reset_index()
stats_min = df_hist.groupby("dia")["tmin"].agg(["mean", "std"]).reset_index()

stats_max["upper"] = stats_max["mean"] + 2 * stats_max["std"]
stats_max["lower"] = stats_max["mean"] - 2 * stats_max["std"]

stats_min["upper"] = stats_min["mean"] + 2 * stats_min["std"]
stats_min["lower"] = stats_min["mean"] - 2 * stats_min["std"]


# =========================
# DATOS AÑO ACTUAL
# =========================
df_act = df[df["anio"] == año_actual]


# =========================
# GRAFICO 1: SCATTER
# =========================
plt.figure(figsize=(12, 6))

df_hist = df[df["anio"] < año_actual]

plt.scatter(df_hist["dia"], df_hist["tmax"], facecolors="none", edgecolors="red", label="Tmax histórico")
plt.scatter(df_hist["dia"], df_hist["tmin"], facecolors="none", edgecolors="blue", label="Tmin histórico")

plt.scatter(df_act["dia"], df_act["tmax"], color="black", marker="^", s=80, label="Tmax actual")
plt.scatter(df_act["dia"], df_act["tmin"], color="black", marker="v", s=80, label="Tmin actual")

plt.title(f"Scatter temperaturas mes {mes}")
plt.xlabel("Día")
plt.ylabel("Temperatura")
plt.legend()
plt.grid(True)
plt.show()


# =========================
# GRAFICO 2: MAXIMAS
# =========================
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(stats_max['dia'], stats_max['mean'],
        label='Media Tmax', color='black', linewidth=2)

ax.plot(stats_max['dia'], stats_max['upper'],
        color='red', linestyle='--', linewidth=2)

ax.plot(stats_max['dia'], stats_max['lower'],
        color='red', linestyle='--', linewidth=2)

ax.fill_between(stats_max['dia'],
                stats_max['lower'],
                stats_max['upper'],
                color='red',
                alpha=0.25)

ax.scatter(df_act["dia"], df_act["tmax"],
           color="red",
           edgecolors="black",
           marker="^",
           s=80,
           label="Tmax actual")

ax.legend()
ax.set_title("Temperatura máxima (histórico + actual)")
ax.set_xlabel("Día")
ax.set_ylabel("Temperatura")


# =========================
# GRAFICO 3: MINIMAS
# =========================
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(stats_min['dia'], stats_min['mean'],
        label='Media Tmin', color='black', linewidth=2)

ax.plot(stats_min['dia'], stats_min['upper'],
        color='#1f77b4', linestyle='--', linewidth=2)

ax.plot(stats_min['dia'], stats_min['lower'],
        color='#1f77b4', linestyle='--', linewidth=2)

ax.fill_between(stats_min['dia'],
                stats_min['lower'],
                stats_min['upper'],
                color='#1f77b4',
                alpha=0.25)


ax.scatter(df_act["dia"], df_act["tmin"],
           color="blue",
           edgecolors="black",
           marker="v",
           s=80,
           label="Tmin actual")

ax.legend()
ax.set_title("Temperatura mínima (histórico + actual)")
ax.set_xlabel("Día")
ax.set_ylabel("Temperatura")
