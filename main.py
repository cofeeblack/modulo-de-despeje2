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
    
    /* Título con color exacto del logo y tamaño jerárquico */
    .titulo-esquemática { 
        color: #002D62; 
        text-align: center; 
        font-weight: bold; 
        font-size: 42px; /* Un poco menor que el nombre del logo */
        margin-top: 10px;
        margin-bottom: 20px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Centrado del texto descriptivo */
    .texto-centrado {
        text-align: center;
        font-size: 20px !important;
        color: #333333;
    }

    .stButton>button {
        background-color: #002D62;
        color: #FFD700;
        border-radius: 10px;
        border: 2px solid #FFD700;
        font-weight: bold;
        font-size: 20px;
        width: 100%;
    }
    
    .logo-container { display: flex; justify-content: center; align-items: center; }
    
    .stRadio label, .stSelectbox label { font-size: 22px !important; font-family: 'Courier New', monospace; }
    
    .op-table {
        margin-left: auto;
        margin-right: auto;
        font-family: 'Courier New', monospace;
        font-size: 24px;
        border-collapse: collapse;
    }
    .op-table td { padding: 0px 12px; text-align: center; }
    .red-text { color: #e74c3c; font-weight: bold; }
    .linea-suma { border-top: 2px solid black; }
    </style>
    """, unsafe_allow_html=True)

# --- NOMBRE DEL ARCHIVO DEL LOGO ---
NOMBRE_LOGO = "logo fabio faraon.png"

# --- FUNCIONES DE APOYO ---
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

def reiniciar_serie():
    st.session_state.clear()

# --- GESTIÓN DE ESTADO ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# --- VISTA 1: INTRODUCCIÓN ---
if st.session_state.pagina == "inicio":
    # Contenedor para el logo centrado
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image(NOMBRE_LOGO, width=480)
    except:
        st.error(f"⚠️ No se encontró el logo '{NOMBRE_LOGO}'")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Título estilizado y centrado
    st.markdown('<h1 class="titulo-esquemática">Matemática Esquemática</h1>', unsafe_allow_html=True)
    
    st.write("---")
    
    # Texto descriptivo centrado
    st.markdown('<p class="texto-centrado">Bienvenido al entorno visual del profesor <b>Fabio Molano</b>.</p>', unsafe_allow_html=True)
    st.markdown('<p class="texto-centrado">Aquí transformamos ecuaciones en estructuras comprensibles para dominar el lenguaje del cambio.</p>', unsafe_allow_html=True)
    
    st.write("") # Espaciador
    
    # El botón ya está configurado para ocupar el ancho completo (centrado por defecto en el layout)
    if st.button("🚀 Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

# --- VISTA 2: MÓDULO DE DESPEJE ---
elif st.session_state.pagina == "despeje":
    with st.sidebar:
        try: st.image(NOMBRE_LOGO, use_container_width=True)
        except: pass
        st.markdown("### Matemática Esquemática")
        if st.button("🏠 Inicio"):
            st.session_state.pagina = "inicio"
            st.rerun()

    if 'contador_ejercicios' not in st.session_state:
        st.session_state.contador_ejercicios = 0
        st.session_state.puntos_totales = 0
        preparar_nuevo_ejercicio()

    if st.session_state.contador_ejercicios >= 10:
        st.header("📊 Resultado Final")
        st.metric("Puntaje Total", f"{st.session_state.puntos_totales}/100")
        st.button("Nueva Serie", on_click=reiniciar_serie)
        st.stop()

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    st.title("Módulo de Despeje")
    st.write(f"**Ejercicio {st.session_state.contador_ejercicios + 1} de 10**")
    st.info(f"**Ecuación Inicial:** {fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}")

    # Lógica de pasos (Paso 1 al 5 omitida por brevedad, se mantiene igual a la anterior)
    # ... [Insertar aquí el código de los pasos 1 a 5 de la respuesta previa] ...
    
    # Muestro solo el final (Paso 5) para confirmar la integración gráfica
    if st.session_state.paso == 5:
        st.subheader("Análisis Gráfico")
        m, inter = Fraction(-a, b), Fraction(c, b)
        st.latex(rf"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}")
        
        col_m, col_b = st.columns(2)
        col_m.metric("Pendiente (m)", str(m))
        col_b.metric("Intercepto (b)", str(inter))
        
        x_vals = np.linspace(-10, 10, 20)
        chart_data = pd.DataFrame({'x': x_vals, 'y': float(m)*x_vals + float(inter)})
        st.line_chart(chart_data.set_index('x'))
        
        if st.button("Siguiente Ejercicio"):
             st.session_state.contador_ejercicios += 1
             preparar_nuevo_ejercicio()
             st.rerun()
