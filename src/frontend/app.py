
import streamlit as st
from styles import apply_professional_theme
from views.analytics import render_analytics
from views.directory import render_directory
from views.form import render_contact_form
from views.update_phone import render_update_page

st.set_page_config(page_title="Contact Manager Pro", page_icon="🔹", layout="wide")


def render_home() -> None:
    """Renders the main dashboard menu exposing the interactive operational capabilities.

    Dispatches session configuration payloads towards target pages and routes system
    actions categorized under transactional commands, structural queries, and statistical logs.

    Returns:
        None
    """
    apply_professional_theme()
    st.title("🔹 Contact Manager Pro Operations Menu")
    st.markdown("Seleccione el método del Servicio de Negocio que desea ejecutar:")
    st.markdown("---")
    
    def move_to_form(action_type: str) -> None:
        """Helper callback subroutine to update session state routing keys for form handling."""
        st.session_state.form_action = action_type
        st.session_state.page = "form_page"
        st.rerun()

    st.markdown("### 📥 Métodos de Escritura (Commands)")
    if st.button("➕ add_contact() — Crear Nuevo Registro", use_container_width=True):
        move_to_form("create")
        
    if st.button("✏️ update_contact_number_by_id() — Actualizar Número de un Contacto", use_container_width=True):
        st.session_state.editing_contact_name = ""  
        st.session_state.page = "update_page"
        st.rerun()
        
    st.markdown("---")
    st.markdown("### 🔍 Métodos de Consulta Directa (Queries)")
    if st.button("🆔 get_contact_by_id() — Buscar un Registro por Cédula", use_container_width=True):
        move_to_form("get_id")
    if st.button("📱 get_contact_by_number() — Buscar un Registro por Teléfono", use_container_width=True):
        move_to_form("get_phone")

    st.markdown("---")
    st.markdown("### 📤 Métodos de Eliminación Fuerte (Deletions)")
    if st.button("🗑️ delete_contact_by_id() — Remover Registro por Cédula", use_container_width=True):
        move_to_form("delete_id")
    if st.button("🚨 delete_contact_by_number() — Remover Registro por Teléfono", use_container_width=True):
        move_to_form("delete_phone")
        
    st.markdown("---")
    st.markdown("### 📋 Vistas de Reportes y Módulos Estadísticos")
    if st.button("👥 get_all_contacts() — Ver Directorio General (Formato Tabla)", use_container_width=True):
        st.session_state.page = "directory"
        st.rerun()
    if st.button("📊 get_contact_analytics() — Ver Panel Estadístico del Sistema", use_container_width=True):
        st.session_state.page = "analytics"
        st.rerun()


if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    render_home()
elif st.session_state.page == "directory":
    render_directory()
elif st.session_state.page == "form_page":
    render_contact_form()
elif st.session_state.page == "analytics":
    render_analytics()
elif st.session_state.page == "update_page":
    render_update_page()