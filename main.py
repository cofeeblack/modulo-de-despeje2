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
    
    /* Título con color exacto del logo (#002D62) */
    .titulo-esquemática { 
        color: #002D62; 
        text-align: center; 
        font-weight: bold; 
        font-size: 42px;
        margin-top: 10px;
        margin-bottom: 20px;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
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
    
    /* Tabla de operación vertical */
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
# Asegúrate de que en GitHub el archivo se llame exactamente así
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

# --- NAVEGACIÓN ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = "inicio"

# --- VISTA 1: INICIO (BIENVENIDA) ---
if st.session_state.pagina == "inicio":
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image(NOMBRE_LOGO, width=480)
    except:
        st.error(f"⚠️ No se encontró el logo '{NOMBRE_LOGO}'")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<h1 class="titulo-esquemática">Matemática Esquemática</h1>', unsafe_allow_html=True)
    st.write("---")
    st.markdown('<p class="texto-centrado">Bienvenido al entorno visual del profesor <b>Fabio Molano</b>.</p>', unsafe_allow_html=True)
    st.markdown('<p class="texto-centrado">Aquí transformamos ecuaciones en estructuras comprensibles para dominar el lenguaje del cambio.</p>', unsafe_allow_html=True)
    st.write("") 
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
        if st.button("Nueva Serie"):
            st.session_state.clear()
            st.rerun()
        st.stop()

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    st.title("Módulo de Despeje")
    st.write(f"**Ejercicio {st.session_state.contador_ejercicios + 1} de 10**")
    st.info(f"**Ecuación Inicial:** {fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}")

    # PASO 1: IDENTIFICACIÓN
    if st.session_state.paso == 1:
        st.subheader("Paso 1: Identificación")
        resp = st.radio("¿Cuál es la variable dependiente?", ["...", "x", "y"])
        if st.button("Comprobar"):
            if resp == "y": st.session_state.paso = 2
            else: st.session_state.error_en_actual = True; st.error("Error ☹️")
            st.rerun()

    # PASO 2: NEUTRALIZAR
    elif st.session_state.paso == 2:
        st.subheader("Paso 2: Neutralizar término")
        inst = st.text_input(f"¿Qué monomio debemos sumar/restar para dejar solo el término con 'y'?")
        if st.button("Aplicar"):
            if inst.lower().replace(" ", "") == fmt_c(-a, 'x').lower().replace("+", ""):
                st.session_state.paso = 3
            else: st.session_state.error_en_actual = True; st.warning("Incorrecto ☹️")
            st.rerun()

    # PASO 3: OPERACIÓN VERTICAL
    elif st.session_state.paso == 3:
        st.subheader("Paso 3: Operación Vertical")
        monomio_op = fmt_c(-a, 'x', incluir_mas=True)
        st.markdown(f"""<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <table class="op-table">
                <tr><td>{fmt_c(a, 'x')}</td><td>{'+' if b > 0 else '-'}</td><td>{fmt_c(abs(b), 'y')}</td><td>=</td><td>{c}</td><td></td></tr>
                <tr class="red-text"><td>{monomio_op}</td><td></td><td></td><td>=</td><td></td><td>{monomio_op}</td></tr>
                <tr><td colspan="6" class="linea-suma"></td></tr>
            </table></div>""", unsafe_allow_html=True)
        
        correcta = f"{fmt_c(b, 'y')} = {c} {monomio_op}"
        if not st.session_state.opciones_paso3:
            opcs = [correcta, f"{fmt_c(b, 'y')} = {c} {fmt_c(a, 'x', incluir_mas=True)}", f"{b}y = {c-a}x"]
            random.shuffle(opcs); st.session_state.opciones_paso3 = opcs
        
        res = st.radio("¿Cuál es el resultado de la operación?", st.session_state.opciones_paso3)
        if st.button("Verificar"):
            if res == correcta: st.session_state.paso = 4
            else: st.session_state.error_en_actual = True; st.error("Error ☹️")
            st.rerun()

    # PASO 4: COEFICIENTE
    elif st.session_state.paso == 4:
        st.subheader("Paso 4: El Coeficiente")
        st.latex(f"{fmt_c(b, 'y')} = {c} {fmt_c(-a, 'x', incluir_mas=True)}")
        op = st.selectbox(f"¿Por qué número debemos dividir ambos lados para despejar 'y'?", ["...", f"{b}", f"{-b}"])
        if st.button("Siguiente"):
            if op == f"{b}": st.session_state.paso = 5
            else: st.session_state.error_en_actual = True; st.error("Error ☹️")
            st.rerun()

    # PASO 5: FINAL Y GRÁFICO
    elif st.session_state.paso == 5:
        st.subheader("Paso 5: Resultado y Análisis Gráfico")
        m, inter = Fraction(-a, b), Fraction(c, b)
        txt_c = f"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}"
        
        if not st.session_state.opciones_paso5:
            opcs = [txt_c, f"y = {fmt_c(-m, 'x')} {'+' if inter > 0 else ''} {inter}", f"y = {fmt_c(m, 'x')} - {abs(inter)}"]
            random.shuffle(opcs); st.session_state.opciones_paso5 = opcs

        res_f = st.radio("Selecciona la ecuación de la recta despejada:", st.session_state.opciones_paso5, disabled=st.session_state.finalizado)
        
        if not st.session_state.finalizado:
            if st.button("Finalizar Ejercicio"):
                st.session_state.finalizado = True
                if res_f == txt_c and not st.session_state.error_en_actual:
                    st.balloons(); st.session_state.puntos_totales += 10
                else: st.error(f"Incorrecto. La respuesta correcta es: {txt_c}")
                st.rerun()
        else:
            st.write("---")
            col_m, col_b = st.columns(2)
            col_m.metric("Pendiente (m)", str(m))
            col_b.metric("Intercepto (b)", str(inter))
            
            x_vals = np.linspace(-10, 10, 20)
            y_vals = float(m)*x_vals + float(inter)
            chart_data = pd.DataFrame({'x': x_vals, 'y': y_vals})
            st.line_chart(chart_data.set_index('x'))
            
            if st.button("Siguiente Ejercicio"):
                st.session_state.contador_ejercicios += 1
                preparar_nuevo_ejercicio()
                st.rerun()
