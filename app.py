import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="TSC | Andean Survival",
    page_icon="🏔️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS (PARA DARLE EL LOOK FUTURISTA) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .metric-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4F4F4F;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATOS SIMULADOS (MOCK DATA) ---
# En el futuro, esto vendrá de tu base de datos real
datos_mapa = pd.DataFrame({
    'lat': [-16.4955, -16.5000, -16.5123, -16.3800],
    'lon': [-68.1335, -68.1193, -68.1250, -67.9800],
    'tipo': ['Precaución', 'Seguro', 'Bloqueo', 'Peligro'],
    'color': ['#FFA500', '#00FF00', '#FF0000', '#FF0000'] # Naranja, Verde, Rojo
})

# --- BARRA LATERAL (NAVEGACIÓN) ---
st.sidebar.title("🏔️ TSC COMMAND")
st.sidebar.markdown("---")
opcion = st.sidebar.radio(
    "Selecciona Módulo:",
    ["📡 Dashboard (Vivo)", "🗺️ Mapa Táctico", "📝 Enviar Reporte", "🎒 Mi Perfil"]
)
st.sidebar.markdown("---")
st.sidebar.info("Estado del Sistema: v0.1 ALPHA\n\nConexión: Segura 🟢")

# --- MÓDULO 1: DASHBOARD ---
if opcion == "📡 Dashboard (Vivo)":
    st.title("📡 INTEL FEED: LA PAZ")
    
    # Ticker de Precios (Métricas)
    col1, col2, col3 = st.columns(3)
    col1.metric("USD / BOB (Calle)", "8.45 Bs", "+0.10")
    col2.metric("EUR / BOB", "9.10 Bs", "-0.05")
    col3.metric("Clima (Centro)", "12°C", "Nublado")
    
    st.markdown("### 🚨 Alertas Recientes")
    st.warning("⚠️ **Bloqueo Parcial** en Autopista (Carril bajada). Reportado hace 15 min.")
    st.success("✅ **Ruta a Yungas** habilitada. Paso normal por Yolosita.")
    st.info("ℹ️ **Tipo de Cambio:** Casa de cambio 'El Sol' (Sagárnaga) tiene dólares a 8.40.")

# --- MÓDULO 2: MAPA TÁCTICO ---
elif opcion == "🗺️ Mapa Táctico":
    st.title("🗺️ RADAR DE RUTAS")
    st.write("Visualización de incidentes reportados en las últimas 24 horas.")
    
    # Mostrar el mapa
    st.map(datos_mapa, zoom=12)
    
    st.markdown("""
    **Simbología:**
    * 🔴 Rojo: Bloqueo / Peligro
    * 🟠 Naranja: Precaución / Tráfico
    * 🟢 Verde: Ruta Segura / Verificada
    """)

# --- MÓDULO 3: ENVIAR REPORTE ---
elif opcion == "📝 Enviar Reporte":
    st.title("📝 NUEVO REPORTE DE INTEL")
    st.write("Tu información ayuda a otros viajeros. Gana puntos de reputación.")
    
    with st.form("reporte_form"):
        tipo = st.selectbox("¿Qué quieres reportar?", ["🚧 Bloqueo/Marcha", "💱 Tipo de Cambio", "🚕 Precio Taxi", "🛡️ Seguridad"])
        ubicacion = st.text_input("Ubicación (Ej: Plaza Murillo)")
        detalle = st.text_area("Detalles adicionales")
        foto = st.file_uploader("Evidencia (Foto)", type=["jpg", "png"])
        
        submitted = st.form_submit_button("ENVIAR A LA RED")
        
        if submitted:
            st.balloons() # Efecto de celebración
            st.success("✅ ¡Reporte enviado! Tus datos están siendo verificados en la Blockchain (Simulado).")

# --- MÓDULO 4: PERFIL ---
elif opcion == "🎒 Mi Perfil":
    st.title("👤 EXPEDIENTE: SÉBASTIEN")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=100)
    with col2:
        st.markdown("### Rango: **Explorador Novato**")
        st.progress(25)
        st.caption("25/100 XP para siguiente nivel")
    
    st.markdown("---")
    st.markdown("### 🏅 Medallas")
    st.write("🔒 *Gravity Master (Bloqueado)*")
    st.write("🔒 *Survivor de la Altura (Bloqueado)*")
