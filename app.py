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
st.markdown("### Centro de Reportes en Tiempo Real")

nombre = st.text_input("👤 Reportado por:", placeholder="Tu nombre o alias")

# Menú de opciones solicitadas
novedad = st.selectbox("📝 Seleccione la Novedad:", 
                        ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

# Espacio para foto si es Street Food o si el usuario quiere
foto = None
if novedad == "Street food":
    st.info("🍔 ¡Dato gastronómico! Comparte una foto si puedes.")
    foto = st.file_uploader("📸 Foto del Street Food", type=["jpg", "png", "jpeg"])
else:
    if st.checkbox("¿Deseas adjuntar una foto al reporte?"):
        foto = st.file_uploader("📸 Seleccionar imagen", type=["jpg", "png", "jpeg"])

comentarios = st.text_area("💬 Detalles del reporte:", placeholder="Escribe aquí lo que está pasando...")

st.write("---")

# --- 3. EL MAPA Y EL GPS ---
st.subheader("📍 Ubicación Satelital")

# Captura de GPS
loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', key='gps_map_v4')

if loc:
    pos = json.loads(loc)
    lat = pos.get('latitude')
    lon = pos.get('longitude')
    
    if lat and lon:
        st.success(f"✅ Ubicación fijada: {lat}, {lon}")
        
        # --- AQUÍ ESTÁ EL MAPA ---
        # Creamos un pequeño cuadro de datos para el mapa
        map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_data)
        
        # --- BOTÓN DE ENVÍO FINAL ---
        if st.button("🚀 ENVIAR REPORTE AL EXCEL"):
            try:
                sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                # Guardamos: Fecha, Nombre, Novedad, Comentarios, Lat, Lon
                sheet.append_row([fecha, nombre, novedad, comentarios, lat, lon])
                st.balloons()
                st.success("¡Misión cumplida! El reporte y el mapa se han sincronizado.")
            except Exception as e:
                st.error(f"Error al conectar con el Excel: {e}")
    else:
        st.error("❌ El satélite respondió pero no envió coordenadas válidas.")
else:
    st.warning("🛰️ Buscando señal de GPS... Por favor, asegúrate de dar permiso de ubicación en el navegador.")
    st.caption("Si estás en PC, revisa el icono del candado 🔒 en la barra de direcciones.")

if st.button("🔄 Forzar actualización"):
    st.rerun()

