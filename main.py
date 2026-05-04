import streamlit as st
import random
import pandas as pd
import numpy as np
from fractions import Fraction

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Matemática Esquemática - Fabio Molano", layout="centered")

# --- ESTILOS PERSONALIZADOS (AJUSTE DE PROPORCIÓN Y POSICIÓN) ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    
    /* Título con aumento proporcional y desplazamiento mayor a la izquierda */
    .titulo-esquemática { 
        color: #002D62 !important; 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 62px !important; /* Aumento proporcional a la escala anterior */
        margin-top: 5px !important;
        margin-bottom: 30px !important;
        margin-left: -35px !important; /* Desplazamiento acentuado a la izquierda */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        display: block;
        letter-spacing: -2px; /* Ajuste de interletrado para fuentes grandes */
        white-space: nowrap; /* Evita que el texto salte de línea por el tamaño */
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
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image(NOMBRE_LOGO, width=480)
    except:
        st.error(f"Asegúrate de que el archivo se llame '{NOMBRE_LOGO}' en tu repositorio.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicación del nuevo estilo escalado
    st.markdown('<span class="titulo-esquemática">Matemática Esquemática</span>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    st.markdown('<span class="texto-centrado">Bienvenido al entorno visual del profesor <b>Fabio Molano</b>.</span>', unsafe_allow_html=True)
    st.markdown('<span class="texto-centrado">Aquí transformamos ecuaciones en estructuras comprensibles para dominar el lenguaje del cambio.</span>', unsafe_allow_html=True)
    
    st.write(" ") 
    
    if st.button("🚀 Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

# --- VISTA: DESPEJE ---
elif st.session_state.pagina == "despeje":
    st.title("Módulo de Despeje")
    st.write("Cargando ejercicios interactivos...")
    if st.button("Volver al Inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()
