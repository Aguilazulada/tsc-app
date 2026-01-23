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

# --- MÓDULO 3: ENVIAR REPORTE (INTELIGENTE) ---
elif opcion == "📝 Enviar Reporte":
    st.title("⚡ REPORTE TÁCTICO")
    
    # 1. SELECCIÓN DE CATEGORÍA
    st.markdown("### 1. ¿Qué quieres reportar?")
    categoria = st.radio(
        "Selecciona una opción:",
        ["🚧 Bloqueo / Tráfico", "💱 Tipo de Cambio", "🛡️ Seguridad / Otros"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    with st.form("reporte_form"):
        # LÓGICA CONDICIONAL: Muestra cosas distintas según la categoría
        
        # CASO A: SI ES DINERO
        if categoria == "💱 Tipo de Cambio":
            st.info("📊 **Referencia de Mercado (Promedio Hoy):**")
            
            # Tabla de referencia visual
            col_ref1, col_ref2 = st.columns(2)
            col_ref1.metric("Dólar (USD)", "8.45 Bs", "Ref")
            col_ref2.metric("Euro (EUR)", "9.10 Bs", "Ref")
            
            st.markdown("#### Tu Reporte:")
            col1, col2 = st.columns(2)
            with col1:
                moneda = st.selectbox("Moneda", ["🇺🇸 Dólar (USD)", "🇪🇺 Euro (EUR)"])
            with col2:
                operacion = st.selectbox("Acción", ["Compra (Busco)", "Venta (Tengo)"])
            
            # Input numérico preciso (mejor que slider para dinero)
            precio = st.number_input("Precio encontrado (Bs)", min_value=6.00, max_value=15.00, value=8.45, step=0.05)
            nivel_detalle = f"{moneda} - {operacion} a {precio} Bs"

        # CASO B: SI ES BLOQUEO (Mantenemos la agilidad)
        elif categoria == "🚧 Bloqueo / Tráfico":
            st.warning("⚠️ Reportando incidente en vía pública")
            nivel = st.select_slider(
                "¿Qué tan grave es?", 
                options=["🟢 Transitable", "🟡 Tráfico Lento", "🟠 Bloqueo Parcial", "🔴 Bloqueo Total", "⚫ Guerra Civil"]
            )
            nivel_detalle = f"Estado: {nivel}"

        # CASO C: OTROS
        else:
            nivel_detalle = st.text_input("Describe brevemente (Ej: Robos en la zona, Fiesta...)")

        st.markdown("---")

        # UBICACIÓN Y ENVÍO
        col_gps1, col_gps2 = st.columns([1,3])
        with col_gps1:
            st.write("📍 Ubicación:")
        with col_gps2:
            st.checkbox("Usar mi GPS actual", value=True)
        
        submitted = st.form_submit_button("🚀 ENVIAR REPORTE", use_container_width=True)
        
        if submitted:
            st.balloons()
            st.success(f"✅ DATO GUARDADO: {categoria}")
            st.caption(f"Detalle: {nivel_detalle}")

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
