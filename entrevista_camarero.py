import streamlit as st
import json
import time
from datetime import datetime
from enviar_a_monday import enviar_a_monday

st.set_page_config(page_title="Entrevista Camarero", layout="centered")

# Logo
st.image("logo gg.png", width=200)

# Iniciar variables de sesión
if "pagina" not in st.session_state:
    st.session_state.pagina = 0
if "respuestas" not in st.session_state:
    st.session_state.respuestas = []
if "tiempos" not in st.session_state:
    st.session_state.tiempos = []
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Cargar preguntas
with open("estructura_preguntas_camarero.json", encoding="utf-8") as f:
    estructura = json.load(f)

preguntas_generales = estructura["generales"]
preguntas_especificas = estructura["camarero"]
total_preguntas = len(preguntas_generales) + len(preguntas_especificas)

# Página 0: Datos personales
if st.session_state.pagina == 0:
    st.title("Entrevista Camarero")

    st.subheader("📋 Datos del Candidato")
    st.session_state.nombre = st.text_input("Nombre completo")
    st.session_state.telefono = st.text_input("Teléfono")
    st.session_state.correo = st.text_input("Correo electrónico")
    
    vias = ["Calle", "Avenida", "Plaza", "Camino"]
    st.session_state.via = st.selectbox("Vía", vias)
    st.session_state.nombre_via = st.text_input("Nombre de la vía")
    st.session_state.numero = st.number_input("Número", step=1)
    st.session_state.puerta = st.text_input("Puerta")
    st.session_state.cp = st.number_input("Código Postal", step=1)
    st.session_state.ciudad = st.text_input("Ciudad")

    if st.button("Comenzar Entrevista"):
        st.session_state.pagina = 1
        st.session_state.start_time = time.time()

# Páginas 1 a n: Preguntas
else:
    indice = st.session_state.pagina - 1
    todas_preguntas = preguntas_generales + preguntas_especificas

    if indice < total_preguntas:
        pregunta_actual = todas_preguntas[indice]
        st.subheader(f"Pregunta {indice+1} de {total_preguntas}")
        st.markdown(f"⏱️ **Tiempo máximo para responder: 120 segundos**")
        respuesta = st.text_area(pregunta_actual)
        tiempo_actual = time.time()

        if st.button("Siguiente"):
            tiempo_tardado = round(tiempo_actual - st.session_state.start_time)
            st.session_state.tiempos.append(tiempo_tardado)
            st.session_state.respuestas.append(respuesta)
            st.session_state.pagina += 1
            st.session_state.start_time = time.time()

    # Página final
    else:
        st.success("✅ Entrevista completada. Gracias por tu tiempo.")
        tiempo_total = sum(st.session_state.tiempos)

        # Envío a Monday
        telefono_final = st.session_state.telefono.strip()
        if not telefono_final.startswith("+"):
            telefono_final = "+34 " + telefono_final

        enviar_a_monday(
            nombre=st.session_state.nombre,
            puesto="Camarero",
            puntuacion_total=0,  # ya calculado antes en versión completa
            evaluacion_texto="(resumen generado aquí)",
            entrevistador_id=44226316,
            fecha=datetime.today().strftime("%Y-%m-%d"),
            respuestas=st.session_state.respuestas,
            evaluaciones=["(evaluaciones individuales)"] * total_preguntas,
            tiempos=st.session_state.tiempos,
            tiempo_total=tiempo_total,
            via=st.session_state.via,
            nombre_via=st.session_state.nombre_via,
            numero=st.session_state.numero,
            puerta=st.session_state.puerta,
            cp=st.session_state.cp,
            ciudad=st.session_state.ciudad,
            telefono=telefono_final,
            correo=st.session_state.correo
        )

        st.stop()