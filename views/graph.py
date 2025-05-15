import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import plotly.express as px
import time
import os
from dotenv import load_dotenv

load_dotenv()

def clean_temperature_data():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM medicion WHERE id_sensor = '1' AND dato > 100;"
            cursor.execute(delete_query)
            connection.commit()
        except Error as e:
            st.write("Error al intentar eliminar los datos:", e)
        return

def clean_humidity_data():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM medicion WHERE id_sensor = '2' AND dato > 100;"
            cursor.execute(delete_query)
            connection.commit()
        except Error as e:
            st.write("Error al intentar eliminar los datos:", e)
        return

def clean_lux_data():
    connection = connect_db()
    if connection:
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM medicion WHERE id_sensor = '5' AND dato > 100000;"
            cursor.execute(delete_query)
            connection.commit()
        except Error as e:
            st.write("Error al intentar eliminar los datos:", e)
        return

def connect_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        return None

def HumidityData():
    connection = connect_db()
    if connection:
        query = "SELECT fecha, dato FROM medicion WHERE id_sensor = '2';"
        data = pd.read_sql(query, connection)
        connection.close()
        data['fecha'] = pd.to_datetime(data['fecha']) 
        return data
    else:
        return pd.DataFrame() 

def TemperatureData():
    connection = connect_db()
    if connection:
        query = "SELECT fecha, dato FROM medicion WHERE id_sensor = '1';"
        data = pd.read_sql(query, connection)
        connection.close()
        return data
    else:
        return pd.DataFrame()  

def GasData():
    connection = connect_db()
    if connection:
        query = "SELECT fecha, dato FROM medicion WHERE id_sensor = '3';"
        data = pd.read_sql(query, connection)
        connection.close()
        return data
    else:
        return pd.DataFrame()  

def Co2Data():
    connection = connect_db()
    if connection:
        query = "SELECT fecha, dato FROM medicion WHERE id_sensor = '4';"
        data = pd.read_sql(query, connection)
        connection.close()
        return data
    else:
        return pd.DataFrame()  

def LuxData():
    connection = connect_db()
    if connection:
        query = "SELECT fecha, dato FROM medicion WHERE id_sensor = '5';"
        data = pd.read_sql(query, connection)
        connection.close()
        data['fecha'] = pd.to_datetime(data['fecha']) 
        return data
    else:
        return pd.DataFrame() 

def metrics(humidityData, temperatureData, luxData):
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi4, kpi5 = st.columns(2)

    last_humidity = humidityData['dato'].iloc[-1] if not humidityData.empty else "N/A"
    last_temperature = temperatureData['dato'].iloc[-1] if not temperatureData.empty else "N/A"
    last_lux = luxData['dato'].iloc[-1] if not luxData.empty else 0

    if (last_lux ==0):
        lux = "N/A"
    
    if (last_lux > 0 and last_lux <=10):
        lux = "Oscuro"
    if (last_lux >10 and last_lux <=50):
        lux = "Tenue"
    if (last_lux >50 and last_lux <=500):
        lux = "Iluminado"
    if (last_lux >500 and last_lux <=10000):
        lux = "Billante"
    if (last_lux >10000):
        lux = "Muy Brillante"

    kpi1.metric(label="Temperatura ", value=str(last_temperature) + "°C 🌡️")
    kpi2.metric(label="Humedad ", value=str(last_humidity) + "% 💧")
    kpi3.metric(label="Calidad del Aire ", value="Buena" + " 💨")
    kpi4.metric(label="CO2 ", value="Normal" + " 🌬️")
    kpi5.metric(label="Intensidad Lumínica ", value=lux + " 💡")

def Tgraphs(temperatureData, iteration):
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.subheader("Temperatura")
        if temperatureData.empty:
            st.write("No hay datos registrados por el momento")
        else:
            temperatureData['dato'] = pd.to_numeric(temperatureData['dato'], errors='coerce')
            temperatureData = temperatureData.dropna()

            temperature_chart = px.line(
                temperatureData,
                x='fecha',
                y='dato',
                title="Datos de Temperatura a lo Largo del Tiempo",
                labels={'dato': 'Temperatura (°C)', 'fecha': 'Fecha y Hora'},
                line_shape='linear'
            )
            temperature_chart.update_traces(line=dict(color='red'))  

            temperature_chart.update_layout(
                height=400,
                width=600,
                xaxis_tickformat='%Y-%m-%d %H:%M:%S'
            )

            st.plotly_chart(temperature_chart, use_container_width=True, key=f'temperature_chart_{iteration}')

    with fig_col2:
        st.markdown("### Histograma de Temperatura")
        if temperatureData.empty:
            st.write("No hay datos registrados por el momento")
        else:
            histogram_chart = px.histogram(
                temperatureData,
                x='dato',
                nbins=20,
                title="Distribución de Temperatura",
                labels={'dato': 'Temperatura (°C)'}
            )
            histogram_chart.update_traces(marker_color='red') 

           
            st.plotly_chart(histogram_chart, use_container_width=True, key=f'Thistogram_chart_{iteration}')

