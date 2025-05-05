
import requests
import json
import datetime
import streamlit as st

def enviar_a_monday(
    nombre,
    puesto,
    puntuacion_total,
    evaluacion_texto,
    entrevistador_id,
    fecha_entrevista,
    respuestas_puntuaciones,
    respuestas_evaluaciones,
    telefono,
    correo,
    via,
    nombre_via,
    numero,
    puerta,
    cp,
    ciudad,
    tiempo_total
):
    api_key = st.secrets["monday_api_key"]
    board_id = st.secrets["monday_board_id"]

    # Construir el diccionario de valores para cada columna
    column_values = {
        "name": nombre,
        "multiple_person_mkqhdm94": {"personsAndTeams": [{"id": entrevistador_id, "kind": "person"}]},
        "dropdown_mkqhgq7t": {"labels": [puesto]},
        "date": {"date": fecha_entrevista},
        "numeric_mkqhfqy3": puntuacion_total,
        "text_mkqhc1ck": evaluacion_texto,
        "phone_mkqjgqhj": {"phone": telefono, "countryShortName": "ES"},
        "email_mkqjt99t": correo,
        "dropdown_mkqjbykm": {"label": via},
        "text_mkqjmeh1": nombre_via,
        "numeric_mkqjjj0g": numero,
        "text_mkqjwkmz": puerta,
        "numeric_mkqjwczq": cp,
        "text_mkqjx0sz": ciudad,
        "numeric_mkqjs2kq": tiempo_total
    }

    # Añadir dinámicamente las respuestas individuales (puntuaciones y evaluaciones)
    column_values.update(respuestas_puntuaciones)
    column_values.update(respuestas_evaluaciones)

    query = """
    mutation ($board_id: Int!, $item_name: String!, $column_values: JSON!) {
        create_item (board_id:$board_id, item_name:$item_name, column_values:$column_values) {
            id
        }
    }
    """

    variables = {
        "board_id": int(board_id),
        "item_name": nombre,
        "column_values": json.dumps(column_values)
    }

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(
        url="https://api.monday.com/v2",
        json={"query": query, "variables": variables},
        headers=headers
    )

    return response.json()
