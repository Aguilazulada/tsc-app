import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="TSC | Andean Survival", page_icon="🏔️", layout="centered")

# Estilos CSS (Tipografía más grande para móviles)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    div[data-testid="stMetricValue"] { font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DATOS DE PRUEBA (CON TUS EJEMPLOS) ---
data_reportes = pd.DataFrame({
    'lat': [-16.4955, -16.5000, -16.5123, -16.4820],
    'lon': [-68.1335, -68.1193, -68.1250, -68.1500],
    'categoria': ['💱 Cambio', '🟢 Seguro', '🚧 Bloqueo', '💱 Cambio'],
    'titulo': ['Casa El Sol', 'Plaza Murillo', 'Marcha Centro', 'Túnel San Francisco'],
    'precio_dolar': [8.45, None, None, 8.55], # 8.55 es el mejor precio
    'descripcion': [
        'Local formal, piden carnet. Seguro pero fila larga.',
        'Todo tranquilo, muchos policías.',
        'Mineros bloqueando ingreso al Prado.',
        'Señora de lentes y sombrero, sentada en una silla blanca. Preguntar bajito.'
    ],
    # El tamaño del punto en el mapa dependerá del precio (más grande = mejor cambio)
    'size': [50, 20, 100, 200], 
    'color': ['#00FF00', '#0000FF', '#FF0000', '#00FF00']
})

# --- BARRA LATERAL ---
st.sidebar.title("🏔️ TSC COMMAND")
opcion = st.sidebar.radio("Menú:", ["🗺️ Mapa & Intel", "📝 Enviar Reporte"])

# --- 1. MAPA & INTEL (FUSIÓN VISUAL) ---
if opcion == "🗺️ Mapa & Intel":
    st.title("🗺️ RADAR DE MERCADO")
    
    # Filtro rápido
    ver_dinero = st.toggle("🤑 Ver solo Oportunidades de Dinero", value=True)
    
    if ver_dinero:
        # Filtramos solo cambio y ordenamos por precio
        map_data = data_reportes[data_reportes['categoria'] == '💱 Cambio']
        st.info("💡 **Tip:** Los círculos más grandes son los que pagan mejor.")
        
        # Mostramos KPIs clave arriba del mapa
        mejor_tasa = map_data['precio_dolar'].max()
        st.metric("🔥 MEJOR TASA DETECTADA", f"{mejor_tasa} Bs")
    else:
        map_data = data_reportes

    # EL MAPA (Ahora los puntos varían de tamaño según importancia)
    st.map(map_data, color="color", size="size", zoom=13)
    
    st.markdown("### 📝 Detalles de Inteligencia")
    
    # Mostramos las tarjetas de detalle (Aquí aparece tu descripción)
    for index, row in map_data.iterrows():
        with st.container():
            # Diseño de tarjeta para cada reporte
            c1, c2 = st.columns([1, 3])
            with c1:
                # Icono gigante según categoría
                if row['categoria'] == '💱 Cambio':
                    st.markdown(f"## 💵\n**{row['precio_dolar']} Bs**")
                else:
                    st.markdown("## 🚧")
            with c2:
                st.subheader(row['titulo'])
                st.caption(f"📍 Coordenadas: {row['lat']}, {row['lon']}")
                st.write(f"👁️‍🗨️ **Intel Visual:** {row['descripcion']}")
            st.divider()

# --- 2. ENVIAR REPORTE (CON DESCRIPCIÓN VISUAL) ---
elif opcion == "📝 Enviar Reporte":
    st.title("⚡ NUEVO REPORTE")
    
    tipo = st.selectbox("Categoría", ["💱 Tipo de Cambio (Dinero)", "🚧 Bloqueo (Ruta)", "🛡️ Seguridad"])
    
    with st.form("reporte_v2"):
        if tipo == "💱 Tipo de Cambio (Dinero)":
            col_din1, col_din2 = st.columns(2)
            col_din1.number_input("Precio Compra (Bs)", value=8.50, step=0.05)
            col_din2.selectbox("Moneda", ["USD", "EUR"])
            
            # EL CAMPO NUEVO QUE PEDISTE 👇
            st.text_area("👁️‍🗨️ Señas Particulares (Clave para ubicarlo)", 
                         placeholder="Ej: Señora con manta azul, kiosco al lado del poste, entrar al pasillo del fondo...")
            
        elif tipo == "🚧 Bloqueo (Ruta)":
            st.select_slider("Gravedad", ["Tráfico Lento", "Bloqueo Total"])
            st.text_area("Detalles visuales", placeholder="Ej: Están quemando llantas, hay paso por la vereda...")
            
        st.form_submit_button("🚀 PUBLICAR EN EL MAPA")
