import requests
import json
import streamlit as st

def enviar_a_monday(
    nombre,
    puesto,
    puntuacion_total,
    evaluacion_texto,
    fecha_actual,
    entrevistador_id,
    respuestas_puntuaciones,
    respuestas_evaluaciones,
    datos_personales,
    tiempo_total
):
    api_url = "https://api.monday.com/v2"
    headers = {
        "Authorization": st.secrets["monday_api_key"],
        "Content-Type": "application/json"
    }

    column_values = {
        "dropdown_mkqhgq7t": {"labels": [puesto]},
        "date": {"date": fecha_actual},
        "numeric_mkqhfqy3": puntuacion_total,
        "text_mkqhc1ck": evaluacion_texto,
        "multiple_person_mkqhdm94": {"personsAndTeams": [{"id": entrevistador_id, "kind": "person"}]},
        "dropdown_mkqjbykm": {"labels": [datos_personales["via"]]},
        "text_mkqjmeh1": datos_personales["nombre_via"],
        "numeric_mkqjjj0g": int(datos_personales["numero"]),
        "text_mkqjwkmz": datos_personales["puerta"],
        "numeric_mkqjwczq": int(datos_personales["cp"]),
        "text_mkqjx0sz": datos_personales["ciudad"],
        "phone_mkqjgqhj": {"phone": datos_personales["telefono"]},
        "email_mkqjt99t": {"email": datos_personales["correo"]},
        "numeric_mkqjs2kq": tiempo_total
    }

    column_values.update(respuestas_puntuaciones)
    column_values.update(respuestas_evaluaciones)

    query = """
    mutation ($itemName: String!, $columnVals: JSON!) {
      create_item (
        board_id: 4459466340,
        item_name: $itemName,
        column_values: $columnVals
      ) {
        id
      }
    }
    """

    variables = {
        "itemName": nombre,
        "columnVals": json.dumps(column_values)
    }

    data = {"query": query, "variables": variables}
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()
