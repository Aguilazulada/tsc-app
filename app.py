import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="TSC | Andean Survival", page_icon="🏔️", layout="centered")

# --- ESTILOS (DARK MODE + FUENTES GRANDES) ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FAFAFA; }
    div[data-testid="stMetricValue"] { font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)
# --- FUNCIÓN DE CARGA DE DATOS (CORREGIDA PARA 8 COLUMNAS) ---
@st.cache_data(ttl=60)
def cargar_datos():
    SHEET_ID = "11ISvaU8BcuqnsFfliARmesR2fHxaMSlvEA0CcZslDOA"
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    
    try:
        df = pd.read_csv(url)
        
        # MAPA DE COLUMNAS (Ajustado a tu Excel real)
        # 0:Fecha | 1:Categoria | 2:Titulo | 3:Lugar | 4:Descripcion | 5:Precio | 6:Lat | 7:Lon
        
        rename_map = {
            df.columns[0]: 'fecha',
            df.columns[1]: 'categoria',
            df.columns[2]: 'titulo',
            # La columna 3 es 'Lugar'. No la asignamos directo, pero la usaremos abajo.
            df.columns[4]: 'descripcion',
            df.columns[5]: 'precio_dolar',
            df.columns[6]: 'lat',
            df.columns[7]: 'lon'
        }
        df = df.rename(columns=rename_map)
        
        # TRUCO: Unimos el "Lugar" al Título para no perder esa info
        # Ejemplo: "Casa de Cambio (Zona Sur)"
        df['titulo'] = df['titulo'] + " - " + df.iloc[:, 3].astype(str)

        # LIMPIEZA DE NUMEROS (Lat/Lon/Precio)
        df['lat'] = pd.to_numeric(df['lat'].astype(str).str.replace(',', '.'), errors='coerce')
        df['lon'] = pd.to_numeric(df['lon'].astype(str).str.replace(',', '.'), errors='coerce')
        df['precio_dolar'] = pd.to_numeric(df['precio_dolar'], errors='coerce').fillna(0)
        
        # ASIGNACIÓN DE COLORES
        conditions = [
            (df['categoria'].str.contains('Cambio', case=False, na=False)),
            (df['categoria'].str.contains('Bloqueo', case=False, na=False)),
            (df['categoria'].str.contains('Seguro', case=False, na=False))
        ]
        colors = ['#00FF00', '#FF0000', '#0000FF'] # Verde, Rojo, Azul
        df['color'] = np.select(conditions, colors, default='#808080')
        
        # ASIGNACIÓN DE TAMAÑOS
        df['size'] = np.where(df['categoria'].str.contains('Cambio', case=False), 
                              df['precio_dolar'] * 20, 
                              50)
                              
        return df.dropna(subset=['lat', 'lon'])
        
    except Exception as e:
        # Esto te ayudará a ver errores en la pantalla si algo falla
        st.error(f"Error leyendo Google Sheets: {e}")
        return pd.DataFrame()


# --- CARGAR DATOS ---
data_reportes = cargar_datos()

# --- BARRA LATERAL ---
st.sidebar.title("🏔️ TSC COMMAND")
st.sidebar.markdown("---")
opcion = st.sidebar.radio("Navegación:", ["📡 Intel Dashboard", "🗺️ Mapa Táctico", "📝 Enviar Reporte"])

if st.sidebar.button("🔄 Actualizar Datos"):
    st.cache_data.clear()
    st.rerun()

# --- 1. DASHBOARD ---
if opcion == "📡 Intel Dashboard":
    st.title("📡 INTEL FEED")
    
    # Métricas Clave (Calculadas de datos reales)
    if not data_reportes.empty:
        mejor_cambio = data_reportes[data_reportes['categoria'].str.contains('Cambio', na=False)]['precio_dolar'].max()
        total_alertas = len(data_reportes[data_reportes['categoria'].str.contains('Bloqueo', na=False)])
    else:
        mejor_cambio = 0
        total_alertas = 0

    col1, col2 = st.columns(2)
    col1.metric("Mejor Dólar (Venta)", f"{mejor_cambio} Bs")
    col2.metric("Alertas Activas", f"{total_alertas}", "Reportadas")
    
    st.markdown("---")
    st.subheader("📋 Feed de Reportes (En Vivo)")
    
    if not data_reportes.empty:
        st.dataframe(
            data_reportes[['categoria', 'titulo', 'precio_dolar', 'fecha']],
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No hay datos aún. Sé el primero en reportar.")

# --- 2. MAPA TÁCTICO ---
elif opcion == "🗺️ Mapa Táctico":
    st.title("🗺️ RADAR DE OPERACIONES")
    
    filtro = st.radio("Filtro:", ["Todo", "Solo Dinero 💱", "Solo Amenazas 🚧"], horizontal=True)
    
    if not data_reportes.empty:
        if filtro == "Solo Dinero 💱":
            map_data = data_reportes[data_reportes['categoria'].str.contains('Cambio', na=False)]
        elif filtro == "Solo Amenazas 🚧":
            map_data = data_reportes[data_reportes['categoria'].str.contains('Bloqueo', na=False)]
        else:
            map_data = data_reportes

        st.map(map_data, color="color", size="size", zoom=12)
        
        # Detalles debajo del mapa
        st.markdown("### 👁️‍🗨️ Detalles Visuales")
        for index, row in map_data.iterrows():
            with st.expander(f"{row['titulo']} ({row['categoria']})"):
                st.write(f"**Descripción:** {row['descripcion']}")
                if row['precio_dolar'] > 0:
                    st.write(f"**Precio:** {row['precio_dolar']} Bs")
                st.caption(f"Reportado: {row['fecha']}")
    else:
        st.warning("Esperando datos de satélite...")

# --- 3. ENVIAR REPORTE (LINK AL FORM) ---
elif opcion == "📝 Enviar Reporte":
    st.title("⚡ REPORTE TÁCTICO")
    st.markdown("""
    Para mantener la seguridad de la red, usamos un canal encriptado (Google Forms) para la ingesta de datos.
    
    Tus datos aparecerán en el mapa automáticamente en 60 segundos.
    """)
    
    # IMPORTANTE: CAMBIA ESTE LINK POR EL DE TU FORMULARIO (Botón "Enviar" -> Link)
    link_formulario = "https://docs.google.com/spreadsheets/d/11ISvaU8BcuqnsFfliARmesR2fHxaMSlvEA0CcZslDOA/edit?usp=sharing" 
    
    st.link_button("🚀 ABRIR CANAL DE REPORTE", link_formulario, type="primary", use_container_width=True)
    
    st.info("💡 **Tip:** Si estás en el lugar, activa el GPS de tu cámara para copiar las coordenadas.")
