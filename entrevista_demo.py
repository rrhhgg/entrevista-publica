import streamlit as st
import openai
import json
from datetime import datetime
from enviar_a_monday import enviar_a_monday

# Cargar preguntas
with open("estructura_preguntas_demo.json", encoding="utf-8") as f:
    preguntas = json.load(f)

st.title("Entrevista Demo - Grupo Gómez")
st.write("Por favor, responde a las siguientes preguntas con sinceridad.")

# Datos del candidato
nombre = st.text_input("Nombre del candidato")
puesto = st.text_input("Puesto al que aplica (ej: Camarero)")

respuestas_usuario = []

for i, item in enumerate(preguntas):
    st.subheader(f"Pregunta {i + 1}")
    st.write(item["pregunta"])
    respuesta = st.text_area(f"Tu respuesta a la pregunta {i + 1}", key=f"respuesta_{i}")
    respuestas_usuario.append({
        "pregunta": item["pregunta"],
        "respuesta": respuesta,
        "respuestas_tipo": item["respuestas_tipo"]
    })

if st.button("Evaluar respuestas") and nombre and puesto:
    client = openai.OpenAI(api_key=st.secrets["openai_api_key"])
    resultados = []
    puntuacion_total = 0

    for item in respuestas_usuario:
        prompt = f"""
Eres un evaluador de entrevistas para el puesto de camarero en Grupo Gómez SL.
Evalúa la siguiente respuesta según estos ejemplos:

Pregunta: {item['pregunta']}

Respuestas tipo:
"""
        for num, texto in item["respuestas_tipo"].items():
            prompt += f"{num}. {texto}\n"

        prompt += f"""
Respuesta del candidato:
{item['respuesta']}

Devuelve:
- puntuacion (solo el número)
- número de respuesta tipo más similar
- justificación breve
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

        # Extraer puntuación si es posible
        try:
            lineas = resultado_texto.splitlines()
            puntuacion = int(next((l for l in lineas if l.strip().isdigit()), "0"))
        except:
            puntuacion = 0

        puntuacion_total += puntuacion
        resultados.append({"pregunta": item["pregunta"], "evaluacion": resultado_texto})

    st.subheader("Resultados")
    for i, resultado in enumerate(resultados):
        st.markdown(f"**Pregunta {i + 1}:** {resultado['pregunta']}")
        st.text_area("Evaluación GPT", resultado['evaluacion'], height=120, key=f"resultado_{i}")

    resumen = " ".join([r['evaluacion'] for r in resultados])
    enviar_a_monday(nombre=nombre, puesto=puesto, puntuacion_total=puntuacion_total, evaluacion_texto=resumen)
    st.success("✅ Entrevista registrada en Monday.com")
elif st.button("Evaluar respuestas"):
    st.warning("⚠️ Por favor, rellena el nombre y el puesto antes de continuar.")