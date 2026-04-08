import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
from streamlit_js_eval import streamlit_js_eval
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD (No tocar, ya funciona) ---
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
try:
    raw_creds = st.secrets["google_credentials"]
    creds_dict = json.loads(raw_creds) if isinstance(raw_creds, str) else dict(raw_creds)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"Error de credenciales: {e}")

# --- 2. INTERFAZ: RECUPERANDO EL LOOK ORIGINAL ---
st.set_page_config(page_title="Aguilazulada GPS", page_icon="🦅")
st.title("🦅 Aguilazulada")

st.subheader("📝 Datos del Reporte")

# Aquí he puesto campos genéricos, dime cuáles tenías tú y los cambio:
nombre = st.text_input("👤 Nombre / Identificador")
descripcion = st.text_area("📋 Observaciones o Novedades")

st.markdown("---")

# --- 3. EL GPS (Versión 2.0 más fuerte) ---
st.subheader("📍 Ubicación Satelital")
st.write("Presiona el botón para fijar tu posición:")

# Usamos una versión de JS que suele ser más compatible con celulares y PCs viejitas
loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', key='get_location_final')

if loc:
    try:
        pos = json.loads(loc)
        # Algunos navegadores devuelven la info un poco distinto, aquí cubrimos ambos casos
        lat = pos.get('latitude') or pos.get('coords', {}).get('latitude')
        lon = pos.get('longitude') or pos.get('coords', {}).get('longitude')
        
        if lat and lon:
            st.success(f"✅ Ubicación fijada: {lat}, {lon}")
            
            # --- BOTÓN DE ENVÍO ---
            if st.button("🚀 ENVIAR REPORTE AL EXCEL"):
                try:
                    sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
                    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    # Mandamos: Fecha, Nombre, Descripción, Latitud, Longitud
                    sheet.append_row([fecha, nombre, descripcion, lat, lon])
                    
                    st.balloons()
                    st.success("¡Datos guardados con éxito en el Excel!")
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
        else:
            st.warning("⚠️ El GPS respondió pero no envió coordenadas claras. Intenta refrescar.")
    except Exception as e:
        st.error(f"Error procesando ubicación: {e}")
else:
    st.info("🛰️ Buscando señal... Si no aparece, dale a 'Recargar' en tu navegador.")
    if st.button("🔄 Reintentar capturar señal"):
        st.rerun()


