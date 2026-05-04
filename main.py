import streamlit as st
import random
import pandas as pd
import numpy as np
from fractions import Fraction

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Matemática Esquemática - Fabio Molano", layout="centered")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .titulo-principal { color: #003366; text-align: center; font-weight: bold; }
    .stButton>button {
        background-color: #003366;
        color: #FFD700;
        border-radius: 10px;
        border: 2px solid #FFD700;
        font-weight: bold;
        width: 100%;
    }
    .logo-container { display: flex; justify-content: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# URL del logo (sustituir por la ruta local si es necesario)
LOGO_URL = "https://tu-enlace-aqui.com/logo_ojo_aureo.png" 

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

# --- GESTIÓN DE NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# --- VISTA: INICIO / INTRODUCCIÓN ---
if st.session_state.pagina == "inicio":
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("https://i.imgur.com/vHq4R7p.png", width=400) # Reemplazar por tu archivo
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1 class='titulo-principal'>Matemática Esquemática</h1>", unsafe_allow_html=True)
    st.write("---")
    st.write("Bienvenido al entorno de aprendizaje visual del profesor **Fabio Molano**.")
    st.write("Aquí transformamos ecuaciones en estructuras comprensibles para dominar el lenguaje del cambio.")
    
    if st.button("Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

# --- VISTA: MÓDULO DE DESPEJE ---
elif st.session_state.pagina == "despeje":
    # Sidebar con Logo y Título
    with st.sidebar:
        st.image("https://i.imgur.com/vHq4R7p.png", use_container_width=True)
        st.markdown("### Matemática Esquemática")
        if st.button("Volver al Inicio"):
            st.session_state.pagina = "inicio"
            st.rerun()

    # Inicialización de lógica de ejercicios
    if 'contador_ejercicios' not in st.session_state:
        st.session_state.contador_ejercicios = 0
        st.session_state.puntos_totales = 0
        preparar_nuevo_ejercicio()

    # (Aquí va toda la lógica del Módulo de Despeje anterior...)
    # ... [Paso 1 a 4] ...
    
    # --- NOVEDAD: PASO 5 CON ANÁLISIS GRÁFICO ---
    if st.session_state.get('paso') == 5:
        a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
        m = Fraction(-a, b)
        inter = Fraction(c, b)
        
        st.subheader("Paso 5: Análisis Esquemático")
        st.latex(rf"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Pendiente (m):** {m}")
            st.write("Indica la inclinación de la recta.")
        with col2:
            st.success(f"**Intercepto (b):** {inter}")
            st.write("Punto donde cruza el eje Y.")

        # Gráfico dinámico
        x_vals = np.linspace(-10, 10, 100)
        y_vals = float(m) * x_vals + float(inter)
        df_grafico = pd.DataFrame({'x': x_vals, 'y': y_vals})
        
        st.line_chart(df_grafico.set_index('x'))
        
        if st.button("Finalizar Ejercicio"):
            st.session_state.contador_ejercicios += 1
            preparar_nuevo_ejercicio()
            st.rerun()
