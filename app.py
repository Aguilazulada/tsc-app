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
    creds_dict = json.loads(raw_creds) if isinstance(raw_creds, str) else dict(raw_creds)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
except Exception as e:
    st.error(f"❌ Error en la 'Caja Fuerte' (Secrets): {e}")

# --- 2. INTERFAZ AGUILAZULADA ---
st.title("🦅 Aguilazulada")
st.markdown("### Reporte Multi-Propósito")

nombre = st.text_input("👤 Reportado por:", placeholder="Tu nombre")
novedad = st.selectbox("📝 Tipo de Novedad:", ["Bloqueo", "Precio Dólar", "Marchas", "Street food", "Otros"])

# --- LA OPCIÓN DE FOTO (SE MANTIENE SIEMPRE) ---
st.write("---")
foto = st.file_uploader("📸 Adjuntar Foto (Opcional)", type=["jpg", "png", "jpeg"])
if foto:
    st.image(foto, caption="Vista previa de la imagen", use_container_width=True)

comentarios = st.text_area("💬 Detalles del reporte:")

st.write("---")

# --- 3. DIAGNÓSTICO DEL EXCEL (Para saber si el Sheet está bien) ---
if st.button("🧪 Probar Conexión al Excel"):
    try:
        # Busca el nombre exacto de tu archivo
        sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
        st.success("✅ ¡Conexión exitosa! El robot puede escribir en tu Google Sheet.")
    except Exception as e:
        st.error(f"❌ Error con el Excel: {e}")
        st.info("Revisa que hayas compartido el archivo con el correo del robot como 'Editor'.")

st.write("---")

# --- 4. EL GPS Y EL MAPA ---
st.subheader("📍 Ubicación")
st.info("Si el mapa no carga, presiona el botón de abajo y acepta los permisos en la parte superior del navegador.")

# Botón para forzar la captura
if st.button("📡 ACTIVAR GPS Y MAPA"):
    loc = streamlit_js_eval(js_expressions='done(JSON.stringify(window.navigator.geolocation.getCurrentPosition(x => x.coords)))', key='gps_final_ultra')
    
    if loc:
        pos = json.loads(loc)
        st.session_state.lat = pos.get('latitude')
        st.session_state.lon = pos.get('longitude')

# Mostrar mapa si hay datos
if 'lat' in st.session_state and st.session_state.lat:
    lat, lon = st.session_state.lat, st.session_state.lon
    st.success(f"✅ Satélite conectado.")
    
    df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(df_mapa)
    
    # ENVÍO FINAL
    if st.button("🚀 ENVIAR REPORTE"):
        try:
            sheet = client.open("FORMULARIO SIN TÍTULO (Respuestas)").sheet1
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            # Guardamos: Fecha, Nombre, Novedad, Detalles, Lat, Lon
            sheet.append_row([fecha, nombre, novedad, comentarios, lat, lon])
            st.balloons()
            st.success("¡Reporte enviado correctamente!")
        except Exception as e:
            st.error(f"Error al enviar: {e}")
else:
    st.warning("Esperando coordenadas para dibujar el mapa...")

