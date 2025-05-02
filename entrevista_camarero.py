import streamlit as st
import openai
import json
import time
from datetime import datetime
from enviar_a_monday import enviar_a_monday
from PIL import Image
import re

st.set_page_config(page_title="Entrevista Camarero", layout="centered")

logo = Image.open("logo gg.png")
st.image(logo, use_container_width=True)

st.title("Entrevista Camarero")

if "page" not in st.session_state:
    st.session_state.page = 0
    st.session_state.respuestas = []
    st.session_state.puntuaciones = []
    st.session_state.evaluaciones = []
    st.session_state.tiempos = []
    st.session_state.start_time = time.time()

with open("estructura_preguntas_camarero.json", encoding="utf-8") as f:
    preguntas = json.load(f)

if st.session_state.page == 0:
    st.subheader("Datos del candidato")
    st.session_state.nombre = st.text_input("Nombre completo")
    st.session_state.telefono = st.text_input("Teléfono de contacto")
    st.session_state.email = st.text_input("Correo electrónico")

    st.subheader("Domicilio")
    st.session_state.via = st.selectbox("Tipo de vía", ["Calle", "Avenida", "Plaza", "Camino", "Carretera", "Otra"])
    st.session_state.nombre_calle = st.text_input("Nombre de la calle")
    st.session_state.numero = st.text_input("Número")
    st.session_state.puerta = st.text_input("Puerta / Piso")
    st.session_state.cp = st.text_input("Código Postal")
    st.session_state.ciudad = st.text_input("Ciudad")

    if st.button("Comenzar entrevista"):
        st.session_state.page = 1
        st.session_state.start_time = time.time()
        st.experimental_rerun()

elif 1 <= st.session_state.page <= len(preguntas):
    actual = preguntas[st.session_state.page - 1]
    st.subheader(f"{actual['categoria']} - Pregunta {st.session_state.page}")
    st.write(actual["pregunta"])

    respuesta = st.text_area("Tu respuesta", key=f"respuesta_{st.session_state.page}")
    st.caption("⏱ Tiempo máximo para esta respuesta: 120 segundos")

    if st.button("Enviar respuesta"):
        tiempo_transcurrido = int(time.time() - st.session_state.start_time)
        st.session_state.respuestas.append({
            "pregunta": actual["pregunta"],
            "respuesta": respuesta,
            "respuestas_tipo": actual["respuestas_tipo"],
            "categoria": actual["categoria"]
        })
        st.session_state.tiempos.append(tiempo_transcurrido)
        st.session_state.page += 1
        st.session_state.start_time = time.time()

else:
    with st.spinner("Evaluando respuestas..."):
        client = openai.OpenAI(api_key=st.secrets["openai_api_key"])
        total_puntos = 0

        for r in st.session_state.respuestas:
            prompt = f"Pregunta: {r['pregunta']}\n\nRespuestas tipo:\n"
            for clave, valor in r["respuestas_tipo"].items():
                prompt += f"{clave}. {valor}\n"
            prompt += f"\nRespuesta del candidato:\n{r['respuesta']}\n\nDevuelve:\n- Puntuación\n- Respuesta tipo más cercana\n- Justificación breve"

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un evaluador objetivo."},
                        {"role": "user", "content": prompt}
                    ]
                )
                result_text = response.choices[0].message.content
            except Exception as e:
                result_text = f"Error: {e}"

            try:
                match = re.search(r"\b(10|[2-9])\b", result_text)
                puntuacion = int(match.group(1)) if match else 0
            except:
                puntuacion = 0

            st.session_state.puntuaciones.append(puntuacion)
            st.session_state.evaluaciones.append(result_text[:500])
            total_puntos += puntuacion

        resumen = " ".join(st.session_state.evaluaciones)
        tiempo_total = sum(st.session_state.tiempos)

        telefono_final = st.session_state.telefono.strip()
        if not telefono_final.startswith("+"):
            telefono_final = "+34 " + telefono_final

        enviar_a_monday(
            nombre=st.session_state.nombre,
            puesto="Camarero",
            puntuacion_total=total_puntos,
            evaluacion_texto=resumen,
            correo_entrevistador=None,
            puntuaciones=st.session_state.puntuaciones,
            evaluaciones=st.session_state.evaluaciones,
            tiempo_total=tiempo_total,
            telefono=telefono_final,
            email=st.session_state.email,
            via=st.session_state.via,
            calle=st.session_state.nombre_calle,
            numero=str(st.session_state.numero),
            puerta=str(st.session_state.puerta),
            cp=str(st.session_state.cp),
            ciudad=st.session_state.ciudad
        )

        st.success("✅ Entrevista registrada correctamente.")
        st.markdown("Gracias por completar tu entrevista. Nos pondremos en contacto contigo.")