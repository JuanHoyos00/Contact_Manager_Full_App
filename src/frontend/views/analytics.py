from typing import Any, Dict

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

BASE_URL: str = "http://127.0.0.1:8000/api/contacts"


def render_analytics() -> None:
    """Renders metric counters and graphical statistical distribution layouts based on backend metrics.

    Fetches the contacts dataset from the API, evaluates distribution properties,
    and renders interactive metrics and charts inside the Streamlit context view.

    Returns:
        None
    """
    st.title("📊 Panel Estadístico del Sistema")
    st.markdown("Análisis demográfico cuantitativo de los contactos almacenados en Supabase.")
    
    if st.button("⬅️ Volver al Panel Principal", key="btn_analytics_back"):
        st.session_state.page = "home"
        st.rerun()
        
    st.markdown("---")
    
    try:
        response: requests.Response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            st.error("No se pudieron extraer métricas del servidor.")
            return
        
        contacts_list: Any = response.json()
        contacts_list = contacts_list.get("data", contacts_list) if isinstance(contacts_list, dict) else contacts_list
    except Exception as e:
        st.error(f"Error de red con el backend: {e}")
        return

    if not contacts_list or len(contacts_list) == 0:
        st.info("📊 No hay suficientes datos para generar gráficos estadísticos. Registre contactos primero.")
        return

    total_records: int = len(contacts_list)
    st.metric(label="Total Contactos Registrados", value=total_records, delta="Activos")
    
    country_distribution: Dict[str, int] = {}
    for record in contacts_list:
        if isinstance(record, dict):
            country_name: str = record.get("country", "UNK").upper()
            country_distribution[country_name] = country_distribution.get(country_name, 0) + 1

    chart_data: pd.DataFrame = pd.DataFrame({
        "País": list(country_distribution.keys()),
        "Cantidad de Contactos": list(country_distribution.values())
    })

    st.markdown("<br>### 🗺️ Distribución de Contactos por País", unsafe_allow_html=True)
    
    fig: px.bar = px.bar(
        chart_data, 
        x="País", 
        y="Cantidad de Contactos",
        color="País",
        text_auto=True,
        title="Volumen de Cuentas por Indicativo Regional",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)