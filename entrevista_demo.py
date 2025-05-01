import streamlit as st
import openai
import json

# Cargar preguntas
with open("estructura_preguntas_demo.json", encoding="utf-8") as f:
    preguntas = json.load(f)

st.title("Entrevista Demo - Grupo Gómez")
st.write("Por favor, responde a las siguientes preguntas con sinceridad.")

respuestas_usuario = []

for i, item in enumerate(preguntas):
    st.subheader(f"Pregunta {i + 1}")
    st.write(item["pregunta"])
    respuesta = st.text_area(f"Tu respuesta a la pregunta {i + 1}", key=f"respuesta_{i}")
    respuestas_usuario.append({"pregunta": item["pregunta"], "respuesta": respuesta, "respuestas_tipo": item["respuestas_tipo"]})

if st.button("Evaluar respuestas"):
    client = openai.OpenAI(api_key=st.secrets["openai_api_key"])
    resultados = []

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
            resultado = response.choices[0].message.content
        except Exception as e:
            resultado = f"Error al evaluar: {e}"

        resultados.append({"pregunta": item['pregunta'], "evaluacion": resultado})

    st.subheader("Resultados")
    for i, resultado in enumerate(resultados):
        st.markdown(f"**Pregunta {i + 1}:** {resultado['pregunta']}")
        st.text_area("Evaluación GPT", resultado['evaluacion'], height=120, key=f"resultado_{i}")