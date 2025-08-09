# Proyecto: Análisis climático usando la web de AEMET (API AEMET)
Este proyecto utiliza la API de la AEMET para recopilar y analizar datos climáticos diarios del mes de junio en la estación "SEVILLA AEROPUERTO" (idema: 5783) a lo largo de los últimos 50 años.

(Vease la actualizacion en la parte final de este texto  si se desean estudiar datos de otros meses y estaciones).

## 🔹 Funcionalidad actual
Obtención automática de los datos climáticos diarios de junio desde 1975 hasta 2024.

Extracción de:

Fecha (fecha)

Temperatura máxima (tmax)

Temperatura mínima (tmin)

Almacenamiento en un archivo JSON con todos los datos históricos.

Conversión a formato CSV mediante pandas para facilitar el análisis posterior.

Generación de tres tipos de gráficos para el análisis de las temperaturas:

Gráfico de dispersión (scatter plot) con todas las temperaturas máximas y mínimas de todos los años hasta 2024, con los datos de 2025 superpuestos y destacados.

Gráfico de líneas para la temperatura máxima, mostrando la media diaria hasta 2024 junto con una banda de incertidumbre calculada como media ± 2 desviaciones típicas.

Gráfico de líneas para la temperatura mínima, con la misma lógica que el gráfico de máxima, usando colores y bandas específicas para las temperaturas mínimas.

## ⚠️ Notas importantes

1 Nuestros archivos se ejecutaron desde la carpeta C:\espaciopython\CODIGOS UTILES\GRAFICA_AEMET
Es posible, sobre todo con los codigos subidos mas recientemente y menos pulidos que si se instalan en otra carpeta haya algun problema.

2 Los datos del mes de junio de 2025 aún no están disponibles en su totalidad en la API de la AEMET.
Por tanto, este año no se ha incluido en el archivo histórico.
Si se desean usar los datos parciales disponibles de 2025, se deben descargar manualmente con el script correspondiente (junio_actual.py) y unirlos al archivo principal de forma independiente.

(vease actualizacion, mas abajo.)

## 🔐 Configuración del token de acceso
Para poder acceder a la API de la AEMET es necesario disponer de un token válido.

Este token debe guardarse en un archivo .env con la siguiente variable de entorno:

ini
Copiar
Editar
TOKEN_AEMET=tu_token_aqui
El script carga este token con la librería python-dotenv.

Importante:
Debes modificar la ruta al archivo .env en el código para que apunte a la ubicación correcta en tu sistema.

Por ejemplo, en tu script:

python
Copiar
Editar
from dotenv import load_dotenv
load_dotenv("C:/ruta/a/tu/archivo/tokens.env")
Asegúrate de que esa ruta corresponda a donde realmente está tu archivo .env.

## 📂 Orden de ejecución de los archivos
datos_junio_ultimos_50_anos.py

datos_junio_actual.py (opcional, para datos parciales de 2025)

convertidor_df.py

scatter_plot.py

grafica_lineas_maxima.py

grafica_lineas_minima.py


# ACTUALIZACION:
Se ha añadido un archivo (Graficador temp) que permite tomar los datos del mes deseado en la estacion meteorologica deseada y hace todas las funciones descritas arriba y permite usarlas como funciones si ya se tienen los datos.

Este archivo toma automaticamente los datos del año actual si estan disponibles.

Ademas, creara una nueva carpeta para almacenar los datos del mes y estacion seleccionados.

Recomendamos tener cuidado con las rutas: nuestro archivo estaba en C:\espaciopython\CODIGOS UTILES\GRAFICA_AEMET y se ejecuto desde ahi. 




