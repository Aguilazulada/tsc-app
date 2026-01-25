import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="TSC | Andean Survival", page_icon="🏔️", layout="centered")

# Estilos CSS (Recuperamos tu estilo original)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    .stMetric { background-color: #262730; padding: 10px; border-radius: 5px; border: 1px solid #4F4F4F; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS (CON LA NUEVA COLUMNA DE DESCRIPCIÓN) ---
data_reportes = pd.DataFrame({
    'lat': [-16.4955, -16.5000, -16.5123, -16.4820],
    'lon': [-68.1335, -68.1193, -68.1250, -68.1500],
    'categoria': ['💱 Cambio', '🟢 Seguro', '🚧 Bloqueo', '💱 Cambio'],
    'titulo': ['Casa El Sol', 'Plaza Murillo', 'Marcha Centro', 'Túnel San Francisco'],
    'precio_dolar': [8.45, None, None, 8.55],
    'descripcion': [
        'Local formal con letrero amarillo.',
        'Policía turística presente.',
        'Mineros en la vía.',
        'Señora de lentes y sombrero, silla blanca. Preguntar bajito.'
    ],
    'color': ['#00FF00', '#0000FF', '#FF0000', '#00FF00'],
    'size': [50, 20, 100, 200] # El tamaño indica la calidad del dato
})

# --- BARRA LATERAL ---
st.sidebar.title("🏔️ TSC COMMAND")
opcion = st.sidebar.radio("Navegación:", ["📡 Intel Dashboard", "🗺️ Mapa Táctico", "📝 Enviar Reporte"])

# --- 1. DASHBOARD (RECUPERADO) ---
if opcion == "📡 Intel Dashboard":
    st.title("📡 INTEL FEED")
    
    # Tus Métricas (Ticker) volvieron
    col1, col2, col3 = st.columns(3)
    col1.metric("Dólar (Calle)", "8.55 Bs", "🔥 High")
    col2.metric("Euro (Calle)", "9.10 Bs", "Estable")
    col3.metric("Clima", "12°C", "Nublado")
    
    st.markdown("---")
    st.subheader("🚨 Últimas Alertas")
    st.warning("🚧 **Bloqueo:** Marcha en el Centro. Evitar El Prado.")
    
    st.markdown("---")
    st.subheader("💎 Mejores Datos de Cambio")
    # Tabla simple para ver rápido quién paga más
    st.dataframe(
        data_reportes[data_reportes['categoria']=='💱 Cambio'][['titulo', 'precio_dolar', 'descripcion']],
        hide_index=True
    )

# --- 2. MAPA TÁCTICO (MEJORADO CON TU IDEA) ---
elif opcion == "🗺️ Mapa Táctico":
    st.title("🗺️ RADAR DE OPERACIONES")
    
    # Filtro
    filtro = st.radio("Filtro:", ["Todo", "Solo Dinero 💱", "Solo Amenazas 🚧"], horizontal=True)
    
    if filtro == "Solo Dinero 💱":
        map_data = data_reportes[data_reportes['categoria'] == '💱 Cambio']
        st.caption("💡 Los puntos más grandes son el mejor precio.")
    elif filtro == "Solo Amenazas 🚧":
        map_data = data_reportes[data_reportes['categoria'] == '🚧 Bloqueo']
    else:
        map_data = data_reportes

    # Mapa con puntos de tamaño variable
    st.map(map_data, color="color", size="size", zoom=13)
    
    # Aquí mostramos los detalles visuales que pediste
    st.markdown("### 👁️‍🗨️ Detalles Visuales (Señas)")
    for index, row in map_data.iterrows():
        with st.expander(f"{row['titulo']} ({row['categoria']})"):
            st.write(f"**Descripción:** {row['descripcion']}")
            if row['precio_dolar'] > 0:
                st.write(f"**Precio:** {row['precio_dolar']} Bs")

# --- 3. REPORTE (CON TU NUEVO CAMPO DE TEXTO) ---
elif opcion == "📝 Enviar Reporte":
    st.title("⚡ REPORTE TÁCTICO")
    
    categoria = st.radio("Categoría:", ["💱 Tipo de Cambio", "🚧 Bloqueo", "🛡️ Otros"], horizontal=True)
    
    with st.form("reporte"):
        # Si es Dinero, mostramos el campo de "Señas Particulares"
        if categoria == "💱 Tipo de Cambio":
            col1, col2 = st.columns(2)
            col1.number_input("Precio (Bs)", value=8.50, step=0.05)
            col2.selectbox("Moneda", ["USD", "EUR"])
            
            st.markdown("**¿Cómo ubicamos al cambista?**")
            st.text_area("Señas Particulares", placeholder="Ej: Señora de lentes, puesto azul, al lado del túnel...")
            
        elif categoria == "🚧 Bloqueo":
            st.select_slider("Gravedad", ["Tráfico", "Colapso Total"])
            st.text_area("Detalles", placeholder="Ej: Escombros en la vía...")
            
        st.checkbox("📍 Usar mi GPS", value=True)
        
        if st.form_submit_button("🚀 ENVIAR"):
            st.balloons()
            st.success("Reporte agregado con éxito.")
           
