from typing import Any, Dict

import requests
import streamlit as st

BASE_URL: str = "http://127.0.0.1:8000/api/contacts"

COUNTRY_FLAGS: Dict[str, str] = {
    "COL": "https://flagcdn.com/co.svg", "EEUU": "https://flagcdn.com/us.svg",
    "CAN": "https://flagcdn.com/ca.svg", "CHI": "https://flagcdn.com/cn.svg",
    "JAP": "https://flagcdn.com/jp.svg", "ALE": "https://flagcdn.com/de.svg",
    "RUI": "https://flagcdn.com/gb.svg", "FRA": "https://flagcdn.com/fr.svg",
    "IND": "https://flagcdn.com/in.svg", "ITA": "https://flagcdn.com/it.svg",
    "BRA": "https://flagcdn.com/br.svg", "RUS": "https://flagcdn.com/ru.svg",
    "COR": "https://flagcdn.com/kr.svg", "AUS": "https://flagcdn.com/au.svg",
    "ESP": "https://flagcdn.com/es.svg", "MEX": "https://flagcdn.com/mx.svg",
    "PBA": "https://flagcdn.com/nl.svg", "SUI": "https://flagcdn.com/ch.svg",
    "TUR": "https://flagcdn.com/tr.svg", "ARA": "https://flagcdn.com/sa.svg",
    "SIN": "https://flagcdn.com/sg.svg"
}


def render_directory() -> None:
    """Renders the comprehensive contacts directory table interface inside Streamlit.
    
    Fetches remote records from the core API, processes structural filters based on user
    sub-string queries, applies formatting sanitization to block Markdown syntax breakdown,
    and exposes navigation routines alongside inline administrative management buttons.

    Returns:
        None
    """
    st.title("📋 Directorio General de Contactos")
    
    if st.button("⬅️ Volver al Panel Principal", key="btn_back_home"):
        st.session_state.page = "home"
        st.rerun()
        
    st.markdown("---")
    
    try:
        response: requests.Response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            st.error("No se pudieron recuperar los contactos del servidor.")
            return
        contacts_list: Any = response.json()
    except Exception as e:
        st.error(f"Error de comunicación con el backend: {e}")
        return

    if not contacts_list:
        st.info("📂 El directorio está vacío.")
        return

    search_query: str = st.text_input("🔍 Filtrar tabla...", placeholder="Escriba aquí...")
    st.markdown("<br>", unsafe_allow_html=True)

    # Definición de columnas con saltos de línea para evitar exceder los 120 caracteres
    columns_sizes = [0.5, 1.5, 2.5, 1.2, 2.3, 2.0]
    header_col1, header_col2, header_col3, header_col4, header_col5, header_col6 = st.columns(columns_sizes)
    
    with header_col1:
        st.markdown("**#**")
    with header_col2:
        st.markdown("**Cédula / ID**")
    with header_col3:
        st.markdown("**Nombre Completo**")
    with header_col4:
        st.markdown("**País**")
    with header_col5:
        st.markdown("**Teléfono**")
    with header_col6:
        st.markdown("**Acciones**")
    st.markdown("<hr style='margin: 8px 0; border: 1px solid #CBD5E1;'>", unsafe_allow_html=True)

    visible_row_index: int = 1
    for record in contacts_list:
        if not isinstance(record, dict): 
            continue
        
        contact_id: str = str(record.get("id", ""))
        full_name: str = record.get("full_name", "Sin Nombre")
        country_iso: str = str(record.get("country", "COL")).upper()
        phone_string: str = record.get("phone_number", "Sin Número")
        
        if search_query:
            low: str = search_query.lower()
            if low not in full_name.lower() and low not in phone_string and low not in contact_id.lower() and low not in country_iso.lower():
                continue

        flag_url: str = COUNTRY_FLAGS.get(country_iso, "https://flagcdn.com/un.svg")
        
        row_col1, row_col2, row_col3, row_col4, row_col5, row_col6 = st.columns([0.5, 1.5, 2.5, 1.2, 2.3, 2.0])
        
        with row_col1: 
            st.write(visible_row_index)
        with row_col2: 
            st.code(contact_id)
        with row_col3: 
            full_name_limpio: str = full_name.strip()
            st.markdown(f"**{full_name_limpio}**")
        with row_col4: 
            st.markdown(f"""
                <p style='margin-top:3px;'>
                    <img src="{flag_url}" width="18" style="border-radius:1px; margin-right:4px; vertical-align:middle;"/>
                    <code style="font-size:0.85rem;">{country_iso}</code>
                </p>
            """, unsafe_allow_html=True)
        with row_col5: 
            st.markdown(f"`{phone_string}`")
        with row_col6:
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("✏️", key=f"tbl_edit_{contact_id}_{visible_row_index}"):
                    st.session_state.editing_contact_id = contact_id
                    st.session_state.editing_contact_name = full_name
                    st.session_state.page = "update_page"
                    st.rerun()
            with act_col2:
                if st.button("🗑️", key=f"tbl_del_{contact_id}_{visible_row_index}"):
                    try:
                        res: requests.Response = requests.delete(f"{BASE_URL}/{contact_id}")
                        if res.status_code in [200, 204]:
                            st.rerun()
                        else:
                            st.error(f"Error al eliminar: Código {res.status_code}")
                    except Exception as ex:
                        st.error(f"Error de red: {ex}")
                        
        st.markdown("<hr style='margin: 4px 0; border: 0.5px solid #F1F5F9;'>", unsafe_allow_html=True)
        visible_row_index += 1