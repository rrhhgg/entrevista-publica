import streamlit as st
import time
from enviar_a_monday import enviar_a_monday

st.set_page_config(page_title="Entrevista Camarero", layout="centered")

# Función para manejar navegación
def avanzar_pagina():
    st.session_state.pagina += 1
    st.session_state.start_time = time.time()

# Inicializar variables de estado
if "pagina" not in st.session_state:
    st.session_state.pagina = 0
    st.session_state.tiempos = []
    st.session_state.start_time = time.time()

pag = st.session_state.pagina

# Página 0: datos personales
if pag == 0:
    st.title("Entrevista Camarero")
    st.subheader("Datos personales del candidato")

    st.session_state.nombre = st.text_input("Nombre completo")
    st.session_state.telefono = st.text_input("Teléfono")
    st.session_state.correo = st.text_input("Correo electrónico")
    st.session_state.via = st.selectbox("Tipo de vía", ["Calle", "Avenida", "Plaza"])
    st.session_state.nombre_via = st.text_input("Nombre de la vía")
    st.session_state.numero = st.text_input("Número")
    st.session_state.puerta = st.text_input("Puerta")
    st.session_state.cp = st.text_input("Código Postal")
    st.session_state.ciudad = st.text_input("Ciudad")

    if st.button("Comenzar entrevista"):
        avanzar_pagina()
        st.experimental_rerun()

# Página 1: Primera pregunta
elif pag == 1:
    st.subheader("Pregunta 1")
    respuesta = st.text_area("¿Por qué quieres trabajar con nosotros?")
    if st.button("Siguiente"):
        duracion = int(time.time() - st.session_state.start_time)
        st.session_state.tiempos.append(duracion)
        avanzar_pagina()
        st.experimental_rerun()

# Página final: envío
elif pag == 2:
    tiempo_total = sum(st.session_state.tiempos)
    telefono_final = st.session_state.telefono
    if not telefono_final.startswith("+"):
        telefono_final = "+34 " + telefono_final

    enviar_a_monday(
        nombre=st.session_state.nombre,
        puesto="Camarero",
        puntuacion_total=10,
        evaluacion="Ejemplo de evaluación",
        p1_generales=10,
        p1_generales_eval="Respuesta correcta",
        telefono=telefono_final,
        correo=st.session_state.correo,
        via=st.session_state.via,
        nombre_via=st.session_state.nombre_via,
        numero=st.session_state.numero,
        puerta=st.session_state.puerta,
        cp=st.session_state.cp,
        ciudad=st.session_state.ciudad,
        tiempo=tiempo_total
    )

    st.success("✅ Entrevista registrada correctamente. ¡Gracias!")