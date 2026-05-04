import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Matemática Esquemática - Fabio Molano", layout="centered")

# --- ESTILOS PERSONALIZADOS (AJUSTE FINO DE ALINEACIÓN) ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    
    .titulo-esquemática { 
        color: #002D62 !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 62px !important;
        margin-top: 5px !important;
        margin-bottom: 30px !important;
        /* Desplazamiento acumulado: -200px + -25px = -225px */
        margin-left: -225px !important; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        display: block;
        letter-spacing: -2px;
        white-space: nowrap;
    }
    
    .texto-centrado {
        text-align: center !important;
        font-size: 20px !important;
        color: #333333;
        display: block;
        width: 100%;
    }

    .stButton>button {
        background-color: #002D62 !important;
        color: #FFD700 !important;
        border-radius: 10px;
        border: 2px solid #FFD700;
        font-weight: bold;
        font-size: 22px;
        width: 100%;
        height: 60px;
    }
    
    .logo-container { 
        display: flex; 
        justify-content: center; 
        margin-bottom: 0px;
    }

    hr { margin-top: 0px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- RECURSOS ---
NOMBRE_LOGO = "logo fabio faraon.png" 

if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# --- VISTA: INICIO ---
if st.session_state.pagina == "inicio":
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image(NOMBRE_LOGO, width=480)
    except:
        st.error(f"Verifica que '{NOMBRE_LOGO}' esté en tu repositorio de GitHub.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicación del desplazamiento de -225px
    st.markdown('<span class="titulo-esquemática">Matemática Esquemática</span>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<span class="texto-centrado">Bienvenido al entorno visual del profesor <b>Fabio Molano</b>.</span>', unsafe_allow_html=True)
    st.markdown('<span class="texto-centrado">Aquí transformamos ecuaciones en estructuras comprensibles para dominar el lenguaje del cambio.</span>', unsafe_allow_html=True)
    
    st.write(" ") 
    if st.button("🚀 Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

# --- VISTA: MÓDULO DE DESPEJE ---
elif st.session_state.pagina == "despeje":
    st.title("Módulo de Despeje")
    st.write("Cargando herramientas de modelado matemático...")
    if st.button("Volver al Inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()
