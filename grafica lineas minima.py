# -*- coding: utf-8 -*-
"""
Created on Tue Jul  1 16:33:48 2025

@author: fenris123
"""

import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos (todos los años)
df = pd.read_csv("datos_junio.csv", parse_dates=['fecha'])

# Datos hasta 2024 para estadística
df_anteriores = df[df['fecha'].dt.year <= 2024].copy()
df_anteriores['dia'] = df_anteriores['fecha'].dt.day

# Calcular media y desviación típica de Tmin por día
stats_min = df_anteriores.groupby('dia')['tmin'].agg(['mean', 'std']).reset_index()
stats_min['upper'] = stats_min['mean'] + 2 * stats_min['std']
stats_min['lower'] = stats_min['mean'] - 2 * stats_min['std']

# Datos de 2025 para superponer (solo Tmin)
df_2025 = df[df['fecha'].dt.year == 2025].copy()
df_2025['dia'] = df_2025['fecha'].dt.day

# Crear figura y eje
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('white')  # fondo blanco

# Líneas de media y bandas (azules)
ax.plot(stats_min['dia'], stats_min['mean'], label='Media Tmin', color='black', linewidth=2)
ax.plot(stats_min['dia'], stats_min['upper'], label='Media + 2 std', color='#99ccff', linestyle='--', linewidth=2)  # azul claro
ax.plot(stats_min['dia'], stats_min['lower'], label='Media - 2 std', color='#3399ff', linestyle='--', linewidth=2)  # azul más oscuro

# Relleno banda azul claro
ax.fill_between(stats_min['dia'], stats_min['lower'], stats_min['upper'], color='#99ccff', alpha=0.8)


# Limitar eje X de 1 a 30
ax.set_xlim(1, 30)

# Quitar bordes superior y derecho
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Etiquetas y título
ax.set_xlabel('Día del mes de junio')
ax.set_ylabel('Temperatura mínima (°C)')
ax.set_title('Media y banda ±2 desviaciones típicas de Tmin (hasta 2024)')

# Ticks X
ax.set_xticks(range(1, 31))

# Puntos Tmin 2025 superpuestos
ax.scatter(df_2025['dia'], df_2025['tmin'], color='blue', edgecolors='black', marker='v', s=100, label='Tmin 2025')

# Leyenda
ax.legend()

plt.tight_layout(pad=3.0)
plt.show()
