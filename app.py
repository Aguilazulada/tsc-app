import streamlit as st
import gspread
import json
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
st.markdown("### Reporte de Novedades")

nombre = st.text_input("👤 Reportado por:")

# Nuevas opciones solicitadas
novedad = st.selectbox("📝 Seleccione Novedad:", 
                        ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

# Permitir foto si es Street Food (o cualquier otra opcionalmente)
foto = None
if novedad == "Street food":
    foto = st.file_uploader("📸 Sube una foto de la comida", type=["jpg", "png", "jpeg"])
else:
    if st.checkbox("¿Deseas adjuntar una foto?"):
        foto = st.file_uploader("📸 Selecciona imagen", type=["jpg", "png", "jpeg"])

comentarios = st.text_area("💬 Detalles adicionales:")

st.write("---")

# --- 3. EL GPS (Intento Definitivo) ---
st.subheader("📍 Ubicación")
st.warning("Asegúrate de tener el GPS del celular encendido antes de presionar el botón.")

# Usamos una expresión de JS más agresiva para pedir permiso
loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', key='get_gps_v3')

if loc:
    pos = json.loads(loc)
    lat = pos.get('latitude')
    lon = pos.get('longitude')
    
    if lat:
        st.success(f"✅ Satélite conectado: {lat}, {lon}")
        
        # --- BOTÓN DE ENVÍO FINAL ---
        if st.button("🚀 ENVIAR REPORTE COMPLETO"):
            try:
                sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
                fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                # Guardamos: Fecha, Nombre, Novedad, Comentarios, Lat, Lon
                sheet.append_row([fecha, nombre, novedad, comentarios, lat, lon])
                st.balloons()
                st.success("¡Misión cumplida! Datos guardados en el Excel.")
            except Exception as e:
                st.error(f"Error al conectar con Google Sheets: {e}")
    else:
        st.error("❌ El navegador denegó el acceso al GPS.")
else:
    st.info("🛰️ Esperando señal... Si estás en PC, verifica el candado 🔒 de la barra de direcciones.")

if st.button("🔄 Forzar actualización de señal"):
    st.rerun()
