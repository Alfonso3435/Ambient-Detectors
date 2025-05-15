import streamlit as st


home_page = st.Page(
    page="views/home.py",
    title="Inicio",
    icon="🌤️",
    default=True,
)

graph_page = st.Page(
    page="views/graph.py",
    title="Panel en Tiempo Real",
    icon="📈"
)

data_page = st.Page(
    page="views/data.py",
    title="Visualización de Lecturas",
    icon="🌐"
)


pg = st.navigation(pages=[home_page, graph_page,data_page ])


pg.run()