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
    div[data-testid="stMarkdownContainer"] > p { font-size: 20px; }
    .stRadio label {
        font-size: 22px !important;
        font-family: 'Courier New', monospace;
    }
    .op-table {
        margin-left: auto;
        margin-right: auto;
        font-family: 'Courier New', monospace;
        font-size: 22px;
        border-collapse: collapse;
    }
    .op-table td { padding: 0px 10px; text-align: center; }
    .red-text { color: #e74c3c; font-weight: bold; }
    .linea-suma { border-top: 2px solid black; }
    </style>
    """, unsafe_allow_html=True)

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

# --- INICIALIZACIÓN SEGURA DEL ESTADO ---
if 'paso' not in st.session_state:
    st.session_state.paso = 1
    st.session_state.a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    st.session_state.b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    st.session_state.c = random.randint(5, 25)
    st.session_state.opciones_paso3 = []
    st.session_state.opciones_paso5 = []

a, b, c = st.session_state.a, st.session_state.b, st.session_state.c

st.title("Módulo de Despeje: Variable Dependiente")
st.info(f"**Ecuación Inicial:** {fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}")

# --- FLUJO DE PASOS ---

if st.session_state.paso == 1:
    st.subheader("Paso 1: Identificación")
    resp = st.radio("¿Cuál es la variable dependiente?", ["...", "x", "y"])
    if st.button("Comprobar"):
        if resp == "y":
            st.session_state.paso = 2
            st.rerun()

elif st.session_state.paso == 2:
    st.subheader("Paso 2: Neutralizar término")
    inst = st.text_input("¿Qué monomio sumamos o restamos a ambos lados? (ej: -2x):")
    if st.button("Aplicar"):
        target = fmt_c(-a, 'x').lower().replace("+", "")
        ingreso = inst.lower().replace(" ", "").replace("+", "")
        if ingreso == target:
            st.session_state.paso = 3
            st.rerun()
        else:
            if a > 0:
                st.warning(f"Pista: El término {fmt_c(a, 'x')} es positivo. Si quieres que desaparezca un término que está sumando, entonces debes...")
            else:
                st.warning(f"Pista: El término {fmt_c(a, 'x')} es negativo. Si quieres que desaparezca un término que está restando, entonces debes...")

elif st.session_state.paso == 3:
    st.subheader("Paso 3: Operación Vertical")
    monomio_op = fmt_c(-a, 'x', incluir_mas=True)
    st.markdown(f"""<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
        <table class="op-table">
            <tr><td>{fmt_c(a, 'x')}</td><td>{'+' if b > 0 else '-'}</td><td>{fmt_c(abs(b), 'y')}</td><td>=</td><td>{c}</td><td></td></tr>
            <tr class="red-text"><td>{monomio_op}</td><td></td><td></td><td>=</td><td></td><td>{monomio_op}</td></tr>
            <tr><td colspan="6" class="linea-suma"></td></tr>
        </table></div>""", unsafe_allow_html=True)

    if not st.session_state.opciones_paso3:
        correcta = f"{fmt_c(b, 'y')} = {c} {monomio_op}"
        opcs = [correcta, f"{fmt_c(b, 'y')} = {c} {fmt_c(a, 'x', incluir_mas=True)}", f"2y = {c-a if 'x' not in str(c-a) else c}x"]
        random.shuffle(opcs)
        st.session_state.opciones_paso3 = opcs

    res_sel = st.radio("¿Cuál es el resultado de la operación?", st.session_state.opciones_paso3)
    if st.button("Verificar Resultado"):
        if res_sel == f"{fmt_c(b, 'y')} = {c} {monomio_op}":
            st.session_state.paso = 4
            st.rerun()

elif st.session_state.paso == 4:
    st.subheader("Paso 4: El Coeficiente")
    monomio_op = fmt_c(-a, 'x', incluir_mas=True)
    st.latex(f"{fmt_c(b, 'y')} = {c} {monomio_op}")
    op_div = st.selectbox("¿Por cuánto dividimos toda la ecuación?", ["...", f"{b}", f"{-b}"], index=0)
    if st.button("Siguiente"):
        if op_div == f"{b}":
            st.session_state.paso = 5
            st.rerun()

elif st.session_state.paso == 5:
    st.subheader("Paso 5: Resultado Final")
    # Mostrar la ecuación del paso anterior con la división repartida
    st.write("A partir de la siguiente operación, indica la ecuación simplificada:")
    st.latex(rf"y = \frac{{{c}}}{{{b}}} \frac{{{fmt_c(-a, 'x', incluir_mas=True)}}}{{{b}}}")
    
    m = Fraction(-a, b)
    inter = Fraction(c, b)
    if not st.session_state.opciones_paso5:
        correcta = f"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}"
        opcs = [correcta, f"y = {fmt_c(-m, 'x')} {'+' if inter > 0 else ''} {inter}", f"y = {fmt_c(m, 'x')} {'-' if inter > 0 else '+'}{abs(inter)}"]
        random.shuffle(opcs)
        st.session_state.opciones_paso5 = opcs

    res_final = st.radio("Ecuación final:", st.session_state.opciones_paso5)
    if st.button("Finalizar"):
        if res_final == f"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}":
            st.balloons()
            st.success("¡Excelente trabajo!")
            if st.button("Nuevo Ejercicio"):
                for key in list(st.session_state.keys()): del st.session_state[key]
                st.rerun()
