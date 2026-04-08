import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD (Ya la dominas) ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
raw_creds = st.secrets["google_credentials"]
creds_dict = json.loads(raw_creds) if isinstance(raw_creds, str) else dict(raw_creds)
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# --- 2. INTERFAZ QUE TE GUSTABA ---
st.title("🦅 Aguilazulada")
st.markdown("### Formulario de Reporte Directo")

# Campos del formulario (ajústalos a tu gusto)
nombre = st.text_input("👤 Reportado por:")
comentarios = st.text_area("📝 Novedades:")

st.write("---")

# --- 3. EL GPS (El truco del botón) ---
st.subheader("📍 Localización")
st.info("Haz clic abajo para activar el GPS. Si sale un aviso arriba, dale a 'Permitir'.")

# Este botón es el que "obliga" al navegador a buscarte
if st.button("🛰️ CLIC AQUÍ PARA FIJAR UBICACIÓN"):
    loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', target_id='get_location')
    
    if loc:
        datos_gps = json.loads(loc)
        st.session_state.lat = datos_gps.get('latitude')
        st.session_state.lon = datos_gps.get('longitude')

# Si ya tenemos la ubicación en memoria, la mostramos
if 'lat' in st.session_state and st.session_state.lat:
    st.success(f"✅ Coordenadas listas: {st.session_state.lat}, {st.session_state.lon}")
    
    # --- BOTÓN DE ENVÍO FINAL ---
    if st.button("🚀 ENVIAR AL EXCEL"):
        try:
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Enviamos: Fecha, Nombre, Comentarios, Lat, Lon
            sheet.append_row([fecha, nombre, comentarios, st.session_state.lat, st.session_state.lon])
            st.balloons()
            st.success("¡Reporte guardado en el Google Sheet!")
        except Exception as e:
            st.error(f"Hubo un problema al guardar: {e}")
else:
    st.warning("Pendiente: Capturar ubicación satelital.")