def Hgraphs(humidityData, iteration):
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.subheader("Humedad")
        if humidityData.empty:
            st.write("No hay datos registrados por el momento")
        else:
            humidityData['dato'] = pd.to_numeric(humidityData['dato'], errors='coerce')
            humidityData = humidityData.dropna()

            humidity_chart = px.line(
                humidityData,
                x='fecha',
                y='dato',
                title="Datos de Humedad a lo Largo del Tiempo",
                labels={'dato': 'Humedad (%)', 'fecha': 'Fecha y Hora'},
                line_shape='linear'
            )
            humidity_chart.update_traces(line=dict(color='blue'))  

            humidity_chart.update_layout(
                height=400,
                width=600,
                xaxis_tickformat='%Y-%m-%d %H:%M:%S'
            )

            st.plotly_chart(humidity_chart, use_container_width=True, key=f'humidity_chart_{iteration}')

    with fig_col2:
        st.markdown("### Histograma de Humedad")
        if humidityData.empty:
            st.write("No hay datos registrados por el momento")
        else:
            histogram_chart = px.histogram(
                humidityData,
                x='dato',
                nbins=20,
                title="Distribución de Humedad",
                labels={'dato': 'Humedad (%)'}
            )
            histogram_chart.update_traces(marker_color='blue') 

           
            st.plotly_chart(histogram_chart, use_container_width=True, key=f'Hhistogram_chart_{iteration}')

def Ggraphs(gasData, iteration):
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.subheader("Calidad del Aire")
        if gasData.empty:
            st.write("No hay datos registrados por el momento")
        else:
            gasData['dato'] = pd.to_numeric(gasData['dato'], errors='coerce')
            gasData = gasData.dropna()

            gas_chart = px.line(
                gasData,
                x='fecha',
                y='dato',
                title="Datos de C.A. a lo Largo del Tiempo",
                labels={'dato': 'CA (ppm)', 'fecha': 'Fecha y Hora'},
                line_shape='linear'
            )
            gas_chart.update_traces(line=dict(color='green'))  

            gas_chart.update_layout(
                height=400,
                width=600,
                xaxis_tickformat='%Y-%m-%d %H:%M:%S'
            )

            st.plotly_chart(gas_chart, use_container_width=True, key=f'gas_chart_{iteration}')

    with fig_col2:
        st.markdown("### Histograma de Calidad del Aire")
        if gasData.empty:
            st.write("No hay datos registrados por el momento")
        else:
            histogram_chart = px.histogram(
                gasData,
                x='dato',
                nbins=20,
                title="Distribución de Calidad del Aire",
                labels={'dato': 'CA (ppm)'}
            )
            histogram_chart.update_traces(marker_color='green') 

           
            st.plotly_chart(histogram_chart, use_container_width=True, key=f'Ghistogram_chart_{iteration}')

def Cgraphs(co2Data, iteration):
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.subheader("Dióxido de Carbono")
        if co2Data.empty:
            st.write("No hay datos registrados por el momento")
        else:
            co2Data['dato'] = pd.to_numeric(co2Data['dato'], errors='coerce')
            co2Data = co2Data.dropna()

            co2_chart = px.line(
                co2Data,
                x='fecha',
                y='dato',
                title="Datos de CO2 a lo Largo del Tiempo",
                labels={'dato': 'CO2 (ppm)', 'fecha': 'Fecha y Hora'},
                line_shape='linear'
            )
            co2_chart.update_traces(line=dict(color='orange'))  

            co2_chart.update_layout(
                height=400,
                width=600,
                xaxis_tickformat='%Y-%m-%d %H:%M:%S'
            )

            st.plotly_chart(co2_chart, use_container_width=True, key=f'co2_chart_{iteration}')

    with fig_col2:
        st.markdown("### Histograma de Dióxido de Carbono")
        if co2Data.empty:
            st.write("No hay datos registrados por el momento")
        else:
            histogram_chart = px.histogram(
                co2Data,
                x='dato',
                nbins=20,
                title="Distribución de CO2",
                labels={'dato': 'CO2(ppm)'}
            )
            histogram_chart.update_traces(marker_color='orange') 

           
            st.plotly_chart(histogram_chart, use_container_width=True, key=f'Chistogram_chart_{iteration}')

def Lgraphs(luxData, iteration):
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.subheader("Intensidad Lumínica")
        if luxData.empty:
            st.write("No hay datos registrados por el momento")
        else:
            luxData['dato'] = pd.to_numeric(luxData['dato'], errors='coerce')
            luxData = luxData.dropna()

            lux_chart = px.line(
                luxData,
                x='fecha',
                y='dato',
                title="Datos de LUX a lo Largo del Tiempo",
                labels={'dato': 'LUX (lx)', 'fecha': 'Fecha y Hora'},
                line_shape='linear'
            )
            lux_chart.update_traces(line=dict(color='yellow'))  

            lux_chart.update_layout(
                height=400,
                width=600,
                xaxis_tickformat='%Y-%m-%d %H:%M:%S'
            )

            st.plotly_chart(lux_chart, use_container_width=True, key=f'lux_chart_{iteration}')

    with fig_col2:
        st.markdown("### Histograma de Intensidad Lumínica")
        if luxData.empty:
            st.write("No hay datos registrados por el momento")
        else:
            histogram_chart = px.histogram(
                luxData,
                x='dato',
                nbins=20,
                title="Distribución de LUX",
                labels={'dato': 'LUX (lx)'}
            )
            histogram_chart.update_traces(marker_color='yellow') 

           
            st.plotly_chart(histogram_chart, use_container_width=True, key=f'Lhistogram_chart_{iteration}')

def main():
    st.title("Estatus Actual de la Estación:")

    placeholder = st.empty()
    iteration = 0 

    while True:
        clean_temperature_data()
        clean_humidity_data()
        clean_lux_data()


        temperatureData = TemperatureData()
        humidityData = HumidityData()
        gasData = GasData()
        co2Data = Co2Data()
        luxData = LuxData()

        

        with placeholder.container():
            metrics(humidityData, temperatureData, luxData)
            st.markdown("---")
            Tgraphs(temperatureData, iteration)
            Hgraphs(humidityData, iteration)
            Ggraphs(gasData, iteration)
            Cgraphs(co2Data, iteration)
            Lgraphs(luxData, iteration)
            

        time.sleep(5)
        iteration += 1

main()
