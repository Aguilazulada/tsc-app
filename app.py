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
    # Este bloque limpia cualquier salto de línea rebelde en el secreto
    raw_creds = st.secrets["google_credentials"]
    if isinstance(raw_creds, str):
        creds_dict = json.loads(raw_creds, strict=False)
    else:
        creds_dict = dict(raw_creds)
    
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"❌ Error crítico de configuración: {e}")
    st.stop()

# --- 2. INTERFAZ AGUILAZULADA ---
st.title("🦅 Aguilazulada")
st.markdown("### Reporte Operativo")

# Formulario
nombre = st.text_input("👤 Reportado por:", placeholder="Tu nombre")
novedad = st.selectbox("📝 Tipo de Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

# --- 📸 OPCIÓN DE FOTO (SIEMPRE VISIBLE) ---
st.write("---")
st.subheader("📸 Evidencia Fotográfica")
foto = st.file_uploader("Subir imagen (Opcional)", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, caption="Vista previa de la evidencia", use_container_width=True)

comentarios = st.text_area("💬 Detalles adicionales:")

st.write("---")

# --- 3. GPS Y MAPA ---
st.subheader("📍 Ubicación Satelital")

if st.button("🛰️ ACTIVAR GPS Y MOSTRAR MAPA"):
    # Activación manual para evitar bloqueos del navegador
    loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', key='gps_fixed')
    
    if loc:
        pos = json.loads(loc)
        st.session_state.lat = pos.get('latitude')
        st.session_state.lon = pos.get('longitude')

if 'lat' in st.session_state and st.session_state.lat:
    lat, lon = st.session_state.lat, st.session_state.lon
    st.success(f"✅ Satélite enlazado: {lat}, {lon}")
    
    # Mostrar Mapa
    df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(df_mapa)
    
    # --- BOTÓN DE ENVÍO FINAL ---
    if st.button("🚀 ENVIAR TODO AL EXCEL"):
        try:
            # Abrir la hoja por su nombre exacto
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Guardamos: Fecha, Nombre, Novedad, Detalles, Lat, Lon
            sheet.append_row([fecha, nombre, novedad, comentarios, lat, lon])
            st.balloons()
            st.success("¡Misión cumplida! Datos y ubicación guardados.")
        except Exception as e:
            st.error(f"Error al escribir en el Excel: {e}")
else:
    st.warning("⚠️ El mapa aparecerá aquí cuando captures la ubicación.")
