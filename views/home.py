import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import pandas as pd

st.title("¡Bienvenido a la Aplicación de Ambient Detectors! 🌡️☀️💨")


st.markdown("""
Esta aplicación está dedicada a mostrar datos en tiempo real de nuestra estación metereológica. 
Nuestra app mide varios parámetros metereológicos como:

- Temperatura
- Humedad
- Calidad del aire
- Intensidad lumínica
- CO2


Nuestra interfaz amigable al usuario te permite visualizar tendencias, comparar datos históricamente,
y ganar conocimiento acerca de los patrones de nuestro clima local.
""")


image_url = "https://picsum.photos/800/400"  
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
st.image(image, caption="Nuestra estación metereológica", use_column_width=True)

st.subheader("¡Mira la aplicación en acción!")
st.markdown("""
¿Quieres ver nuestra aplicación en acción? Mira nuestro demo en el siguiente video:

[Mira la demo de Ambient Detectors](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

Este video te guiará a través de las principales características de nuestra app y te enseñará a aprovechar al máximo los datos meteorológicos disponibles.
""")

st.subheader("Rangos utilizados para la Intensidad Lumínica")

df1 = pd.DataFrame({
    'Rango (lux)': ['0 - 10', '10 - 50', '50 - 500', '500 - 10,000', '> 10,000'],
    'Valor': [
        'Oscuro',
        'Tenue',
        'Iluminado',
        'Brillante',
        'Muy Brillante',
    ]
})
st.table(df1)
st.subheader("Rangos utilizados para Calidad del Aire")

df2 = pd.DataFrame({
    'Rango (ppm)': ['0 - 10', '10 - 50', '50 - 500', '500 - 10,000', '> 10,000'],
    'Valor': [
        'Bueno',
        'Moderado',
        'Poco Saludable',
        'No saludable',
        'Peligroso',
    ]
})
st.table(df2)

st.subheader("Rangos utilizados para CO2")

df3 = pd.DataFrame({
    'Rango (ppm)': ['0 - 10', '10 - 50', '50 - 500', '500 - 10,000', '> 10,000'],
    'Valor': [
        'Excelente',
        'Bueno',
        'Regular',
        'Pobre',
        'Peligroso',
    ]
})




st.table(df3)

st.subheader("¿Listo para explorar?")

st.page_link("views/graph.py", label="Empieza a explorar con nuestra estación metereológica")

st.markdown("---")
st.markdown(""" 
            Desarrollado por:
            
            Juan Alfonso Vega Sol A01751854.


            Jesús Emiliano García Jimenez A01751766.
            """)