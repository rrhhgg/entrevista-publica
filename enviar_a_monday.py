import requests
from datetime import datetime

# Función para enviar datos a Monday.com
def enviar_a_monday(nombre, puesto, puntuacion_total, evaluacion_texto):
    url = "https://api.monday.com/v2"
    headers = {
        "Authorization": "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI5NzQ5NDgyNCwiYWFpIjoxMSwidWlkIjo0NDIyNjMxNiwiaWFkIjoiMjAyMy0xMS0yMFQxNzowNjozNC4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MTY4ODEzMjIsInJnbiI6ImV1YzEifQ.o1cqRb0B9pGxLS2PQQbU4_RkQlhW3GhGVkGUV3xiCxI",
        "Content-Type": "application/json"
    }

    fecha_actual = datetime.today().strftime('%Y-%m-%d')
    evaluacion_texto = evaluacion_texto.replace('"', "'")[:500]

    query = {
        "query": f"""
            mutation {{
              create_item (
                board_id: 1939525964,
                item_name: "{nombre}",
                column_values: {{
                  \"texto\": "{puesto}",
                  \"fecha\": {{ \"date\": "{fecha_actual}" }},
                  \"números\": "{puntuacion_total}",
                  \"texto8\": "{evaluacion_texto}"
                }}
              ) {{
                id
              }}
            }}
        """
    }

    response = requests.post(url, json=query, headers=headers)
    return response.json()