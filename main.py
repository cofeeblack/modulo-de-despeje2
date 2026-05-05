import streamlit as st
import random
import pandas as pd
import numpy as np
from fractions import Fraction

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Matemática Esquemática - Fabio Molano", layout="centered")

# --- ESTILOS PERSONALIZADOS UNIFICADOS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    
    /* Título principal con tamaño especial */
    .titulo-esquemática { 
        color: #002D62 !important; text-align: center !important; font-weight: bold !important; 
        font-size: 62px !important; margin-top: 5px !important; margin-bottom: 30px !important;
        margin-left: -225px !important; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        display: block; letter-spacing: -2px; white-space: nowrap;
    }

    /* Unificación de fuente para TODO lo demás (Ecuaciones, Textos, Botones) */
    html, body, [class*="st-"], .stMarkdown, p, span, label, input, button, .stSelectbox, .stNumberInput {
        font-size: 24px !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    }

    /* Botones específicos */
    .stButton>button {
        background-color: #002D62 !important; color: #FFD700 !important; border-radius: 10px;
        border: 2px solid #FFD700; font-weight: bold; font-size: 24px !important; width: 100%; height: 60px;
    }

    /* Tabla de operación vertical */
    .op-table { margin-left: auto; margin-right: auto; font-family: 'Courier New', monospace; font-size: 28px !important; border-collapse: collapse; }
    .op-table td { padding: 0px 15px; text-align: center; }
    .red-text { color: #e74c3c; font-weight: bold; }
    .linea-suma { border-top: 3px solid black; }
    
    .logo-container { display: flex; justify-content: center; margin-bottom: 0px; }
    hr { margin-top: 0px; margin-bottom: 25px; }
    </style>
    """, unsafe_allow_html=True)

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
    st.session_state.a = random.choice([i for i in range(-7, 8) if i != 0])
    st.session_state.b = random.choice([i for i in range(-7, 8) if i != 0])
    st.session_state.c = random.choice([i for i in range(-25, 26) if i != 0])
    st.session_state.opciones_paso3 = []
    st.session_state.opciones_paso5 = []
    st.session_state.error_en_actual = False

def preparar_pi():
    st.session_state.pi_modo = "analisis"
    st.session_state.pi_m = random.choice([-3, -2, -1, 1, 2, 3, 0.5, -0.5])
    st.session_state.pi_b = random.randint(-5, 5)
    st.session_state.pi_opciones = []

# --- LÓGICA DE NAVEGACIÓN ---
if 'pagina' not in st.session_state: st.session_state.pagina = "inicio"

if st.session_state.pagina == "inicio":
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try: st.image("logo fabio faraon.png", width=480)
    except: st.warning("Logo no detectado")
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
        st.header("🏁 Resultados del Módulo")
        st.write(f"Puntaje Final: {st.session_state.puntos_totales}/100")
        if st.button("📈 Ir al Módulo Pendiente-Intercepto"):
            st.session_state.pagina = "pendiente_intercepto"
            preparar_pi()
            st.rerun()
        st.stop()

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    st.write(f"**Módulo de Despeje**")
    st.write(f"Ejercicio {st.session_state.contador_ejercicios + 1}/10")
    st.latex(f"{fmt_c(a, 'x')} {fmt_c(b, 'y', True)} = {c}")

    if st.session_state.paso == 1:
        st.write("Paso 1: ¿Cuál es la variable dependiente?")
        ans = st.radio("Selecciona:", ["...", "x", "y"])
        if st.button("Comprobar"):
            if ans == "y": st.session_state.paso = 2
            else: st.error("❌ Error. Debemos despejar 'y'.")
            st.rerun()

    elif st.session_state.paso == 2:
        st.write("Paso 2: Neutralizar")
        ins = st.text_input(f"¿Qué término sumamos para quitar {fmt_c(a, 'x')}?")
        if st.button("Aplicar"):
            entrada = ins.replace(" ", "").lower().replace("+", "")
            esperado = fmt_c(-a, 'x').replace(" ", "").lower().replace("+", "")
            if entrada == esperado: st.session_state.paso = 3
            else: st.error(f"❌ Incorrecto. Suma {fmt_c(-a, 'x')}")
            st.rerun()

    elif st.session_state.paso == 3:
        st.write("Paso 3: Operación Vertical")
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
        res = st.radio("¿Qué sobrevive?", st.session_state.opciones_paso3)
        if st.button("Siguiente"):
            if res == correcta: st.session_state.paso = 4
            else: st.error("❌ Error en la suma.")
            st.rerun()

    elif st.session_state.paso == 4:
        st.write("Paso 4: El Coeficiente")
        st.latex(f"{fmt_c(b, 'y')} = {fmt_c(-a, 'x')} {'+' if c > 0 else ''} {c}")
        div = st.radio(f"¿Por qué número dividimos toda la ecuación?", ["...", f"{b}", f"{-b}"])
        if st.button("Dividir"):
            if div == str(b): st.session_state.paso = 5
            else: st.error(f"❌ Divide por {b}.")
            st.rerun()

    elif st.session_state.paso == 5:
        st.write("Paso 5: Resultado Final (Ley de Signos)")
        st.latex(r"y = \frac{" + f"{fmt_c(-a, 'x')} {'+' if c > 0 else ''} {c}" + r"}{" + f"{b}" + r"}")
        
        m_f, b_f = Fraction(-a, b), Fraction(c, b)
        eq_c = f"y = {fmt_c(m_f, 'x')} {fmt_c(b_f, incluir_mas=True)}"
        
        if not st.session_state.opciones_paso5:
            st.session_state.opciones_paso5 = random.sample([eq_c, f"y = {-m_f}x + {b_f}", f"y = {m_f}x - {b_f}"], 3)
        
        sel = st.radio("Selecciona la ecuación simplificada:", st.session_state.opciones_paso5)
        if st.button("Terminar Ejercicio"):
            if sel == eq_c:
                st.balloons(); st.session_state.puntos_totales += 10
            else: st.error(f"❌ Error de signos. Era: {eq_c}")
            st.session_state.contador_ejercicios += 1
            preparar_nuevo_ejercicio()
            st.rerun()

# --- VISTA: PENDIENTE-INTERCEPTO ---
elif st.session_state.pagina == "pendiente_intercepto":
    st.title("📈 Módulo Pendiente-Intercepto")
    m_t, b_t = st.session_state.pi_m, st.session_state.pi_b

    if st.session_state.pi_modo == "analisis":
        st.write("Parte 1: Identificación Numérica")
        st.latex(f"y = {fmt_c(m_t, 'x')} {'+' if b_t >= 0 else ''} {b_t}")
        c1, c2 = st.columns(2)
        with c1: m_in = st.number_input("Identifica m:", step=0.1)
        with c2: b_in = st.number_input("Identifica b:", step=1.0)
        if st.button("Validar"):
            if float(m_in) == float(m_t) and int(b_in) == int(b_t):
                st.success("¡Correcto!"); st.session_state.pi_modo = "grafico"
                st.rerun()
            else: st.error("Revisa los valores.")

    elif st.session_state.pi_modo == "grafico":
        st.write("Parte 2: Identificación Visual")
        x = np.linspace(-10, 10, 100)
        y = float(m_t) * x + b_t
        st.line_chart(pd.DataFrame({'x': x, 'y': y}).set_index('x'), height=300)
        
        c_pi = f"y = {fmt_c(m_t, 'x')} {'+' if b_t >= 0 else ''} {b_t}"
        if not st.session_state.pi_opciones:
            st.session_state.pi_opciones = random.sample([c_pi, f"y = {-m_t}x + {b_t}", f"y = {m_t}x - {b_t}", f"y = {m_t*2}x + {b_t}"], 4)
        
        op = st.radio("¿Cuál es la ecuación?", st.session_state.pi_opciones)
        if st.button("Verificar"):
            if op == c_pi: st.balloons(); st.success("¡Perfecto!")
            else: st.warning("Mira el corte en Y.")

    if st.button("🏠 Salir"): st.session_state.clear(); st.rerun()
