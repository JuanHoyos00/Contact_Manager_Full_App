from typing import Any, Dict, List

import requests
import streamlit as st

BASE_URL: str = "http://127.0.0.1:8000/api/contacts"

BACKEND_COUNTRIES: Dict[str, Dict[str, Any]] = {
    "COL": {"code": 57, "flag": "🇨🇴", "label": "COL (Colombia)"},
    "EEUU": {"code": 1, "flag": "🇺🇸", "label": "EEUU (United States)"},
    "CAN": {"code": 1, "flag": "🇨🇦", "label": "CAN (Canada)"},
    "CHI": {"code": 86, "flag": "🇨🇳", "label": "CHI (China)"},
    "JAP": {"code": 81, "flag": "🇯🇵", "label": "JAP (Japan)"},
    "ALE": {"code": 49, "flag": "🇩🇪", "label": "ALE (Germany)"},
    "RUI": {"code": 44, "flag": "🇬🇧", "label": "RUI (United Kingdom)"},
    "FRA": {"code": 33, "flag": "🇫🇷", "label": "FRA (France)"},
    "IND": {"code": 91, "flag": "🇮🇳", "label": "IND (India)"},
    "ITA": {"code": 39, "flag": "🇮🇹", "label": "ITA (Italy)"},
    "BRA": {"code": 55, "flag": "🇧🇷", "label": "BRA (Brazil)"},
    "RUS": {"code": 7, "flag": "🇷🇺", "label": "RUS (Russia)"},
    "COR": {"code": 82, "flag": "🇰🇷", "label": "COR (South Korea)"},
    "AUS": {"code": 61, "flag": "🇦🇺", "label": "AUS (Australia)"},
    "ESP": {"code": 34, "flag": "🇪🇸", "label": "ESP (Spain)"},
    "MEX": {"code": 52, "flag": "🇲🇽", "label": "MEX (Mexico)"},
    "PBA": {"code": 31, "flag": "🇳🇱", "label": "PBA (Netherlands)"},
    "SUI": {"code": 41, "flag": "🇨🇭", "label": "SUI (Switzerland)"},
    "TUR": {"code": 90, "flag": "🇹🇷", "label": "TUR (Turkey)"},
    "ARA": {"code": 966, "flag": "🇸🇦", "label": "ARA (Saudi Arabia)"},
    "SIN": {"code": 65, "flag": "🇸🇬", "label": "SIN (Singapore)"}
}


