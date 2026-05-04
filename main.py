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
    /* AJUSTE DE TAMAÑO DE FUENTE PARA OPCIONES MÚLTIPLES */
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 20px;
    }
    .stRadio label {
        font-size: 22px !important;
        font-family: 'Courier New', monospace;
    }
    /* Estilo para la operación vertical alineada */
    .op-table {
        margin-left: auto;
        margin-right: auto;
        font-family: 'Courier New', monospace;
        font-size: 22px;
        border-collapse: collapse;
    }
    .op-table td {
        padding: 0px 10px;
        text-align: center;
    }
    .red-text { color: #e74c3c; font-weight: bold; }
    .linea-suma { border-top: 2px solid black; }
    </style>
    """, unsafe_allow_html=True)

# Función para formatear coeficientes ocultando el 1
def fmt_c(n, var="", incluir_mas=False):
    # Manejo de fracciones para el paso final
    if isinstance(n, Fraction):
        signo = "+" if incluir_mas and n > 0 else ""
        if n.denominator == 1:
            return fmt_c(n.numerator, var, incluir_mas)
        return f"{signo}{n}{var}"
        
    signo = "+" if incluir_mas and n > 0 else ""
    if n == 1: return f"{signo}{var}" if var else f"{signo}1"
    if n == -1: return f"-{var}" if var else "-1"
    return f"{signo}{n}{var}"

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
    eq_text = f"{fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}"
    st.info(f"**Ecuación Inicial:**  {eq_text}")

    if st.session_state.paso == 1:
        st.subheader("Paso 1: Identificación")
        resp = st.radio("¿Cuál es la variable dependiente?", ["Selecciona...", "x", "y"], index=0)
        if st.button("Comprobar"):
            if resp == "y":
                st.session_state.paso = 2
                st.rerun()

    elif st.session_state.paso == 2:
        st.subheader("Paso 2: Neutralizar término")
        st.write(f"Para dejar solo el término con **y**, ¿qué debemos sumar o restar a ambos lados?")
        inst = st.text_input("Escribe el monomio con su signo (ej: -2x o +3x):")
        
        if st.button("Aplicar"):
            resp_l = inst.lower().replace(" ", "")
            val_objetivo = -a
            target_con_signo = fmt_c(val_objetivo, 'x', incluir_mas=True).lower()
            
            if resp_l == target_con_signo or resp_l == fmt_c(val_objetivo, 'x').lower():
                st.session_state.paso = 3
                st.rerun()
            else:
                st.error(f"Si tenemos {fmt_c(a, 'x')}, debemos aplicar su opuesto.")

    elif st.session_state.paso == 3:
        st.subheader("Paso 3: Operación Vertical")
        monomio_op = fmt_c(-a, 'x', incluir_mas=True)
        
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <table class="op-table">
                <tr>
                    <td>{fmt_c(a, 'x')}</td>
                    <td>{'+' if b > 0 else '-'}</td>
                    <td>{fmt_c(abs(b), 'y')}</td>
                    <td>=</td>
                    <td>{c}</td>
                    <td></td>
                </tr>
                <tr class="red-text">
                    <td>{monomio_op}</td>
                    <td></td>
                    <td></td>
                    <td>=</td>
                    <td></td>
                    <td>{monomio_op}</td>
                </tr>
                <tr>
                    <td colspan="6" class="linea-suma"></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
        
        correcta = f"{fmt_c(b, 'y')} = {c} {monomio_op}"
        error_signo = f"{fmt_c(b, 'y')} = {c} {fmt_c(a, 'x', incluir_mas=True)}"
        error_suma = f"{fmt_c(b, 'y')} = {c + (-a if 'x' in monomio_op else 0)}x" # Error típico de suma errónea
        
        opciones = [correcta, error_signo, "2y = 4x"] # Añadí una opción corta de error común
        random.shuffle(opciones)
        
        res_sel = st.radio("¿Cuál es el resultado de la operación?", opciones)
        
        if st.button("Verificar Resultado"):
            if res_sel == correcta:
                st.success("¡Muy bien!")
                st.session_state.paso = 4
                st.rerun()
            else:
                st.error("Revisa los signos y recuerda que no puedes sumar números con letras.")

    elif st.session_state.paso == 4:
        st.subheader("Paso 4: El Coeficiente")
        monomio_op = fmt_c(-a, 'x', incluir_mas=True)
        st.latex(f"{fmt_c(b, 'y')} = {c} {monomio_op}")
        op_div = st.selectbox(f"¿Por cuánto dividimos toda la ecuación?", 
                             ["Selecciona...", f"{b}", f"{-b}"], index=0)
        if st.button("Siguiente"):
            if op_div == f"{b}":
                st.session_state.paso = 5
                st.rerun()

    elif st.session_state.paso == 5:
        st.subheader("Paso 5: Resultado Final")
        m = Fraction(-a, b)
        inter = Fraction(c, b)
        res_final = f"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}"
        st.success(f"¡LOGRADO! La ecuación final es: {res_final}")
        if st.button("Nuevo Ejercicio"):
            st.session_state.clear()
            st.rerun()
