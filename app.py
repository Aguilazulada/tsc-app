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
    raw_creds = st.secrets["google_credentials"]
    # Si Streamlit ya lo leyó como dict, lo usamos; si es texto, lo convertimos
    creds_dict = json.loads(raw_creds) if isinstance(raw_creds, str) else dict(raw_creds)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"❌ Error de configuración: {e}")

# --- 2. INTERFAZ AGUILAZULADA ---
st.title("🦅 Aguilazulada")

nombre = st.text_input("👤 Reportado por:")
novedad = st.selectbox("📝 Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

# --- FOTO (SIEMPRE DISPONIBLE) ---
st.write("---")
foto = st.file_uploader("📸 Adjuntar Foto (Evidencia)", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, caption="Vista previa", use_container_width=True)

comentarios = st.text_area("💬 Detalles del reporte:")

st.write("---")

# --- 3. GPS Y MAPA ---
st.subheader("📍 Ubicación Satelital")

if st.button("📡 CAPTURAR UBICACIÓN Y VER MAPA"):
    # Esto despierta el GPS del navegador
    loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', key='gps_vFinal')
    
    if loc:
        pos = json.loads(loc)
        st.session_state.lat = pos.get('latitude')
        st.session_state.lon = pos.get('longitude')

if 'lat' in st.session_state and st.session_state.lat:
    lat, lon = st.session_state.lat, st.session_state.lon
    st.success("✅ GPS Conectado")
    
    # Dibujar mapa
    df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(df_mapa)
    
    # BOTÓN DE ENVÍO
    if st.button("🚀 ENVIAR REPORTE AL EXCEL"):
        try:
            # Asegúrate que el nombre del Excel sea exacto
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sheet.append_row([fecha, nombre, novedad, comentarios, lat, lon])
            st.balloons()
            st.success("¡Misión cumplida! Datos guardados.")
        except Exception as e:
            st.error(f"Error al guardar en Excel: {e}")
else:
    st.warning("Presiona el botón 'Capturar Ubicación' para ver el mapa.")
