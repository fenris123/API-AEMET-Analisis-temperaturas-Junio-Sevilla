 Proyecto: Análisis climático de Sevilla en el mes de junio (AEMET API)
Este proyecto utiliza la API de la AEMET para recopilar y analizar datos climáticos diarios del mes de junio en la estación "SEVILLA AEROPUERTO" (idema: 5783) a lo largo de los últimos 50 años.

🔹 Funcionalidad actual:
Obtención automática de los datos climáticos diarios de junio desde 1975 hasta 2024.

Extracción de:

Fecha (fecha)

Temperatura máxima (tmax)

Temperatura mínima (tmin)

Almacenamiento en un archivo JSON con todos los datos históricos.

Conversión a formato CSV mediante pandas para facilitar el análisis posterior.

⚠️ Nota importante:
Los datos del mes de junio de 2025 aún no están disponibles en su totalidad en la API de la AEMET.
Por tanto, este año no se ha incluido en el archivo histórico.
Si se desea usar los datos parciales disponibles de 2025, se deben descargar manualmente con el script correspondiente (junio_actual.py) y unirlos al archivo principal de forma independiente.

