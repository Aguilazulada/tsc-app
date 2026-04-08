import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
raw_creds = st.secrets["google_credentials"]
if isinstance(raw_creds, str):
    creds_dict = json.loads(raw_creds)
else:
    creds_dict = dict(raw_creds)

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# --- 2. FUNCIÓN PARA ENVIAR DATOS ---
def guardar_en_excel(datos_fila):
    try:
        sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
        sheet.append_row(datos_fila)
        return True
    except Exception as e:
        st.error(f"Error al escribir en Excel: {e}")
        return False

# --- 3. INTERFAZ (DEVOLVIENDO EL LOOK ORIGINAL) ---
st.set_page_config(page_title="Aguilazulada", page_icon="🦅")
st.title("🦅 Aguilazulada: Reporte GPS")

st.info("Por favor, llena los datos y presiona el botón de ubicación al final.")

# --- AQUÍ EMPIEZA TU FORMULARIO ORIGINAL (Ajusta los nombres si eran otros) ---
nombre = st.text_input("Nombre del Reportante")
descripcion = st.text_area("Descripción del evento o situación")
tipo_reporte = st.selectbox("Categoría", ["Bloqueo", "Accidente", "Precio Dólar", "Zona Segura", "Otro"])

st.markdown("---")
st.write("### 📍 Ubicación Satelital")

# Botón para activar el GPS de forma manual (Más confiable)
if st.button("🛰️ Obtener mi Ubicación Actual"):
    # Esta línea es el "parche" de oro para que el GPS despierte
    loc = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition((pos) => { done(JSON.stringify({lat: pos.coords.latitude, lon: pos.coords.longitude})) })", key='get_loc')
    
    if loc:
        pos = json.loads(loc)
        st.session_state.lat = pos['lat']
        st.session_state.lon = pos['lon']
        st.success(f"✅ Coordenadas obtenidas: {st.session_state.lat}, {st.session_state.lon}")
    else:
        st.warning("Capturando señal... Si no aparece, verifica que el GPS del celu esté en 'Alta Precisión'.")

# --- BOTÓN FINAL DE ENVÍO ---
if st.button("🚀 ENVIAR TODO AL EXCEL"):
    if 'lat' in st.session_state:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos = [ahora, nombre, tipo_reporte, descripcion, st.session_state.lat, st.session_state.lon]
        
        if guardar_en_excel(datos):
            st.balloons()
            st.success("¡Datos y ubicación enviados correctamente!")
    else:
        st.error("❌ Primero debes obtener tu ubicación con el botón de arriba.")


          

