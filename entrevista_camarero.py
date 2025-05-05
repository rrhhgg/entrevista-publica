import streamlit as st
import json
import time
from enviar_a_monday import enviar_a_monday

# Cargar preguntas desde archivo JSON
with open("estructura_preguntas_camarero.json", "r", encoding="utf-8") as f:
    estructura = json.load(f)

preguntas_generales = estructura["generales"]
preguntas_especificas = estructura["camarero"]

# Título y logo
st.image("logo gg.png", width=200)
st.title("Entrevista Camarero")

# Datos personales
if "pagina" not in st.session_state:
    st.session_state.pagina = 0

if "respuestas" not in st.session_state:
    st.session_state.respuestas = []

if "tiempos" not in st.session_state:
    st.session_state.tiempos = []

if st.session_state.pagina == 0:
    with st.form("form_datos"):
        st.subheader("📋 Datos del candidato")
        st.session_state.nombre = st.text_input("Nombre completo")
        st.session_state.telefono = st.text_input("Teléfono")
        st.session_state.correo = st.text_input("Correo electrónico")
        st.session_state.via = st.selectbox("Tipo de vía", ["Calle", "Avenida", "Plaza", "Camino"])
        st.session_state.nombre_via = st.text_input("Nombre de la vía")
        st.session_state.numero = st.text_input("Número")
        st.session_state.puerta = st.text_input("Puerta")
        st.session_state.cp = st.text_input("Código postal")
        st.session_state.ciudad = st.text_input("Ciudad")

        enviado = st.form_submit_button("Comenzar entrevista")
        if enviado:
            st.session_state.pagina += 1
            st.session_state.start_time = time.time()
            st.experimental_rerun()

# Función para mostrar cada pregunta
def mostrar_pregunta(indice, texto_pregunta):
    st.subheader(f"Pregunta {indice + 1}")
    respuesta = st.text_area(texto_pregunta)
    col1, col2 = st.columns([1, 3])
    with col1:
        enviar = st.button("Enviar respuesta", key=f"enviar_{indice}")
    tiempo_restante = 120 - int(time.time() - st.session_state.start_time)
    with col2:
        st.markdown(f"⏱️ Tiempo restante: {max(tiempo_restante, 0)} segundos")
    if enviar:
        tiempo_usado = int(time.time() - st.session_state.start_time)
        st.session_state.respuestas.append(respuesta)
        st.session_state.tiempos.append(tiempo_usado)
        st.session_state.pagina += 1
        st.session_state.start_time = time.time()
        st.experimental_rerun()

# Mostrar preguntas generales y específicas
total_preguntas = preguntas_generales + preguntas_especificas
indice_pregunta = st.session_state.pagina - 1
if 0 <= indice_pregunta < len(total_preguntas):
    mostrar_pregunta(indice_pregunta, total_preguntas[indice_pregunta])
elif st.session_state.pagina == len(total_preguntas) + 1:
    # Enviar a Monday
    respuestas = st.session_state.respuestas
    tiempos = st.session_state.tiempos
    total_puntos = 0
    evaluaciones = {}

    for i, r in enumerate(respuestas):
        prompt = f"Evalúa esta respuesta como si fueras un experto entrevistador: {r}. Da una puntuación de 0 a 10 y explica brevemente por qué."
        evaluacion = {"puntuacion": 7, "evaluacion": "Ejemplo de evaluación automática"}
        evaluaciones[i] = evaluacion
        total_puntos += evaluacion["puntuacion"]

    telefono_final = st.session_state.telefono.strip()
    if not telefono_final.startswith("+"):
        telefono_final = "+34 " + telefono_final

    enviar_a_monday(
        nombre=st.session_state.nombre,
        puesto="Camarero",
        puntuacion_total=total_puntos,
        evaluacion_texto="Resumen general",
        entrevistador_id=None,
        fecha_entrevista=None,
        respuestas_brutas=respuestas,
        evaluaciones=evaluaciones,
        telefono=telefono_final,
        correo=st.session_state.correo,
        via=st.session_state.via,
        nombre_via=st.session_state.nombre_via,
        numero=st.session_state.numero,
        puerta=st.session_state.puerta,
        cp=st.session_state.cp,
        ciudad=st.session_state.ciudad,
        tiempo_total=sum(tiempos)
    )

    st.success("✅ Entrevista registrada correctamente.")
    st.markdown("Gracias por participar.")
