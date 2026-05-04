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
    .titulo-principal { color: #003366; text-align: center; font-weight: bold; margin-top: -20px; }
    .stButton>button {
        background-color: #003366;
        color: #FFD700;
        border-radius: 10px;
        border: 2px solid #FFD700;
        font-weight: bold;
        font-size: 20px;
        width: 100%;
    }
    .logo-container { display: flex; justify-content: center; margin-bottom: 20px; }
    .stRadio label, .stSelectbox label { font-size: 20px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE LÓGICA ---
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
    st.session_state.finalizado = False

# --- NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# --- VISTA: INICIO ---
if st.session_state.pagina == "inicio":
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    # CARGA LOCAL: El archivo debe estar en la misma carpeta
    try:
        st.image("Gemini_Generated_Image_51wlso51wlso51wl (1)_2.png", width=450)
    except Exception:
        st.error("⚠️ No se encontró el archivo del logo. Verifica que se llame 'Gemini_Generated_Image_51wlso51wlso51wl (1)_2.png'")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h1 class='titulo-principal'>Matemática Esquemática</h1>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("""
    Bienvenido al entorno de aprendizaje visual del profesor **Fabio Molano**.
    
    Aquí transformamos ecuaciones en estructuras comprensibles para dominar el lenguaje del cambio.
    """)
    
    if st.button("Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

# --- VISTA: DESPEJE ---
elif st.session_state.pagina == "despeje":
    with st.sidebar:
        try:
            st.image("Gemini_Generated_Image_51wlso51wlso51wl (1)_2.png", use_container_width=True)
        except: pass
        st.markdown("### Matemática Esquemática")
        if st.button("🏠 Inicio"):
            st.session_state.pagina = "inicio"
            st.rerun()

    if 'contador_ejercicios' not in st.session_state:
        st.session_state.contador_ejercicios = 0
        preparar_nuevo_ejercicio()

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    st.title("Módulo de Despeje")
    st.info(f"**Ecuación:** {fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}")

    # Análisis de Pendiente e Intercepto (Simplificado para prueba)
    m = Fraction(-a, b)
    inter = Fraction(c, b)
    
    st.subheader("Análisis de la Recta")
    st.latex(rf"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}")
    
    col1, col2 = st.columns(2)
    col1.metric("Pendiente (m)", str(m))
    col2.metric("Intercepto (b)", str(inter))

    # Gráfico
    x = np.linspace(-10, 10, 20)
    y = float(m) * x + float(inter)
    st.line_chart(pd.DataFrame({'x': x, 'y': y}).set_index('x'))

    if st.button("Siguiente Ejercicio"):
        st.session_state.contador_ejercicios += 1
        preparar_nuevo_ejercicio()
        st.rerun()
