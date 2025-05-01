import streamlit as st
from PIL import Image

st.set_page_config(page_title="Selector de entrevista", layout="centered")

# Mostrar logo
logo = Image.open("logo gg.png")
st.image(logo, use_container_width=True)

st.title("Selecciona el tipo de entrevista")
st.markdown("Elige el puesto para comenzar la evaluación:")

# Diccionario de botones
opciones = {
    "🍽️ Camarero": "https://rrhhgg-entrevista-publica.streamlit.app",
    "🔪 Cocinero": None,
    "👨‍🍳 Jefe de Cocina": None,
    "👔 Director": None,
    "🧼 Friegaplatos": None,
    "🚚 Repartidor": None,
    "👩‍✈️ Hostess": None
}

# Mostrar los botones en filas de 3
cols = st.columns(3)
i = 0
for nombre, enlace in opciones.items():
    col = cols[i % 3]
    if enlace:
        col.markdown(
            f'<a href="{enlace}" target="_blank">'
            f'<button style="width:100%;padding:0.75em;font-size:1.1em;">{nombre}</button></a>',
            unsafe_allow_html=True
        )
    else:
        col.button(nombre, disabled=True)
    i += 1