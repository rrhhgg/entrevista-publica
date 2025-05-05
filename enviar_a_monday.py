import requests
import json
import streamlit as st

def enviar_a_monday(nombre, puesto, fecha, puntuacion_total, evaluacion_general, entrevistador_id, respuestas, datos_personales, tiempo_total):
    api_key = st.secrets["monday_api_key"]
    board_id = st.secrets["monday_board_id"]

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    column_values = {
        "dropdown_mkqhgq7t": {"labels": [puesto]},
        "date": {"date": fecha},
        "numeric_mkqhfqy3": puntuacion_total,
        "text_mkqhc1ck": evaluacion_general,
        "multiple_person_mkqhdm94": {
            "personsAndTeams": [{"id": entrevistador_id, "kind": "person"}]
        },
        "dropdown_mkqjbykm": {"labels": [datos_personales["via"]]},
        "text_mkqjmeh1": datos_personales["nombre_via"],
        "numeric_mkqjjj0g": datos_personales["numero"],
        "text_mkqjwkmz": datos_personales["puerta"],
        "numeric_mkqjwczq": datos_personales["cp"],
        "text_mkqjx0sz": datos_personales["ciudad"],
        "phone_mkqjgqhj": {"phone": datos_personales["telefono"], "countryShortName": "es"},
        "email_mkqjt99t": {"email": datos_personales["correo"]},
        "numeric_mkqjs2kq": tiempo_total
    }

    column_values.update(respuestas)

    query = {
        "query": f"""
            mutation {{
              create_item (
                board_id: {board_id},
                item_name: "{nombre}",
                column_values: {json.dumps(json.dumps(column_values))}
              ) {{
                id
              }}
            }}
        """
    }

    response = requests.post("https://api.monday.com/v2", headers=headers, json=query)
    return response.json()
