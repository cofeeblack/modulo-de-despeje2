import streamlit as st
import random
import pandas as pd
import numpy as np
from fractions import Fraction

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Matemática Esquemática - Fabio Molano", layout="centered")

# --- ESTILOS PERSONALIZADOS (RESTAURADOS) ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .titulo-esquemática { 
        color: #002D62 !important; text-align: center !important; font-weight: bold !important; 
        font-size: 62px !important; margin-top: 5px !important; margin-bottom: 30px !important;
        margin-left: -225px !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        display: block; letter-spacing: -2px; white-space: nowrap;
    }
    .stButton>button {
        background-color: #002D62 !important; color: #FFD700 !important; border-radius: 10px;
        border: 2px solid #FFD700; font-weight: bold; font-size: 22px; width: 100%; height: 60px;
    }
    .op-table { margin-left: auto; margin-right: auto; font-family: 'Courier New', monospace; font-size: 26px; border-collapse: collapse; }
    .op-table td { padding: 0px 15px; text-align: center; }
    .red-text { color: #e74c3c; font-weight: bold; }
    .linea-suma { border-top: 3px solid black; }
    .logo-container { display: flex; justify-content: center; margin-bottom: 0px; }
    hr { margin-top: 0px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE FORMATEO ---
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
    st.session_state.a = random.choice([i for i in range(-7, 8) if i != 0])
    st.session_state.b = random.choice([i for i in range(-7, 8) if i != 0])
    st.session_state.c = random.choice([i for i in range(-25, 26) if i != 0])
    st.session_state.opciones_paso3 = []
    st.session_state.opciones_paso5 = []
    st.session_state.error_en_actual = False

# --- NAVEGACIÓN ---
if 'pagina' not in st.session_state: st.session_state.pagina = "inicio"

if st.session_state.pagina == "inicio":
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try: st.image("logo fabio faraon.png", width=480)
    except: st.warning("Subir el logo a GitHub")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<span class="titulo-esquemática">Matemática Esquemática</span>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🚀 Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

elif st.session_state.pagina == "despeje":
    if 'contador_ejercicios' not in st.session_state:
        st.session_state.contador_ejercicios = 0
        st.session_state.puntos_totales = 0
        preparar_nuevo_ejercicio()

    if st.session_state.contador_ejercicios >= 10:
        st.header("🏁 Resultados")
        st.metric("Puntaje Final", f"{st.session_state.puntos_totales}/100")
        if st.button("Ir al Módulo Pendiente-Intercepto"):
            st.session_state.pagina = "pendiente_intercepto"
            st.rerun()
        st.stop()

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    st.title("Módulo de Despeje")
    st.subheader(f"Ejercicio {st.session_state.contador_ejercicios + 1}/10")
    st.latex(f"{fmt_c(a, 'x')} {fmt_c(b, 'y', True)} = {c}")

    # PASO 1
    if st.session_state.paso == 1:
        ans = st.radio("¿Cuál es la variable dependiente?", ["...", "x", "y"])
        if st.button("Comprobar"):
            if ans == "y": st.session_state.paso = 2
            else: st.error("❌ ¡Error! Debemos despejar 'y' para la forma explícita.")
            st.rerun()

    # PASO 2
    elif st.session_state.paso == 2:
        ins = st.text_input(f"¿Qué término sumamos para neutralizar {fmt_c(a, 'x')}?")
        if st.button("Aplicar Propiedad"):
            entrada = ins.replace(" ", "").lower().replace("+", "")
            esperado = fmt_c(-a, 'x').replace(" ", "").lower().replace("+", "")
            if entrada == esperado: st.session_state.paso = 3
            else: st.error(f"❌ Incorrecto. Debes sumar el opuesto: {fmt_c(-a, 'x')}")
            st.rerun()

    # PASO 3
    elif st.session_state.paso == 3:
        op_monomio = fmt_c(-a, 'x', incluir_mas=True)
        st.markdown(f"""<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
        <table class="op-table">
            <tr><td>{fmt_c(a, 'x')}</td><td>{fmt_c(b, 'y', True)}</td><td>=</td><td>{c}</td></tr>
            <tr class="red-text"><td>{op_monomio}</td><td></td><td>=</td><td>{op_monomio}</td></tr>
            <tr><td colspan="4" class="linea-suma"></td></tr>
        </table></div>""", unsafe_allow_html=True)
        correcta = f"{fmt_c(b, 'y')} = {c} {op_monomio}"
        if not st.session_state.opciones_paso3:
            st.session_state.opciones_paso3 = random.sample([correcta, f"{b}y = {c}{fmt_c(a, 'x', True)}", f"y = {c-a}x"], 3)
        res = st.radio("Resultado de la suma vertical:", st.session_state.opciones_paso3)
        if st.button("Siguiente"):
            if res == correcta: st.session_state.paso = 4
            else: st.error("❌ Error en la simplificación.")
            st.rerun()

    # PASO 4
    elif st.session_state.paso == 4:
        st.write("Ecuación actual:")
        st.latex(f"{fmt_c(b, 'y')} = {fmt_c(-a, 'x')} {'+' if c > 0 else ''} {c}")
        div = st.radio(f"¿Por qué número dividimos para dejar la 'y' sola?", ["...", f"{b}", f"{-b}"])
        if st.button("Aplicar División"):
            if div == str(b): 
                st.session_state.paso = 5
            else: st.error(f"❌ Debes dividir por el coeficiente de y, que es {b}.")
            st.rerun()

    # PASO 5 (NUEVO: PROPIEDAD DISTRIBUTIVA Y REGLA DE SIGNOS)
    elif st.session_state.paso == 5:
        st.subheader("Paso 5: Propiedad Distributiva")
        st.latex(r"y = \frac{" + f"{fmt_c(-a, 'x')} {'+' if c > 0 else ''} {c}" + r"}{" + f"{b}" + r"}")
        
        # Cálculo de signos correcto
        m_frac = Fraction(-a, b)
        b_frac = Fraction(c, b)
        
        # Formatear la ecuación final con ley de signos aplicada
        ec_correcta = f"y = {fmt_c(m_frac, 'x')} {fmt_c(b_frac, incluir_mas=True)}"
        
        if not st.session_state.opciones_paso5:
            # Distractores con errores de signos comunes
            d1 = f"y = {fmt_c(-m_frac, 'x')} {fmt_c(b_frac, incluir_mas=True)}"
            d2 = f"y = {fmt_c(m_frac, 'x')} {fmt_c(-b_frac, incluir_mas=True)}"
            st.session_state.opciones_paso5 = random.sample([ec_correcta, d1, d2], 3)

        ans_final = st.radio("Aplicando ley de signos en cada término, el resultado es:", st.session_state.opciones_paso5)
        
        if st.button("Finalizar Ejercicio"):
            if ans_final == ec_correcta:
                st.balloons()
                st.success("¡Excelente! Has aplicado correctamente la ley de signos.")
                st.session_state.puntos_totales += 10
            else:
                st.error(f"❌ Error de signos. La respuesta correcta era: {ec_correcta}")
            
            st.session_state.contador_ejercicios += 1
            preparar_nuevo_ejercicio()
            st.rerun()
