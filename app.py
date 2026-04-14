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

nombre = st.text_input("👤 Reportado por:")
novedad = st.selectbox("📝 Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

st.write("---")
foto = st.file_uploader("📸 Adjuntar Foto (Evidencia)", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, caption="Evidencia lista", use_container_width=True)

comentarios = st.text_area("💬 Detalles:")

st.write("---")

# --- 3. SISTEMA DE GPS ULTRA-PRECISO ---
st.subheader("📍 Ubicación")

# Este interruptor "enciende" el motor de búsqueda
activar_gps = st.checkbox("🛰️ CONECTAR CON SATÉLITE")

if activar_gps:
    # JS Mejorado: Pide alta precisión y tiene un tiempo de espera
    js_gps = """
    navigator.geolocation.getCurrentPosition(
        (pos) => { 
            done(JSON.stringify({lat: pos.coords.latitude, lon: pos.coords.longitude, ok: true})) 
        },
        (err) => { 
            done(JSON.stringify({error: err.message, ok: false})) 
        },
        {enableHighAccuracy: true, timeout: 10000, maximumAge: 0}
    );
    """
    loc = streamlit_js_eval(js_expressions=js_gps, key='gps_ultra_final')
    
    if loc:
        res = json.loads(loc)
        if res.get('ok'):
            lat, lon = res['lat'], res['lon']
            st.success(f"✅ ¡Señal capturada! ({lat}, {lon})")
            st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
            st.session_state.lat, st.session_state.lon = lat, lon
        else:
            st.error(f"❌ El celular dice: {res.get('error')}")
            st.info("Asegúrate de haberle dado a 'PERMITIR' cuando salió el aviso.")
    else:
        st.info("📡 Buscando... Si no aparece nada en 10 segundos, refresca la página.")

st.write("---")

# --- 4. ENVÍO FINAL ---
if st.button("🚀 ENVIAR REPORTE AL EXCEL"):
    if 'lat' in st.session_state:
        try:
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            sheet.append_row([fecha, nombre, novedad, comentarios, st.session_state.lat, st.session_state.lon])
            st.balloons()
            st.success("¡REPORTE ENVIADO CON ÉXITO!")
        except Exception as e:
            st.error(f"Error al escribir en Excel: {e}")
    else:
        st.error("❌ No hay ubicación. Activa el GPS arriba primero.")


   
