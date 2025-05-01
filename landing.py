import streamlit as st
from PIL import Image

st.set_page_config(page_title="Selector de entrevista", layout="centered")

# Mostrar logo
logo = Image.open("logo gg.png")
st.image(logo, use_container_width=True)

st.title("Selecciona el tipo de entrevista")
st.markdown("Elige el puesto para comenzar la evaluación:")

# Lista de opciones y sus enlaces
opciones = {
    "🍽️ Camarero": "https://rrhhgg-entrevista-publica.streamlit.app",
    "🔪 Cocinero": None,
    "👨‍🍳 Jefe de Cocina": None,
    "👔 Director": None,
    "🧼 Friegaplatos": None,
    "🚚 Repartidor": None,
    "👩‍✈️ Hostess": None
}

for nombre, enlace in opciones.items():
    if enlace:
        if st.button(nombre):
            st.markdown(f'<meta http-equiv="refresh" content="0; url={enlace}" />', unsafe_allow_html=True)
    else:
        st.button(nombre, disabled=True)