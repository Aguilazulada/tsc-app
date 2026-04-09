import streamlit as st
import gspread
import json
import pandas as pd
from google.oauth2.service_account import Credentials
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    # El truco: strict=False permite que el JSON sea más flexible
    raw_creds = st.secrets["google_credentials"]
    if isinstance(raw_creds, str):
        creds_dict = json.loads(raw_creds, strict=False)
    else:
        creds_dict = dict(raw_creds)
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"❌ Error de acceso: {e}")
    st.info("Revisa que los Secrets tengan todas las comas y comillas.")
    st.stop()

# --- 2. INTERFAZ ---
st.title("🦅 Aguilazulada")
st.markdown("### Reporte Satelital y de Novedades")

nombre = st.text_input("👤 Reportado por:")
novedad = st.selectbox("📝 Seleccione Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

# FOTO (Como pediste, siempre presente)
st.write("---")
foto = st.file_uploader("📸 Evidencia Fotográfica", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, caption="Imagen cargada", use_container_width=True)

comentarios = st.text_area("💬 Detalles:")

st.write("---")

# --- 3. GPS Y MAPA ---
st.subheader("📍 Ubicación")
if st.button("📡 ACTIVAR GPS Y MAPA"):
    # Esto fuerza al navegador a pedir permiso
    loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', key='gps_final_hope')
    if loc:
        pos = json.loads(loc)
        st.session_state.lat = pos.get('latitude')
        st.session_state.lon = pos.get('longitude')

if 'lat' in st.session_state and st.session_state.lat:
    lat, lon = st.session_state.lat, st.session_state.lon
    st.success("✅ Coordenadas listas")
    
    # Dibujar mapa
    df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(df_mapa)
    
    # BOTÓN DE ENVÍO
    if st.button("🚀 ENVIAR AL EXCEL"):
        try:
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sheet.append_row([fecha, nombre, novedad, comentarios, lat, lon])
            st.balloons()
            st.success("¡Enviado con éxito al Google Sheet!")
        except Exception as e:
            st.error(f"Error al escribir en Excel: {e}")
else:
    st.warning("El mapa aparecerá cuando captures la ubicación.")

        
