# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 13:52:54 2025

@author: fenris123
"""

# pip install pandas

import json
import pandas as pd

# Cargar los datos desde un archivo JSON
with open("datos_junio_totales.json", encoding="utf-8") as f:
    datos = json.load(f)

# Crear un DataFrame con solo las columnas deseadas
df = pd.DataFrame(datos)[["fecha", "tmax", "tmin"]]

# Convertir columnas de temperatura a tipo numérico (pueden venir como string)
df["tmax"] = pd.to_numeric(df["tmax"].str.replace(",", "."), errors="coerce")
df["tmin"] = pd.to_numeric(df["tmin"].str.replace(",", "."), errors="coerce")

df.to_csv("datos_junio.csv", index=False, encoding="utf-8")

print(df.head())