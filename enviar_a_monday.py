import requests
import json
from datetime import datetime

# Diccionario de correo a ID de usuario en Monday
email_to_id = {
    "frmichelin@grupogomez.es": 44226316,
    "luismf@yurest.com": 44261508,
    "maria.martin@grupogomez.es": 44420699,
    "flopez@grupogomez.es": 44426590,
    "toni@grupogomez.es": 44809847,
    "eventos@grupogomez.es": 45524335,
    "mada.broton@grupogomez.es": 45825925,
    "puertadelmar@grupogomez.es": 46559570,
    "banderaazul@grupogomez.es": 46952448,
    "jose.gomez@grupogomez.es": 49221929,
    "v.gomez@grupogomez.es": 57454886,
    "analiavop@gmail.com": 59593922,
    "v.cobusneanu@grupogomez.es": 61979674,
    "s.garcia@grupogomez.es": 61979678,
    "m.demiguel@grupogomez.es": 62264901,
    "k.chapero@grupogomez.es": 63874482,
    "c.domenech@grupogomez.es": 67088572,
    "marcos@yurest.com": 69167992,
    "andreaplasenciav@gmail.com": 69175970,
    "implementacion@yurest.com": 69975594,
    "comercial@yurest.com": 70872920,
    "a.alandi@grupogomez.es": 71728482,
    "practicas@grupogomez.es": 75180558,
    "info@yurest.com": 75469023,
    "s.bayarri@yurest.com": 72907814,
    "soporte@yurest.com": 43341598
}

# Mapeo de columnas de Monday por número de pregunta (1-indexed)
columnas_puntos = [
    "numeric_mkqje1xr", "numeric_mkqj583y", "numeric_mkqjtmhs",
    "numeric_mkqjax81", "numeric_mkqj4hff", "numeric_mkqjx55q",
    "numeric_mkqjx2t", "numeric_mkqjyb6b", "numeric_mkqj34xs",
    "numeric_mkqjsyt6", "numeric_mkqjbvax"
]

columnas_eval = [
    "text_mkqjynvd", "text_mkqjq3x5", "text_mkqjvc1p",
    "text_mkqjtv3j", "text_mkqj5mt8", "text_mkqjqx0q",
    "text_mkqjbfd8", "text_mkqjx2qd", "text_mkqj998e",
    "text_mkqjks1c", "text_mkqjdwx5"
]

def enviar_a_monday(nombre, puesto, puntuacion_total, evaluacion_texto, correo_entrevistador, puntuaciones=[], evaluaciones=[]):
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI5NzQ5NDgyNCwiYWFpIjoxMSwidWlkIjo0NDIyNjMxNiwiaWFkIjoiMjAyMy0xMS0yMFQxNzowNjozNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTY4ODEzMjIsInJnbiI6ImV1YzEifQ.o1cqRb0B9pGxLS2PQQbU4_RkQlhW3GhGVkGUV3xiCxI",
        "Content-Type": "application/json"
    }

    persona_id = email_to_id.get(correo_entrevistador.strip().lower()) if correo_entrevistador else None
    fecha_actual = datetime.today().strftime('%Y-%m-%d')
    evaluacion_texto = evaluacion_texto.replace('"', "'")[:500]

    column_values = {
        "dropdown_mkqhgq7t": { "labels": [puesto] },
        "date": { "date": fecha_actual },
        "numeric_mkqhfqy3": puntuacion_total,
        "text_mkqhc1ck": evaluacion_texto
    }

    if persona_id:
        column_values["multiple_person_mkqhdm94"] = {
            "personsAndTeams": [{"id": persona_id, "kind": "person"}]
        }

    # Añadir columnas de puntuaciones y evaluaciones
    for i, valor in enumerate(puntuaciones):
        if i < len(columnas_puntos):
            column_values[columnas_puntos[i]] = valor

    for i, texto in enumerate(evaluaciones):
        if i < len(columnas_eval):
            column_values[columnas_eval[i]] = texto[:500]

    query = {
        "query": f"""
            mutation {{
              create_item (
                board_id: 1939525964,
                item_name: "{nombre}",
                column_values: {json.dumps(json.dumps(column_values))}
              ) {{
                id
              }}
            }}
        """
    }

    response = requests.post(url, json=query, headers=headers)
    return response.json()