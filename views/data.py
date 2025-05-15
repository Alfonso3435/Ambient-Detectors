import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime, time, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

load_dotenv()

def connect():
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
        st.error(f"Error al conectar a la base de datos: {e}")
        return None

def fetch_data(query):
    connection = connect()
    if connection:
        try:
            data = pd.read_sql(query, connection)
            data['fecha'] = pd.to_datetime(data['fecha'])
            return data
        except Error as e:
            st.error(f"Error al obtener datos: {e}")
            return pd.DataFrame()
        finally:
            connection.close()
    else:
        return pd.DataFrame()

def HumidityData():
    return fetch_data("SELECT fecha, dato FROM medicion WHERE id_sensor = '2';")

def TemperatureData():
    return fetch_data("SELECT fecha, dato FROM medicion WHERE id_sensor = '1';")

def GasData():
    return fetch_data("SELECT fecha, dato FROM medicion WHERE id_sensor = '3';")

def Co2Data():
    return fetch_data("SELECT fecha, dato FROM medicion WHERE id_sensor = '4';")

def LuxData():
    return fetch_data("SELECT fecha, dato FROM medicion WHERE id_sensor = '5';")

def display_statistics(data, columns):
    st.subheader("Estadísticas")
    st.write(f"Número de registros: {len(data)}")
    if not data.empty:
        st.write(f"Rango de fechas: {data['fecha'].min().strftime('%d %B %Y')} a {data['fecha'].max().strftime('%d %B %Y')}")
        
        for column in columns:
            if column != 'fecha':
                st.write(f"{column.capitalize()}:")
                st.write(f"  - Promedio: {data[column].mean():.2f}")
                st.write(f"  - Mínimo: {data[column].min():.2f}")
                st.write(f"  - Máximo: {data[column].max():.2f}")
    else:
        st.write("No hay datos disponibles para mostrar estadísticas.")

def display_charts(data, columns, dataset_name):
    if data.empty:
        st.warning("No hay datos disponibles para mostrar gráficos.")
        return

    st.subheader("Gráficos")
    chart_data = data.set_index('fecha')
    
    data_columns = [col for col in columns if col != 'fecha']
    
    color_map = {
        "Sensor DHT11, Temperatura": "red",
        "Sensor DHT11, Humedad": "blue",
        "Sensor MQ135, Calidad de Aire": "green",
        "Sensor MQ135, CO2": "orange",
        "Sensor BH1750, Intensidad Lumínica": "yellow"
    }
    
    line_color = color_map.get(dataset_name, "gray") 
    
    if len(data_columns) == 1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=chart_data.index, y=chart_data[data_columns[0]], 
                                 mode='lines', name=data_columns[0].capitalize(),
                                 line=dict(color=line_color)))
        fig.update_layout(title=f"{dataset_name} a lo largo del tiempo",
                          xaxis_title="Fecha",
                          yaxis_title=data_columns[0].capitalize())
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        fig = make_subplots(rows=len(data_columns), cols=1, shared_xaxes=True, vertical_spacing=0.1)
        
        for i, column in enumerate(data_columns, start=1):
            fig.add_trace(
                go.Scatter(x=chart_data.index, y=chart_data[column], name=column.capitalize(),
                           line=dict(color=line_color)),
                row=i, col=1
            )
            fig.update_yaxes(title_text=column.capitalize(), row=i, col=1)
        
        fig.update_layout(height=300*len(data_columns), title_text=f"{dataset_name} a lo largo del tiempo", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

def main():
    st.title("Datasets de la Estación Meteorológica")
    tData = TemperatureData()
    hData = HumidityData()
    gData = GasData()
    cData = Co2Data()
    lData = LuxData()

    datasets = {
        "Sensor DHT11, Temperatura": {"data": tData, "columns": ['fecha', 'dato']},
        "Sensor DHT11, Humedad": {"data": hData, "columns": ['fecha', 'dato']},
        "Sensor MQ135, Calidad de Aire": {"data": gData, "columns": ['fecha', 'dato']},
        "Sensor MQ135, CO2": {"data": cData, "columns": ['fecha', 'dato']},
        "Sensor BH1750, Intensidad Lumínica": {"data": lData, "columns": ['fecha', 'dato']},
    }
    
    selected_dataset = st.selectbox("Elige un dataset", list(datasets.keys()))
    
    if selected_dataset:
        st.subheader(f"Visualizando: {selected_dataset}")
        
        if datasets[selected_dataset]['data'].empty:
            st.warning(f"No hay datos disponibles para el {selected_dataset}.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Fecha de inicio", 
                                           min(datasets[selected_dataset]['data']['fecha']).date(),
                                           min_value=min(datasets[selected_dataset]['data']['fecha']).date(),
                                           max_value=max(datasets[selected_dataset]['data']['fecha']).date(),
                                           format="DD/MM/YYYY")
            with col2:
                end_date = st.date_input("Fecha de fin", 
                                         max(datasets[selected_dataset]['data']['fecha']).date(),
                                         min_value=min(datasets[selected_dataset]['data']['fecha']).date(),
                                         max_value=max(datasets[selected_dataset]['data']['fecha']).date(),
                                         format="DD/MM/YYYY")

            col3, col4 = st.columns(2)
            with col3:
                start_time = st.time_input("Hora de inicio", time(0, 0))
            with col4:
                end_time = st.time_input("Hora de fin", time(23, 59))

            start_datetime = datetime.combine(start_date, start_time)
            end_datetime = datetime.combine(end_date, end_time)

            filtered_data = datasets[selected_dataset]['data'][
                (datasets[selected_dataset]['data']['fecha'] >= start_datetime) &
                (datasets[selected_dataset]['data']['fecha'] <= end_datetime)
            ]

            st.dataframe(filtered_data)

            if not filtered_data.empty:
                display_statistics(filtered_data, datasets[selected_dataset]['columns'])
                display_charts(filtered_data, datasets[selected_dataset]['columns'], selected_dataset)
            else:
                st.warning("No hay datos disponibles para el rango de fechas seleccionado.")


main()