import streamlit as st
import random
import pandas as pd
import numpy as np
from fractions import Fraction

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Matemática Esquemática - Fabio Molano", layout="centered")

# --- ESTILOS PERSONALIZADOS REFINADOS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    
    /* Título más grande y con ajuste de posición hacia la izquierda */
    .titulo-esquemática { 
        color: #002D62 !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 52px !important; /* Aumentado para mayor impacto */
        margin-top: 5px !important;
        margin-bottom: 30px !important;
        margin-left: -15px !important; /* Desplazamiento a la izquierda para centrar con el logo */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        display: block;
        letter-spacing: -1px; /* Mejora la elegancia de la fuente grande */
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

# --- ARCHIVOS ---
NOMBRE_LOGO = "logo fabio faraon.png"

# --- LÓGICA DE NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# --- VISTA: INICIO ---
if st.session_state.pagina == "inicio":
    # Contenedor del Logo
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image(NOMBRE_LOGO, width=480)
    except:
        st.error(f"Asegúrate de subir '{NOMBRE_LOGO}' a GitHub")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Título ajustado visualmente
    st.markdown('<span class="titulo-esquemática">Matemática Esquemática</span>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<span class="texto-centrado">Bienvenido al entorno visual del profesor <b>Fabio Molano</b>.</span>', unsafe_allow_html=True)
    st.markdown('<span class="texto-centrado">Aquí transformamos ecuaciones en estructuras comprensibles para dominar el lenguaje del cambio.</span>', unsafe_allow_html=True)
    
    st.write(" ") 
    
    if st.button("🚀 Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

# --- VISTA: DESPEJE (Estructura base) ---
elif st.session_state.pagina == "despeje":
    st.title("Módulo de Despeje")
    st.write("Configurando ejercicios de trigonometría y álgebra...")
    if st.button("Volver al Inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()
