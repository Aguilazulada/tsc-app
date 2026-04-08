import streamlit as st
import gspread
import json
import pandas as pd
from google.oauth2.service_account import Credentials
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
raw_creds = st.secrets["google_credentials"]
creds_dict = json.loads(raw_creds) if isinstance(raw_creds, str) else dict(raw_creds)
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# --- 2. INTERFAZ AGUILAZULADA ---
st.title("🦅 Aguilazulada")

# Formulario rápido
nombre = st.text_input("👤 Reportado por:")
novedad = st.selectbox("📝 Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

if novedad == "Street food":
    foto = st.file_uploader("📸 Sube foto de la comida", type=["jpg", "png"])
comentarios = st.text_area("💬 Detalles:")

st.write("---")

# --- 3. EL GPS Y EL MAPA ---
st.subheader("📍 Ubicación en Tiempo Real")

# Botón manual para forzar al navegador a soltar el GPS
if st.button("📡 CAPTURAR UBICACIÓN AHORA"):
    # Esta línea "despierta" al satélite
    loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', key='gps_final_v5')
    
    if loc:
        pos = json.loads(loc)
        st.session_state.lat = pos.get('latitude')
        st.session_state.lon = pos.get('longitude')

# Si ya tenemos los números, mostramos el mapa
if 'lat' in st.session_state and st.session_state.lat:
    lat, lon = st.session_state.lat, st.session_state.lon
    st.success(f"✅ Ubicación fijada en el mapa")
    
    # Dibujamos el mapa
    df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(df_mapa)
    
    # Botón de envío que solo aparece si hay GPS
    if st.button("🚀 ENVIAR REPORTE AL EXCEL"):
        try:
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sheet.append_row([fecha, nombre, novedad, comentarios, lat, lon])
            st.balloons()
            st.success("¡Datos y mapa guardados!")
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.warning("⚠️ El mapa aparecerá aquí cuando presiones el botón de arriba y permitas el acceso.")




