import streamlit as st
import openai
import json
from datetime import datetime
from enviar_a_monday import enviar_a_monday
from PIL import Image
import re

st.set_page_config(page_title="Entrevista Camarero (Final)", layout="centered")

# Mostrar logo
logo = Image.open("logo gg.png")
st.image(logo, use_container_width=True)

st.title("Entrevista Camarero")
st.write("Por favor, completa tus datos personales antes de comenzar la entrevista.")

# Datos personales
nombre = st.text_input("Nombre completo")
telefono = st.text_input("Teléfono de contacto")
email = st.text_input("Correo electrónico")

st.subheader("Domicilio")
via = st.selectbox("Tipo de vía", ["Calle", "Avenida", "Plaza", "Camino", "Carretera", "Otra"])
nombre_calle = st.text_input("Nombre de la calle")
numero = st.text_input("Número")
puerta = st.text_input("Puerta / Piso")
cp = st.text_input("Código Postal")
ciudad = st.text_input("Ciudad")

# Cargar estructura de preguntas
with open("estructura_preguntas_camarero.json", encoding="utf-8") as f:
    preguntas = json.load(f)

respuestas_usuario = []

for i, item in enumerate(preguntas):
    st.subheader(f"{item['categoria']} - Pregunta {i + 1}")
    st.write(item["pregunta"])
    respuesta = st.text_area(f"Tu respuesta", key=f"respuesta_{i}")
    respuestas_usuario.append({
        "categoria": item["categoria"],
        "pregunta": item["pregunta"],
        "respuesta": respuesta,
        "respuestas_tipo": item["respuestas_tipo"]
    })

if st.button("Evaluar entrevista"):
    if not all([nombre, telefono, email, nombre_calle, numero, cp, ciudad]):
        st.warning("⚠️ Por favor, completa todos los datos personales obligatorios.")
    else:
        client = openai.OpenAI(api_key=st.secrets["openai_api_key"])
        resultados = []
        puntuaciones = []
        evaluaciones = []
        puntuacion_total = 0

        for i, item in enumerate(respuestas_usuario):
            prompt = f"""
Eres un evaluador de entrevistas para Grupo Gómez SL.

Pregunta:
{item['pregunta']}

Respuestas tipo:
"""
            for clave, valor in item["respuestas_tipo"].items():
                prompt += f"{clave}. {valor}\n"
            prompt += f"""

Respuesta del candidato:
{item['respuesta']}

Devuelve solo:
- Puntuación (número)
- Número de respuesta tipo más similar
- Justificación breve
"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un evaluador preciso y objetivo."},
                        {"role": "user", "content": prompt}
                    ]
                )
                resultado_texto = response.choices[0].message.content
            except Exception as e:
                resultado_texto = f"Error al evaluar: {e}"

            try:
                match = re.search(r"\b(10|[2-9])\b", resultado_texto)
                puntuacion = int(match.group(1)) if match else 0
            except:
                puntuacion = 0

            puntuaciones.append(puntuacion)
            evaluaciones.append(resultado_texto[:500])
            puntuacion_total += puntuacion

            resultados.append({
                "categoria": item["categoria"],
                "pregunta": item["pregunta"],
                "evaluacion": resultado_texto,
                "puntuacion": puntuacion
            })

        resumen_general = " ".join([r['evaluacion'] for r in resultados])
        respuesta_monday = enviar_a_monday(
            nombre=nombre,
            puesto="Camarero",
            puntuacion_total=puntuacion_total,
            evaluacion_texto=resumen_general,
            correo_entrevistador=None,
            puntuaciones=puntuaciones,
            evaluaciones=evaluaciones
        )
        st.success("✅ Entrevista registrada en Monday.com")
        st.markdown("Gracias por completar tu entrevista. Pronto nos pondremos en contacto contigo.")