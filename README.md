import streamlit as st
import random

# --- CONFIGURACIÓN DE PÁGINA Y ESTÉTICA ---
st.set_page_config(page_title="Matemáticas Fabio Molano", layout="centered")

# CSS para colores personalizados (Azul y Dorado)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1 { color: #003366; } /* Azul oscuro */
    .stButton>button {
        background-color: #003366;
        color: #FFD700; /* Dorado */
        border-radius: 10px;
        border: 2px solid #FFD700;
    }
    .sidebar .sidebar-content { background-color: #f0f2f6; }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (MENÚ) ---
with st.sidebar:
    # Intenta cargar el logo si lo subes a GitHub con el nombre 'logo.png'
    try:
        st.image("logo.png", width=200)
    except:
        st.write("### Matemáticas Fabio Molano")
    
    st.title("Menú de Módulos")
    modulo = st.radio("Selecciona un tema:", 
                     ["1. Módulo de Despeje", "2. Módulo Gráfico (Próximamente)", "3. Modelamiento"])

# --- LÓGICA DEL MÓDULO DE DESPEJE ---
if "1." in modulo:
    st.title("Módulo de Despeje: Variable Dependiente")
    
    # Inicializar ejercicio
    if 'ejercicio' not in st.session_state:
        st.session_state.a = random.randint(2, 6)
        st.session_state.b = random.randint(-6, -2) # Aseguramos negativo para practicar
        st.session_state.c = random.randint(10, 30)
        st.session_state.paso = 1
        st.session_state.ejercicio = True

    a, b, c = st.session_state.a, st.session_state.b, st.session_state.c

    st.info(f"**Ecuación a resolver:**  {a}x {b}y = {c}")

    # PASO 1: Identificar Variable
    if st.session_state.paso == 1:
        st.subheader("Paso 1: Identificación")
        resp1 = st.radio("¿Cuál es la variable dependiente?", ["Selecciona...", "x", "y", "El término independiente"], index=0)
        if st.button("Comprobar"):
            if resp1 == "y":
                st.success("¡Excelente! 'y' es la variable que depende de 'x'.")
                st.session_state.paso = 2
                st.rerun()
            else:
                st.error("Recuerda que en una función lineal, buscamos dejar la 'y' sola.")

    # PASO 2: Mover término x
    elif st.session_state.paso == 2:
        st.subheader("Paso 2: Aislamiento")
        st.write(f"Queremos mover el término **{a}x** al otro lado.")
        instruccion = st.text_input("¿Qué operación debes hacer a ambos lados?")
        st.caption("Ejemplo: resta 3x, sumar 2x...")

        if st.button("Verificar Paso"):
            # Limpiamos la respuesta del alumno para que sea flexible
            resp_limpia = instruccion.lower().replace(" ", "")
            if f"restar{a}x" in resp_limpia or f"resta{a}x" in resp_limpia or f"-{a}x" in resp_limpia:
                st.success(f"¡Muy bien! Restamos {a}x para anularlo a la izquierda.")
                st.session_state.paso = 3
                st.rerun()
            else:
                st.warning(f"Si el término es {a}x (positivo), ¿cómo lo neutralizas? Piensa en la operación inversa.")

    # PASO 3: División Final
    elif st.session_state.paso == 3:
        st.subheader("Paso 3: El Coeficiente")
        st.latex(f"{b}y = {c} - {a}x")
        st.write(f"La 'y' todavía está acompañada por el coeficiente **{b}**.")
        op_div = st.selectbox("Para despejar y, ¿por cuánto dividimos toda la ecuación?", 
                             ["Selecciona...", f"{abs(b)}", f"{b}", "1"])
        
        if st.button("Finalizar Despeje"):
            if op_div == f"{b}":
                st.balloons()
                st.success("¡LOGRADO! Has despejado la variable.")
                st.latex(f"y = \\frac{{{c} - {a}x}}{{{b}}}")
                if st.button("Hacer otro ejercicio"):
                    del st.session_state.ejercicio
                    st.rerun()
            else:
                st.error(f"¡Cuidado con el signo! Debes dividir exactamente por el coeficiente que ves: {b}")

else:
    st.title("Módulo en Construcción")
    st.write("Este módulo se activará en la siguiente fase de desarrollo.")# modulo-de-despeje2
