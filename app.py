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
st.title("🦅 Aguilazulada")

nombre = st.text_input("👤 Reportado por:", placeholder="Tu nombre")
novedad = st.selectbox("📝 Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

st.write("---")
# FOTO SIEMPRE PRESENTE
foto = st.file_uploader("📸 Adjuntar Foto (Evidencia)", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, caption="Evidencia lista", use_container_width=True)

comentarios = st.text_area("💬 Detalles:")

st.write("---")

# --- 3. SISTEMA DE GPS MEJORADO ---
st.subheader("📍 Ubicación Satelital")

# Usamos un checkbox como interruptor. Es mucho más estable que un botón para el GPS.
activar_gps = st.checkbox("📡 ACTIVAR GPS PARA EL REPORTE")

if activar_gps:
    # Este es el comando que "despierta" al celular
    loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => ({lat: x.coords.latitude, lon: x.coords.longitude}))))', key='gps_vFinal_LaPaz')
    
    if loc:
        try:
            pos = json.loads(loc)
            lat, lon = pos.get('lat'), pos.get('lon')
            
            if lat:
                st.success(f"✅ Satélite enlazado: {lat}, {lon}")
                # Mostramos el Mapa
                df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
                st.map(df_mapa)
                
                # Guardamos en la memoria de la app
                st.session_state.lat = lat
                st.session_state.lon = lon
        except:
            st.info("🔄 Sincronizando con el satélite...")
    else:
        st.warning("🛰️ Buscando señal... Si tu celular te pregunta, dale a 'PERMITIR'.")

st.write("---")

# --- 4. ENVÍO FINAL ---
if st.button("🚀 ENVIAR REPORTE AL EXCEL"):
    if 'lat' in st.session_state:
        try:
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Guardamos: Fecha, Nombre, Novedad, Detalles, Lat, Lon
            sheet.append_row([fecha, nombre, novedad, comentarios, st.session_state.lat, st.session_state.lon])
            st.balloons()
            st.success("¡DATOS ENVIADOS! Revisa tu Google Sheet.")
        except Exception as e:
            st.error(f"Error al escribir en Excel: {e}")
    else:
        st.error("❌ No hay ubicación. Primero marca el cuadro de 'Activar GPS' arriba.")
