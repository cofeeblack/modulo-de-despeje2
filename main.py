import streamlit as st
import streamlit as st
import random
import pandas as pd
import numpy as np
from fractions import Fraction

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Matemática Esquemática - Fabio Molano", layout="centered")

# --- ESTILOS PERSONALIZADOS (AQUÍ ESTÁ EL CAMBIO) ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    
    /* 1. Título centrado, color azul logo y tamaño ajustado */
    .titulo-esquemática { 
        color: #002D62 !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 42px !important;
        margin-top: 0px !important;
        margin-bottom: 30px !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        display: block;
    }
    
    /* 2. Centrado de los textos de bienvenida */
    .texto-centrado {
        text-align: center !important;
        font-size: 20px !important;
        color: #333333;
        display: block;
        width: 100%;
    }

    /* 3. Botón con el azul del logo */
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
    
    /* 4. Contenedor del logo */
    .logo-container { 
        display: flex; 
        justify-content: center; 
        margin-bottom: 10px;
    }

    hr { margin-top: 0px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- ARCHIVOS ---
NOMBRE_LOGO = "logo fabio faraon.png"

# --- FUNCIONES ---
def fmt_c(n, var="", incluir_mas=False):
    if isinstance(n, Fraction):
        signo = "+" if incluir_mas and n > 0 else ""
        if n.denominator == 1: return fmt_c(n.numerator, var, incluir_mas)
        return f"{signo}{n}{var}"
    signo = "+" if incluir_mas and n > 0 else ""
    if n == 1: return f"{signo}{var}" if var else f"{signo}1"
    if n == -1: return f"-{var}" if var else "-1"
    if n == 0: return ""
    return f"{signo}{n}{var}"

def preparar_nuevo_ejercicio():
    st.session_state.paso = 1
    st.session_state.a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    st.session_state.b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    st.session_state.c = random.randint(5, 25)
    st.session_state.opciones_paso3 = []
    st.session_state.opciones_paso5 = []
    st.session_state.error_en_actual = False
    st.session_state.finalizado = False

# --- LÓGICA DE NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# --- VISTA: INICIO ---
if st.session_state.pagina == "inicio":
    # Logo
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image(NOMBRE_LOGO, width=480)
    except:
        st.error(f"Logo no encontrado: {NOMBRE_LOGO}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Título (Cambiado a azul #002D62)
    st.markdown('<span class="titulo-esquemática">Matemática Esquemática</span>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Textos centrados
    st.markdown('<span class="texto-centrado">Bienvenido al entorno visual del profesor <b>Fabio Molano</b>.</span>', unsafe_allow_html=True)
    st.markdown('<span class="texto-centrado">Aquí transformamos ecuaciones en estructuras comprensibles para dominar el lenguaje del cambio.</span>', unsafe_allow_html=True)
    
    st.write(" ") 
    
    if st.button("🚀 Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

# --- VISTA: DESPEJE (Omitido el resto para que pruebes primero el cambio visual) ---
elif st.session_state.pagina == "despeje":
    st.title("Módulo en construcción")
    if st.button("Volver"):
        st.session_state.pagina = "inicio"
        st.rerun()