def render_contact_form() -> None:
    """Renders dynamic forms based on the current action state defined by the user.

    Processes mutations, point queries, and deletion workflows, while matching
    the exact structural transmission payload requirements of the API router layer.

    Returns:
        None
    """
    current_action: str = st.session_state.get("form_action", "create")
    country_options: List[str] = list(BACKEND_COUNTRIES.keys())
    
    if st.button("⬅️ Volver al Menú de Operaciones", key="btn_form_back"):
        st.session_state.selected_contact = None
        st.session_state.page = "home"
        st.rerun()
        
    st.markdown("---")

    if current_action in ["create", "edit"]:
        is_edit: bool = current_action == "edit"
        st.title("✏️ Actualizar Contacto" if is_edit else "➕ Registrar Nuevo Contacto (add_contact)")
        
        default_id: str = ""
        default_name: str = ""
        default_last_name: str = ""
        default_phone: str = ""
        default_country_index: int = country_options.index("COL")
        
        if is_edit and st.session_state.get("selected_contact"):
            record: Any = st.session_state.selected_contact
            p_node: Any = record.get("person", {}) if isinstance(record, dict) else getattr(record, "person", {})
            c_node: Any = record.get("country", {}) if isinstance(record, dict) else getattr(record, "country", {})
            n_node: Any = record.get("number", {}) if isinstance(record, dict) else getattr(record, "number", {})
            
            default_id = str(p_node.get("id", "")) if isinstance(p_node, dict) else str(getattr(p_node, "id", ""))
            default_name = p_node.get("name", "") if isinstance(p_node, dict) else getattr(p_node, "name", "")
            default_last_name = p_node.get("last_name", "") if isinstance(p_node, dict) else getattr(p_node, "last_name", "")
            default_phone = n_node.get("value", "") if isinstance(n_node, dict) else str(n_node)
            
            c_str: str = c_node.get("name", "COL") if isinstance(c_node, dict) else str(c_node)
            if c_str.upper() in country_options:
                default_country_index = country_options.index(c_str.upper())

        col_1, col_2 = st.columns(2)
        with col_1:
            input_id: str = st.text_input("Identification Number / Cédula*", value=default_id, disabled=is_edit, placeholder="Ej. 10203040")
            input_name: str = st.text_input("First Name / Nombre*", value=default_name, placeholder="Ej. Jaime")
            input_last_name: str = st.text_input("Last Name / Apellido", value=default_last_name, placeholder="Ej. Giraldo")
        with col_2:
            input_country: str = st.selectbox(
                "Country / País*", options=country_options, index=default_country_index,
                format_func=lambda k: f"{BACKEND_COUNTRIES[k]['flag']} {BACKEND_COUNTRIES[k]['label']}"
            )
            input_phone: str = st.text_input("Phone Number / Teléfono*", value=default_phone, placeholder="Ej. 3126206120")

        if st.button("💾 Guardar Cambios" if is_edit else "🚀 Crear Registro", key="btn_execute_save"):
            if not input_id.strip() or not input_name.strip() or not input_phone.strip():
                st.error("❌ Los campos Cédula, Nombre y Teléfono son obligatorios.")
                return
            
            flat_payload: Dict[str, Any] = {
                "id": input_id.strip(),
                "name": input_name.strip(),
                "last_name": input_last_name.strip(),
                "country_name": input_country,
                "country_code": int(BACKEND_COUNTRIES[input_country]["code"]),
                "number_": input_phone.strip()
            }
            
            try:
                if is_edit:
                    response: requests.Response = requests.put(f"{BASE_URL}/update-number", json={"id": input_id.strip(), "new_number": input_phone.strip()})
                else:
                    response = requests.post(f"{BASE_URL}/", json=flat_payload)
                    
                if response.status_code in [200, 201]:
                    st.success("¡Operación realizada con éxito en Supabase!")
                    st.session_state.selected_contact = None
                    st.session_state.page = "directory"
                    st.rerun()
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as ex:
                st.error(f"Fallo de conexión: {ex}")

    elif current_action in ["get_id", "get_phone"]:
        is_id: bool = current_action == "get_id"
        st.title("🔍 get_contact_by_id()" if is_id else "📱 get_contact_by_number()")
        
        search_input: str = st.text_input(
            "Ingrese el ID de la Persona (Cédula)*" if is_id else "Ingrese el Número de Teléfono*",
            placeholder="Ej. 10203040" if is_id else "Ej. 3126206120"
        )
        
        if st.button("Buscar Registro", key="btn_trigger_get"):
            if not search_input.strip():
                st.error("Por favor ingrese un parámetro de búsqueda.")
                return
            try:
                url_path: str = f"{search_input.strip()}" if is_id else f"number/{search_input.strip()}"
                response: requests.Response = requests.get(f"{BASE_URL}/{url_path}")
                
                if response.status_code == 200:
                    data: Any = response.json()
                    st.success("¡Registro encontrado con éxito!")
                    st.json(data)
                else:
                    st.error(f"No se encontró ningún registro coincidente. Código: {response.status_code}")
            except Exception as ex:
                st.error(f"Error al conectar con la API: {ex}")

    elif current_action in ["delete_id", "delete_phone"]:
        is_id: bool = current_action == "delete_id"
        st.title("🗑️ delete_contact_by_id()" if is_id else "🚨 delete_contact_by_number()")
        
        target_input: str = st.text_input(
            "Ingrese la Cédula del contacto a remover*" if is_id else "Ingrese el Teléfono del contacto a remover*",
            placeholder="Ej. 10203040"
        )
        
        if st.button("💥 Confirmar Eliminación", key="btn_trigger_delete_form"):
            if not target_input.strip():
                st.error("El campo es requerido.")
                return
            try:
                url_path: str = f"{target_input.strip()}" if is_id else f"number/{target_input.strip()}"
                response: requests.Response = requests.delete(f"{BASE_URL}/{url_path}")
                if response.status_code in [200, 204]:
                    st.success("¡Contacto eliminado de Supabase exitosamente!")
                else:
                    st.error(f"Error al procesar eliminación. Código: {response.status_code}")
            except Exception as ex:
                st.error(f"Error: {ex}")