# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 16:33:48 2025

@author: fenris123
"""

import pandas as pd
import matplotlib.pyplot as plt

# Cargar y preparar datos
df = pd.read_csv("datos_junio.csv", parse_dates=['fecha'])

# Separar datos hasta 2024 y los de 2025
df_anteriores = df[df['fecha'].dt.year <= 2024].copy()
df_2025 = df[df['fecha'].dt.year == 2025].copy()

# Extraer día del mes
df_anteriores['dia'] = df_anteriores['fecha'].dt.day
df_2025['dia'] = df_2025['fecha'].dt.day

# Crear figura
fig, ax = plt.subplots(figsize=(12, 6))

# Datos hasta 2024 (sin relleno)
ax.scatter(df_anteriores['dia'], df_anteriores['tmax'], facecolors='none', edgecolors='red', label='Tmax hasta 2024')
ax.scatter(df_anteriores['dia'], df_anteriores['tmin'], facecolors='none', edgecolors='blue', label='Tmin hasta 2024')

# Datos de 2025 (rellenos, forma distinta, color llamativo, tamaño mayor)
ax.scatter(df_2025['dia'], df_2025['tmax'], color='black', marker='^', s=100, label='Tmax 2025')
ax.scatter(df_2025['dia'], df_2025['tmin'], color='black', marker='v', s=100, label='Tmin 2025')

# Estética
ax.set_xlabel('Día del mes de junio')
ax.set_ylabel('Temperatura (°C)')
ax.set_title('Temperaturas máximas y mínimas en junio (hasta 2024 + 2025)')
ax.set_xticks(range(1, 31))
ax.legend()

# Quitar bordes superior y derecho
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Aumentar margen externo
plt.tight_layout(pad=3.0)

plt.show()