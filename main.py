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
    .titulo-esquemática { 
        color: #002D62 !important; text-align: center !important; font-weight: bold !important; 
        font-size: 62px !important; margin-top: 5px !important; margin-bottom: 30px !important;
        margin-left: -225px !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        display: block; letter-spacing: -2px; white-space: nowrap;
    }
    .texto-centrado { text-align: center !important; font-size: 20px !important; color: #333333; display: block; width: 100%; }
    .stButton>button {
        background-color: #002D62 !important; color: #FFD700 !important; border-radius: 10px;
        border: 2px solid #FFD700; font-weight: bold; font-size: 22px; width: 100%; height: 60px;
    }
    .op-table { margin-left: auto; margin-right: auto; font-family: 'Courier New', monospace; font-size: 24px; border-collapse: collapse; }
    .op-table td { padding: 0px 12px; text-align: center; }
    .red-text { color: #e74c3c; font-weight: bold; }
    .linea-suma { border-top: 2px solid black; }
    .logo-container { display: flex; justify-content: center; margin-bottom: 0px; }
    hr { margin-top: 0px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIONES AUXILIARES ---
NOMBRE_LOGO = "logo fabio faraon.png"

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

def preparar_pi():
    st.session_state.pi_modo = "analisis" # O "grafico"
    st.session_state.pi_m = random.choice([-3, -2, -1, 1, 2, 3, 0.5, -0.5])
    st.session_state.pi_b = random.randint(-5, 5)
    st.session_state.pi_opciones = []

# --- INICIALIZACIÓN DE ESTADO ---
if 'pagina' not in st.session_state: st.session_state.pagina = "inicio"

# --- VISTA: INICIO ---
if st.session_state.pagina == "inicio":
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try: st.image(NOMBRE_LOGO, width=480)
    except: st.warning("Logo no detectado.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<span class="titulo-esquemática">Matemática Esquemática</span>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🚀 Entrar al Módulo de Despeje"):
        st.session_state.pagina = "despeje"
        st.rerun()

# --- VISTA: MÓDULO DE DESPEJE (RESTAURADO) ---
elif st.session_state.pagina == "despeje":
    if 'contador_ejercicios' not in st.session_state:
        st.session_state.contador_ejercicios = 0
        st.session_state.puntos_totales = 0
        preparar_nuevo_ejercicio()

    if st.session_state.contador_ejercicios >= 10:
        st.header("🏁 Módulo Completado")
        st.metric("Puntaje", f"{st.session_state.puntos_totales}/100")
        if st.button("📈 Ir al Módulo Pendiente-Intercepto"):
            st.session_state.pagina = "pendiente_intercepto"
            preparar_pi()
            st.rerun()
        st.stop()

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    st.title("Módulo de Despeje")
    st.write(f"**Ejercicio {st.session_state.contador_ejercicios + 1}/10:**  `{fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}`")

    # Los 5 pasos interactivos reales
    if st.session_state.paso == 1:
        st.subheader("Paso 1: ¿Cuál es la variable dependiente?")
        ans = st.radio("Selecciona:", ["...", "x", "y"])
        if st.button("Comprobar"):
            if ans == "y": st.session_state.paso = 2
            else: st.session_state.error_en_actual = True; st.error("¡Revisa! Queremos dejar sola a la 'y'")
            st.rerun()

    elif st.session_state.paso == 2:
        st.subheader("Paso 2: Neutralizar")
        ins = st.text_input(f"¿Qué término sumamos para quitar {fmt_c(a, 'x')}?")
        if st.button("Aplicar"):
            if ins.replace(" ", "") == fmt_c(-a, 'x').replace("+", ""): st.session_state.paso = 3
            else: st.session_state.error_en_actual = True; st.error("Incorrecto.")
            st.rerun()

    elif st.session_state.paso == 3:
        st.subheader("Paso 3: Operación Vertical")
        op_monomio = fmt_c(-a, 'x', incluir_mas=True)
        st.markdown(f"""<div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px;">
        <table class="op-table">
            <tr><td>{fmt_c(a, 'x')}</td><td>{'+' if b > 0 else '-'}</td><td>{fmt_c(abs(b), 'y')}</td><td>=</td><td>{c}</td></tr>
            <tr class="red-text"><td>{op_monomio}</td><td></td><td></td><td>=</td><td>{op_monomio}</td></tr>
            <tr><td colspan="5" class="linea-suma"></td></tr>
        </table></div>""", unsafe_allow_html=True)
        correcta = f"{fmt_c(b, 'y')} = {c} {op_monomio}"
        if not st.session_state.opciones_paso3:
            st.session_state.opciones_paso3 = random.sample([correcta, f"{b}y = {c}{fmt_c(a, 'x', True)}", f"y = {c-a}x"], 3)
        res = st.radio("¿Qué sobrevive?", st.session_state.opciones_paso3)
        if st.button("Siguiente"):
            if res == correcta: st.session_state.paso = 4
            else: st.session_state.error_en_actual = True; st.error("Error en la suma.")
            st.rerun()

    elif st.session_state.paso == 4:
        st.subheader("Paso 4: El Coeficiente")
        st.latex(f"{fmt_c(b, 'y')} = {c} {fmt_c(-a, 'x', True)}")
        div = st.radio(f"¿Por qué número dividimos toda la ecuación?", ["...", f"{b}", f"{-b}"])
        if st.button("Dividir"):
            if div == str(b): st.session_state.paso = 5
            else: st.session_state.error_en_actual = True; st.error("Debe ser el número que multiplica a y.")
            st.rerun()

    elif st.session_state.paso == 5:
        st.subheader("Paso 5: Resultado Final")
        m, inter = Fraction(-a, b), Fraction(c, b)
        final_eq = f"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}"
        if not st.session_state.opciones_paso5:
            st.session_state.opciones_paso5 = random.sample([final_eq, f"y = {m}x - {inter}", f"y = {-m}x + {inter}"], 3)
        sel = st.radio("Ecuación final:", st.session_state.opciones_paso5)
        if st.button("Terminar Ejercicio"):
            if sel == final_eq and not st.session_state.error_en_actual: st.balloons(); st.session_state.puntos_totales += 10
            st.session_state.contador_ejercicios += 1
            preparar_nuevo_ejercicio()
            st.rerun()

# --- VISTA: MÓDULO PENDIENTE-INTERCEPTO ---
elif st.session_state.pagina == "pendiente_intercepto":
    st.title("📈 Módulo Pendiente-Intercepto")
    m_t, b_t = st.session_state.pi_m, st.session_state.pi_b

    if st.session_state.pi_modo == "analisis":
        st.subheader("Parte 1: Identificación Numérica")
        st.latex(f"y = {fmt_c(m_t, 'x')} {'+' if b_t >= 0 else ''} {b_t}")
        c1, c2 = st.columns(2)
        with c1: m_in = st.number_input("Pendiente (m):", value=0.0)
        with c2: b_in = st.number_input("Intercepto (b):", value=0.0)
        
        if st.button("Validar Datos"):
            if float(m_in) == float(m_t) and int(b_in) == int(b_t):
                st.success(f"¡Bien! El intercepto con Y ocurre en (0, {b_t})")
                if st.button("Pasar a Gráfico >>"):
                    st.session_state.pi_modo = "grafico"
                    st.rerun()
            else: st.error("Revisa los valores de la ecuación.")

    elif st.session_state.pi_modo == "grafico":
        st.subheader("Parte 2: Identificación Visual")
        x = np.linspace(-10, 10, 100)
        y = float(m_t) * x + b_t
        st.line_chart(pd.DataFrame({'x': x, 'y': y}).set_index('x'), height=300)
        
        correcta_pi = f"y = {fmt_c(m_t, 'x')} {'+' if b_t >= 0 else ''} {b_t}"
        if not st.session_state.pi_opciones:
            st.session_state.pi_opciones = random.sample([correcta_pi, f"y = {-m_t}x + {b_t}", f"y = {m_t}x + {-b_t}", f"y = {m_t*2}x + {b_t}"], 4)
        
        op = st.radio("¿Cuál es la ecuación de la recta?", st.session_state.pi_opciones)
        if st.button("Verificar Gráfico"):
            if op == correcta_pi:
                st.balloons(); st.success("¡Dominas la interpretación gráfica!")
                if st.button("Nuevo Desafío"): preparar_pi(); st.rerun()
            else: st.warning("Observa el punto de corte en el eje vertical.")

    if st.button("🏠 Salir"): st.session_state.clear(); st.rerun()
