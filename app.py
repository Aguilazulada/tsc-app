import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from streamlit_js_eval import streamlit_js_eval
import pandas as pd
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD (Caja Fuerte) ---
# Conectamos con la llave JSON que guardaste en los Secrets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_credentials"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# --- 2. FUNCIÓN PARA ENVIAR DATOS AL EXCEL ---
def guardar_en_excel(tipo, lat, lon):
    try:
        # Abrimos tu archivo por el nombre exacto que me diste
        sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
        
        # Preparamos la fila: Fecha/Hora, Tipo, Latitud, Longitud
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fila = [ahora, tipo, lat, lon]
        
        # El robot escribe la fila al final del Excel
        sheet.append_row(fila)
        return True
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# --- 3. INTERFAZ DE LA APLICACIÓN ---
st.set_page_config(page_title="Aguilazulada GPS", layout="centered")
st.title("🦅 Aguilazulada: Reporte en Tiempo Real")

st.markdown("---")
st.write("### 📍 Capturar mi Ubicación")
st.info("Al presionar el botón, el navegador te pedirá permiso para acceder al GPS.")

# Botón mágico que activa el GPS del celular/computadora
loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', target_id='get_location')

if loc:
    pos = eval(loc)
    lat, lon = pos['latitude'], pos['longitude']
    
    st.success(f"✅ Ubicación capturada: {lat}, {lon}")
    
    # Selector de tipo de reporte
    opcion = st.selectbox("¿Qué deseas reportar?", 
                         ["Bloqueo de vía 🚩", "Precio Dólar 💵", "Zona Segura ✅", "Accidente ⚠️"])
    
    # Botón final de envío
    if st.button("🚀 Enviar Reporte Directo"):
        with st.spinner('Comunicando con el satélite...'):
            exito = guardar_en_excel(opcion, lat, lon)
            if exito:
                st.balloons()
                st.success("¡Misión cumplida! El reporte ya está en el Excel.")
else:
    st.warning("Esperando señal de GPS... Asegúrate de tener la ubicación activada.")

st.markdown("---")
st.caption("Proyecto Aguilazulada - Conexión directa a Google Sheets")
      
       
       

     
          

