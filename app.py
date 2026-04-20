import streamlit as st
import simulador_uyunitec  # El archivo que creaste

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Aguilazulada Suite", layout="wide")

# --- MENÚ LATERAL (Esto es lo que crea la flechita) ---
with st.sidebar:
    st.title("🚀 Panel de Misión")
    seleccion = st.radio("Ir a:", ["Sistema Aguilazulada", "Simulador UyuniTec"])
    st.write("---")
    st.info("Desarrollado para el Altiplano Boliviano 🇧🇴")

# --- LÓGICA DE NAVEGACIÓN ---
if seleccion == "Sistema Aguilazulada":
    st.title("🦅 Sistema Aguilazulada")
    # Tu formulario original
    nombre = st.text_input("👤 Reportado por:")
    novedad = st.selectbox("📝 Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])
    detalles = st.text_area("💬 Detalles:")
    foto = st.file_uploader("📸 Adjuntar Foto", type=["jpg", "png", "jpeg"])
    if st.button("Enviar Reporte"):
        st.success("Reporte enviado correctamente")

elif seleccion == "Simulador UyuniTec":
    # Aquí llamamos a la función de tu otro archivo
    simulador_uyunitec.run_uyunitec_sim()


   
