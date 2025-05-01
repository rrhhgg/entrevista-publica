import streamlit as st
from PIL import Image
import base64

st.set_page_config(page_title="Selector de entrevista", layout="centered")

# Mostrar logo
logo = Image.open("logo gg.png")
st.image(logo, use_container_width=True)

st.title("Selecciona el tipo de entrevista")
st.markdown("Elige el puesto para comenzar la evaluación:")

# Diccionario de botones
opciones = {
    "🍽️ Camarero": "https://rrhhgg-entrevista-publica.streamlit.app",
    "🔪 Cocinero": "#",
    "👨‍🍳 Jefe de Cocina": "#",
    "👔 Director": "#",
    "🧼 Friegaplatos": "#",
    "🚚 Repartidor": "#",
    "👩‍✈️ Hostess": "#"
}

# Mostrar los botones
for nombre, enlace in opciones.items():
    if enlace != "#":
        st.markdown(f"[{nombre}](%s)" % enlace, unsafe_allow_html=True)
    else:
        st.button(nombre, disabled=True)