import streamlit as st
from PIL import Image

st.set_page_config(page_title="Selector de entrevista", layout="centered")

# Mostrar logo
logo = Image.open("logo gg.png")
st.image(logo, use_container_width=True)

st.title("Selecciona el tipo de entrevista")
st.markdown("Elige el puesto para comenzar la evaluación:")

# Botones configurados
puestos = {
    "🍽️ Camarero": "https://rrhhgg-entrevista-publica.streamlit.app",
    "🔪 Cocinero": None,
    "👨‍🍳 Jefe de Cocina": None,
    "👔 Director": None,
    "🧼 Friegaplatos": None,
    "🚚 Repartidor": None,
    "👩‍✈️ Hostess": None
}

# Mostrar en filas de 3
cols = st.columns(3)
i = 0
for puesto, url in puestos.items():
    col = cols[i % 3]
    if url:
        col.link_button(puesto, url)
    else:
        col.button(puesto, disabled=True)
    i += 1