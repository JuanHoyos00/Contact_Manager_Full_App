from typing import Dict

import requests
import streamlit as st

BASE_URL: str = "http://127.0.0.1:8000/api/contacts"


def render_update_page() -> None:
    """Renders the phone number modification interface within the Streamlit context.

    Extracts session state markers to determine target user identity boundaries, 
    evaluates format digit compliance for constraints verification, and dispatches
    the network mutation sequences toward the persistent backend storage router.

    Returns:
        None
    """
    st.title("✏️ Actualizar Número de Teléfono")
    st.markdown("Modifique el número telefónico del contacto seleccionado de forma directa.")
    st.markdown("---")
    
    target_id: str = st.session_state.get("editing_contact_id", "")
    target_name: str = st.session_state.get("editing_contact_name", "Contacto Manual")

    if not target_id:
        st.warning("⚠️ No se ha seleccionado ningún contacto desde el directorio.")
        target_id = st.text_input("Ingrese la Cédula / ID manualmente:")
    else:
        st.info(f"👤 **Contacto:** {target_name} | 🆔 **ID/Cédula:** {target_id}")

    new_phone: str = st.text_input("Ingrese el NUEVO número de teléfono (solo dígitos):", placeholder="Ej: 3217654321")
    
    st.markdown("---")
    col_submit, col_cancel = st.columns([1, 4])
    
    with col_submit:
        if st.button("⚡ Ejecutar Actualización", type="primary"):
            if target_id and new_phone:
                if not new_phone.isdigit():
                    st.error("❌ El número telefónico debe contener únicamente dígitos numéricos.")
                    return
                try:
                    payload: Dict[str, str] = {"id": target_id, "new_number": new_phone}
                    response: requests.Response = requests.put(f"{BASE_URL}/update-number", json=payload)
                    
                    if response.status_code == 200:
                        st.toast("¡Número modificado con éxito en la base de datos!", icon="✅")
                        st.session_state.page = "directory"
                        st.rerun()
                    else:
                        st.error(f"Error: {response.json().get('detail', 'No se pudo realizar el cambio')}")
                except Exception as e:
                    st.error(f"Fallo de conexión con el backend: {e}")
            else:
                st.warning("Por favor ingrese el nuevo número.")
                
    with col_cancel:
        if st.button("❌ Cancelar y Volver"):
            st.session_state.page = "directory"
            st.rerun()