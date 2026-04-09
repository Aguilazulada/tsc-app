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
    creds_dict = json.loads(raw_creds, strict=False) if isinstance(raw_creds, str) else dict(raw_creds)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"❌ Error de configuración: {e}")
    st.stop()

# --- 2. INTERFAZ ---
st.title("🦅 Aguilazulada (Beta)")

nombre = st.text_input("👤 Reportado por:", placeholder="Tu nombre")
novedad = st.selectbox("📝 Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

st.write("---")
# Mantenemos la foto que me pediste
foto = st.file_uploader("📸 Adjuntar Foto (Evidencia)", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, caption="Vista previa", use_container_width=True)

comentarios = st.text_area("💬 Detalles:")

st.write("---")

# --- 3. NUEVO SISTEMA DE GPS ---
st.subheader("📍 Localización Satelital")

# Botón que "obliga" al GPS a despertar
if st.button("🎯 CLIC AQUÍ PARA OBTENER UBICACIÓN"):
    # Esta es la instrucción que el celular NO puede ignorar
    loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => ({latitude: x.coords.latitude, longitude: x.coords.longitude}))))', key='gps_final_bolivia')
    
    if loc:
        pos = json.loads(loc)
        st.session_state.lat = pos.get('latitude')
        st.session_state.lon = pos.get('longitude')
        st.success("✅ ¡Coordenadas capturadas!")
    else:
        st.info("🛰️ Buscando señal... Si sale un aviso arriba en tu pantalla, dale a 'PERMITIR'.")

# Si ya tenemos la ubicación, mostramos el mapa y el botón de enviar
if 'lat' in st.session_state and st.session_state.lat:
    lat, lon = st.session_state.lat, st.session_state.lon
    
    # Dibujar el mapa
    df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(df_mapa)
    
    st.write("---")
    
    if st.button("🚀 ENVIAR REPORTE FINAL"):
        try:
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Guardamos todo en el Excel
            sheet.append_row([fecha, nombre, novedad, comentarios, lat, lon])
            st.balloons()
            st.success("¡Excelente! Los datos ya están en tu Google Sheet.")
        except Exception as e:
            st.error(f"Error al escribir en Excel: {e}")
else:
    st.warning("⚠️ El botón de 'Enviar' y el Mapa aparecerán cuando presiones el botón de 'Obtener Ubicación'.")
