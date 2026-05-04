import streamlit as st
import random

# Configuración de la página
st.title("Módulo de Despeje: Variable Dependiente")
st.write("Bienvenido a tu clase de matemáticas interactiva.")

# 1. Generar ejercicio aleatorio si no existe uno en la sesión
if 'a' not in st.session_state:
    st.session_state.a = random.randint(1, 9)
    st.session_state.b = random.randint(-9, -1) # Para que sea -By
    st.session_state.c = random.randint(1, 20)
    st.session_state.paso = 1

a, b, c = st.session_state.a, st.session_state.b, st.session_state.c

st.subheader(f"Ejercicio: Despeja 'y' en la ecuación: {a}x {b}y = {c}")

# PASO 1: Identificar variable
if st.session_state.paso == 1:
    var = st.radio("¿Cuál es la variable dependiente?", ["x", "y", "Ninguna"])
    if st.button("Comprobar"):
        if var == "y":
            st.success("¡Correcto! 'y' es la variable que queremos dejar sola.")
            st.session_state.paso = 2
            st.rerun()
        else:
            st.error("Recuerda: la variable dependiente suele ser 'y' en estas funciones.")

# PASO 2: Mover el término x
elif st.session_state.paso == 2:
    st.write(f"Ecuación actual: {a}x {b}y = {c}")
    pregunta = st.text_input(f"Para dejar solo el término con 'y', ¿qué debemos hacer con {a}x?")
    st.caption("Ejemplo: resta 2x, suma 5x...")
    
    if st.button("Verificar paso"):
        if f"-{a}x" in pregunta.lower() or f"restar {a}x" in pregunta.lower():
            st.success(f"¡Muy bien! Restamos {a}x a ambos lados.")
            st.write(f"Operación: ({a}x - {a}x) {b}y = {c} - {a}x")
            st.latex(f"{b}y = {c} - {a}x")
            st.session_state.paso = 3
            st.rerun()
        else:
            st.warning(f"Si tenemos {a}x positivo, para 'eliminarlo' necesitamos la operación opuesta.")

# PASO 3: Finalizar (Esto es un ejemplo corto)
elif st.session_state.paso == 3:
    st.write("¡Has avanzado mucho! Este es solo un prototipo.")
    if st.button("Nuevo ejercicio"):
        del st.session_state.a
        st.rerun()
