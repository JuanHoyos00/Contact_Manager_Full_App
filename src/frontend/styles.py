import streamlit as st


def apply_professional_theme() -> None:
    """Injects custom CSS styles into the Streamlit app instance.

    Forces a corporate corporate color palette, handles proper font family scaling, 
    custom contact card components styling, and native action button element overrides.

    Returns:
        None
    """
    st.markdown("""
        <style>
        .stApp {
            background-color: #F8FAFC;
        }
        
        h1, h2, h3 {
            color: #1E3A8A !important;
            font-family: 'Segoe UI', system-ui, sans-serif;
            font-weight: 700;
        }
        
        .stMarkdown p {
            color: #334155;
        }

        .contact-card {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-left: 6px solid #2563EB;
            margin-bottom: 15px;
        }
        
        .contact-card h4 {
            margin: 0 0 8px 0 !important;
            color: #1E293B !important;
            font-size: 1.2rem;
        }
        
        .stButton>button {
            background-color: #2563EB !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease-in-out !important;
            width: 100%;
        }
        
        .stButton>button:hover {
            background-color: #1D4ED8 !important;
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3) !important;
            transform: translateY(-1px);
        }
        </style>
    """, unsafe_allow_html=True)