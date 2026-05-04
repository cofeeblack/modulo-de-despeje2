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
        font-size: 22px;
    }
    div[data-testid="stMarkdownContainer"] > p { font-size: 22px; }
    .stRadio label, .stSelectbox label {
        font-size: 24px !important;
        font-family: 'Courier New', monospace;
    }
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
    .stTextInput input { font-size: 22px !important; }
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

def reiniciar_ejercicio():
    st.session_state.paso = 1
    st.session_state.a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    st.session_state.b = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    st.session_state.c = random.randint(5, 25)
    st.session_state.opciones_paso3 = []
    st.session_state.opciones_paso5 = []
    st.session_state.error_en_actual = False
    st.session_state.finalizado = False

def reset_total():
    st.session_state.clear()
    st.rerun()

# --- INICIALIZACIÓN ---
if 'contador_ejercicios' not in st.session_state:
    st.session_state.contador_ejercicios = 0
    st.session_state.ejercicios_perfectos = 0
    st.session_state.ejercicios_erroneos = 0
    st.session_state.puntos_totales = 0
    st.session_state.finalizado = False
    reiniciar_ejercicio()

# --- INFORME FINAL ---
if st.session_state.contador_ejercicios >= 10:
    st.title("📊 Informe de Desempeño")
    col1, col2, col3 = st.columns(3)
    col1.metric("Puntaje Total", f"{st.session_state.puntos_totales}/100")
    col2.metric("Perfectos", st.session_state.ejercicios_perfectos)
    col3.metric("Con errores", st.session_state.ejercicios_erroneos)
    
    if st.session_state.puntos_totales >= 70:
        st.success("¡Excelente trabajo! Has demostrado un gran dominio.")
    else:
        st.warning("Sigue practicando para pulir esos detalles.")
    st.button("Nueva Serie de 10", on_click=reset_total)
    st.stop()

a, b, c = st.session_state.a, st.session_state.b, st.session_state.c

st.title("Módulo de Despeje: Variable Dependiente")
st.write(f"**Ejercicio {st.session_state.contador_ejercicios + 1} de 10**")
st.info(f"**Ecuación Inicial:** {fmt_c(a, 'x')} {'+' if b > 0 else ''} {fmt_c(b, 'y')} = {c}")

# --- FLUJO DE PASOS ---
if st.session_state.paso == 1:
    st.subheader("Paso 1: Identificación")
    resp = st.radio("¿Cuál es la variable dependiente?", ["...", "x", "y"])
    if st.button("Comprobar"):
        if resp == "y":
            st.session_state.paso = 2
            st.rerun()
        else:
            st.session_state.error_en_actual = True
            st.error("Identificación incorrecta. Despejamos 'y' ☹️")

elif st.session_state.paso == 2:
    st.subheader("Paso 2: Neutralizar término")
    inst = st.text_input("¿Qué monomio sumamos o restamos?")
    if st.button("Aplicar"):
        target = fmt_c(-a, 'x').lower().replace("+", "")
        ingreso = inst.lower().replace(" ", "").replace("+", "")
        if ingreso == target:
            st.session_state.paso = 3
            st.rerun()
        else:
            st.session_state.error_en_actual = True
            st.warning(f"Intento fallido ☹️. El término {fmt_c(a, 'x')} requiere su opuesto para anularse.")

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
        opcs = [correcta, f"{fmt_c(b, 'y')} = {c} {fmt_c(a, 'x', incluir_mas=True)}", f"{b}y = {c-a}x"]
        random.shuffle(opcs)
        st.session_state.opciones_paso3 = opcs

    res_sel = st.radio("¿Cuál es el resultado?", st.session_state.opciones_paso3)
    if st.button("Verificar"):
        if res_sel == f"{fmt_c(b, 'y')} = {c} {monomio_op}":
            st.session_state.paso = 4
            st.rerun()
        else:
            st.session_state.error_en_actual = True
            st.error("Resultado incorrecto en la reducción ☹️")

elif st.session_state.paso == 4:
    st.subheader("Paso 4: El Coeficiente")
    st.latex(f"{fmt_c(b, 'y')} = {c} {fmt_c(-a, 'x', incluir_mas=True)}")
    op_div = st.selectbox("¿Por cuánto dividimos?", ["...", f"{b}", f"{-b}"], index=0)
    if st.button("Siguiente"):
        if op_div == f"{b}":
            st.session_state.paso = 5
            st.rerun()
        else:
            st.session_state.error_en_actual = True
            st.error(f"Error al elegir el divisor ☹️")

elif st.session_state.paso == 5:
    st.subheader("Paso 5: Resultado Final")
    st.latex(rf"y = \frac{{{c}}}{{{b}}} \frac{{{fmt_c(-a, 'x', incluir_mas=True)}}}{{{b}}}")
    
    m = Fraction(-a, b)
    inter = Fraction(c, b)
    txt_correcta = f"y = {fmt_c(m, 'x')} {'+' if inter > 0 else ''} {inter}"
    
    if not st.session_state.opciones_paso5:
        opcs = [txt_correcta, f"y = {fmt_c(-m, 'x')} {'+' if inter > 0 else ''} {inter}", f"y = {fmt_c(m, 'x')} - {abs(inter)}"]
        random.shuffle(opcs)
        st.session_state.opciones_paso5 = opcs

    res_final = st.radio("Ecuación final:", st.session_state.opciones_paso5, disabled=st.session_state.finalizado)
    
    if not st.session_state.finalizado:
        if st.button("Finalizar Ejercicio"):
            st.session_state.finalizado = True
            st.session_state.contador_ejercicios += 1
            
            if res_final == txt_correcta and not st.session_state.error_en_actual:
                st.balloons()
                st.success("¡Perfecto! Todo el proceso fue impecable. +10 puntos")
                st.session_state.ejercicios_perfectos += 1
                st.session_state.puntos_totales += 10
            else:
                st.error(f"Ejercicio con errores. 0 puntos ☹️")
                if res_final != txt_correcta:
                    st.info(f"La simplificación correcta era: {txt_correcta}")
                st.session_state.ejercicios_erroneos += 1
            st.rerun()
    else:
        st.button("Continuar al siguiente", on_click=reiniciar_ejercicio)
