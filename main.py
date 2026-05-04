import streamlit as st
import random
from fractions import Fraction

# --- CONFIGURACIÓN DE PÁGINA Y ESTÉTICA ---
st.set_page_config(page_title="Matemáticas Fabio Molano", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1 { color: #003366; }
    .stButton>button {
        background-color: #003366;
        color: #FFD700;
        border-radius: 10px;
        border: 2px solid #FFD700;
        font-weight: bold;
    }
    .math-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FFD700;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para formatear coeficientes (oculta el 1)
def fmt_c(n, var=""):
    if n == 1: return var if var else "1"
    if n == -1: return f"-{var}" if var else "-1"
    return f"{n}{var}"

# --- BARRA LATERAL ---
with st.sidebar:
    try:
        st.image("logo.png", width=200)
    except:
        st.write("### 🎓 Fabio Molano")
    modulo = st.radio("Módulos:", ["1. Módulo de Despeje", "2. Módulo Gráfico"])

# --- MÓDULO DE DESPEJE ---
if "1." in modulo:
    st.title("Módulo de Despeje: Variable Dependiente")
    
    if 'ej_id' not in st.session_state:
        st.session_state.a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        st.session_state.b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        st.session_state.c = random.randint(5, 25)
        st.session_state.paso = 1
        st.session_state.ej_id = random.random()

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c
    
    # Ecuación inicial con formato limpio
    eq_text = f"{fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}"
    st.info(f"**Ecuación:**  {eq_text}")

    # PASO 1: Identificación
    if st.session_state.paso == 1:
        st.subheader("Paso 1: Identificación")
        resp = st.radio("¿Cuál es la variable dependiente?", ["Selecciona...", "x", "y"], index=0)
        if st.button("Comprobar"):
            if resp == "y":
                st.success("¡Correcto!")
                st.session_state.paso = 2
                st.rerun()

    # PASO 2: Elegir monomio
    elif st.session_state.paso == 2:
        st.subheader("Paso 2: Neutralizar término")
        st.write(f"Para dejar solo el término con **y**, ¿qué debemos sumar o restar a ambos lados?")
        inst = st.text_input("Escribe el monomio (ej: -2x o +3x):")
        
        if st.button("Aplicar"):
            resp_l = inst.lower().replace(" ", "").replace("+", "")
            target = f"{-a}x" if -a != 1 else "x"
            if -a == -1: target = "-x"
            
            if resp_l == target or resp_l == f"{-a}x":
                st.session_state.paso = 3
                st.rerun()
            else:
                st.error(f"Si tenemos {fmt_c(a, 'x')}, debemos aplicar su opuesto.")

    # PASO 3: Operación Vertical y Resultado
    elif st.session_state.paso == 3:
        st.subheader("Paso 3: Operación Vertical")
        # Visualización de la suma/resta vertical
        monomio_op = fmt_c(-a, 'x')
        st.markdown(f"""
        <div class='math-box'>
        <div style='text-align: center; font-family: monospace; font-size: 20px;'>
            {fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}<br>
            <span style='color: red;'>{monomio_op} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; = {monomio_op}</span><br>
            <hr style='border: 1px solid black;'>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        opciones = [
            f"{fmt_c(b, 'y')} = {c} {monomio_op}",
            f"{fmt_c(b, 'y')} = {c + a}x",
            f"{fmt_c(b, 'y')} = {c} {'+' if a > 0 else ''} {fmt_c(a, 'x')}"
        ]
        random.shuffle(opciones)
        res_sel = st.radio("¿Cuál es el resultado de la operación?", opciones)
        
        if st.button("Verificar Resultado"):
            if res_sel == opciones[0] or f"{c} {monomio_op}" in res_sel:
                st.success("¡Muy bien! Los términos se han cancelado a la izquierda.")
                st.session_state.paso = 4
                st.rerun()
            else:
                st.error("Error común: Recuerda que no puedes sumar números con letras directamente.")

    # PASO 4: División
    elif st.session_state.paso == 4:
        st.subheader("Paso 4: El Coeficiente")
        st.latex(f"{fmt_c(b, 'y')} = {c} {fmt_c(-a, 'x')}")
        op_div = st.selectbox(f"¿Por cuánto dividimos toda la ecuación?", 
                             ["Selecciona...", f"{b}", f"{-b}", "1"], index=0)
        if st.button("Siguiente"):
            if op_div == f"{b}":
                st.session_state.paso = 5
                st.rerun()

    # PASO 5: Simplificación Final
    elif st.session_state.paso == 5:
        st.subheader("Paso 5: Resultado Final")
        m = Fraction(-a, b)
        inter = Fraction(c, b)
        correcta = f"y = {m}x {'+' if inter > 0 else ''} {inter}"
        st.success(f"¡LOGRADO! La ecuación es: {correcta}")
        if st.button("Nuevo Ejercicio"):
            st.session_state.clear()
            st.rerun()
