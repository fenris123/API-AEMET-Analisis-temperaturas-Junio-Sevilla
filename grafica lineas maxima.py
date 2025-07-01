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

# Calcular media y desviación típica de Tmax por día
stats = df_anteriores.groupby('dia')['tmax'].agg(['mean', 'std']).reset_index()
stats['upper'] = stats['mean'] + 2 * stats['std']
stats['lower'] = stats['mean'] - 2 * stats['std']

# Datos de 2025 para superponer (solo Tmax)
df_2025 = df[df['fecha'].dt.year == 2025].copy()
df_2025['dia'] = df_2025['fecha'].dt.day

# Crear figura y eje
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_facecolor('white')  # fondo blanco

# Líneas de media y bandas
ax.plot(stats['dia'], stats['mean'], label='Media Tmax', color='black', linewidth=2)
ax.plot(stats['dia'], stats['upper'], label='Media + 2 std', color='#ff9999', linestyle='--', linewidth=2)
ax.plot(stats['dia'], stats['lower'], label='Media - 2 std', color='#99ccff', linestyle='--', linewidth=2)

# Relleno banda gris claro
ax.fill_between(stats['dia'], stats['lower'], stats['upper'], color='#f28b82', alpha=1.0)

# Limitar eje X de 1 a 30
ax.set_xlim(1, 30)

# Quitar bordes superior y derecho
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Etiquetas y título
ax.set_xlabel('Día del mes de junio')
ax.set_ylabel('Temperatura máxima (°C)')
ax.set_title('Media y banda ±2 desviaciones típicas de Tmax (hasta 2024)')

# Ticks X
ax.set_xticks(range(1, 31))

# Puntos Tmax 2025 superpuestos
ax.scatter(df_2025['dia'], df_2025['tmax'], color='red', edgecolors='black', marker='^', s=100, label='Tmax 2025')

# Leyenda
ax.legend()

plt.tight_layout(pad=3.0)
plt.show()
