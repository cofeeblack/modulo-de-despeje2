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
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (MENÚ) ---
with st.sidebar:
    try:
        st.image("logo.png", width=200)
    except:
        st.write("### 🎓 Fabio Molano")
    
    st.title("Menú Principal")
    modulo = st.radio("Selecciona un tema:", 
                     ["1. Módulo de Despeje", "2. Módulo Gráfico (Próximamente)"])

# --- LÓGICA DEL MÓDULO DE DESPEJE ---
if "1." in modulo:
    st.title("Módulo de Despeje: Variable Dependiente")
    
    if 'ejercicio_id' not in st.session_state:
        # Generamos coeficientes que den resultados "interesantes"
        st.session_state.a = random.randint(1, 5)
        st.session_state.b = random.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        st.session_state.c = random.choice([6, 10, 12, 15, 20])
        st.session_state.paso = 1
        st.session_state.ejercicio_id = random.random()

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c

    st.info(f"**Ecuación:**  {a}x {'+' if b > 0 else ''}{b}y = {c}")

    # PASOS 1 Y 2 (IDENTIFICACIÓN Y TRANSPOSICIÓN)
    if st.session_state.paso == 1:
        resp1 = st.radio("¿Cuál es la variable dependiente?", ["Selecciona...", "x", "y"], index=0)
        if st.button("Comprobar"):
            if resp1 == "y":
                st.session_state.paso = 2
                st.rerun()

    elif st.session_state.paso == 2:
        instruccion = st.text_input(f"¿Qué operación haces con {a}x para moverlo?")
        if st.button("Verificar"):
            resp_limpia = instruccion.lower().replace(" ", "")
            if f"restar{a}x" in resp_limpia or f"resta{a}x" in resp_limpia or f"-{a}x" in resp_limpia:
                st.session_state.paso = 3
                st.rerun()

    # PASO 3: DIVISIÓN GENERAL
    elif st.session_state.paso == 3:
        st.latex(f"{b}y = {c} - {a}x")
        op_div = st.selectbox(f"¿Por cuánto dividimos toda la ecuación?", 
                             ["Selecciona...", f"{b}", f"{abs(b)}", "1"], index=0)
        if st.button("Siguiente"):
            if op_div == f"{b}":
                st.session_state.paso = 4
                st.rerun()

    # PASO 4: SIMPLIFICACIÓN Y SEPARACIÓN (NUEVO)
    elif st.session_state.paso == 4:
        st.subheader("Paso 4: Repartir la división")
        st.write("Ahora debemos dividir cada término por el coeficiente. ¿Cómo queda la ecuación simplificada?")
        
        # Cálculo de respuestas correctas (simplificando fracciones)
        m = Fraction(-a, b)
        interseptp = Fraction(c, b)
        
        correcta = f"y = {m}x {'+' if interseptp > 0 else ''} {interseptp}"
        error1 = f"y = {Fraction(a, b)}x + {interseptp}" # Error de signo en x
        error2 = f"y = {m}x - {interseptp}" # Error de signo en constante
        error3 = f"y = {Fraction(b, a)}x + {interseptp}" # Coeficiente invertido
        
        opciones = [correcta, error1, error2, error3]
        random.shuffle(opciones)
        
        seleccion = st.radio("Selecciona la forma simplificada correcta:", opciones)
        
        if st.button("Finalizar"):
            if seleccion == correcta:
                st.balloons()
                st.success(f"¡Perfecto! La ecuación final es: {correcta}")
                if st.button("¡Hacer otro ejercicio!"):
                    st.session_state.clear()
                    st.rerun()
            else:
                st.error("Revisa bien la ley de signos al dividir cada término.")
