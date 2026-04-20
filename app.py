import streamlit as st

def run_uyunitec_sim():
    # --- 1. PARÁMETROS BASE ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40  
    PRECIO_KWH_BS = 0.85 
    CONSUMO_LC_BASE = 22 

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción Híbrida 4x4")

    # --- 2. CONFIGURACIÓN EN BARRA LATERAL ---
    with st.sidebar:
        st.header("⛽ Costo y Energía")
        # EL CHOFER PONE EL PRECIO AQUÍ
        precio_gasolina = st.number_input("Precio Gasolina (Bs/L):", value=6.96, step=0.01)
        gasolina_inicial = st.slider("Litros en tanque:", 0, TANQUE_MAX, 70)
        bateria_inicial = st.slider("Carga Batería (%):", 0, 100, 100)
        
        st.write("---")
        st.header("🔌 Gestión")
        modo_energia = st.selectbox(
            "Modo de Conducción:",
            ["Híbrido Automático (Smart)", "Prioridad Motor Térmico (Save)", "Máximo Eléctrico (EV Mode)"]
        )

        st.write("---")
        st.header("🗺️ Ruta")
        distancia = st.number_input("Distancia (km)", value=100, min_value=1)
        terreno = st.selectbox("Terreno:", ["pavimento", "salar (seco)", "tierra/terroso", "calamina", "arena"])
        altitud = st.slider("Altitud (msnm)", 3000, 5000, 3800)

    # --- 3. LÓGICA DE CONSUMO ---
    factores_terreno = {"pavimento": 1.0, "salar (seco)": 1.1, "tierra/terroso": 1.2, "calamina": 1.3, "arena": 1.6}
    penalizacion = factores_terreno.get(terreno, 1.0)
    eficiencia_altitud = max(0.6, 1 - (altitud / 12000))
    
    if modo_energia == "Máximo Eléctrico (EV Mode)":
        c_gas_f, c_bat_f = 0.60, 1.5
    elif modo_energia == "Prioridad Motor Térmico (Save)":
        c_gas_f, c_bat_f = 1.25, 0.2
    else:
        c_gas_f, c_bat_f = 1.0, 1.0

    litros_nec = round((distancia / 100) * (5.75 * penalizacion * c_gas_f / eficiencia_altitud), 2)
    kwh_nec = (distancia / 4) * penalizacion * c_bat_f / eficiencia_altitud
    
    # --- 4. RESULTADOS Y COSTOS ---
    if st.button("🚀 Ejecutar Simulación"):
        litros_fin = round(gasolina_inicial - litros_nec, 2)
        bat_fin = round(bateria_inicial - kwh_nec, 1)
        
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * precio_gasolina
        costo_total_fulwin = (litros_nec * precio_gasolina) + ((kwh_nec / 100 * BATERIA_MAX_KWH) * PRECIO_KWH_BS)
        
        st.markdown("### Análisis de Misión")
        c1, c2, c3 = st.columns(3)
        c1.metric("Gasto Fulwin", f"Bs {round(costo_total_fulwin, 2)}")
        c2.metric("Ahorro Real", f"Bs {round(costo_lc - costo_total_fulwin, 2)}")
        c3.metric("Llegada Batería", f"{max(0, bat_fin)}%")

        # --- SECCIÓN DE TIEMPOS DE RECARGA ---
        st.write("---")
        st.subheader("🕒 Tiempos Estimados de Recarga (al 100%)")
        kwh_a_cargar = BATERIA_MAX_KWH * (1 - (max(0, bat_fin)/100))
        
        t_col1, t_col2, t_col3 = st.columns(3)
        t_col1.info(f"**Doméstico (2.3kW)**\n\n{round(kwh_a_cargar/2.3, 1)} horas")
        t_col2.info(f"**Wallbox (7kW)**\n\n{round(kwh_a_cargar/7, 1)} horas")
        t_col3.info(f"**Carga Rápida DC**\n\n~45 min (al 80%)")

        st.success(f"Cargar los kWh usados te costará solo Bs {round((kwh_a_cargar) * PRECIO_KWH_BS, 2)}")

if __name__ == "__main__":
    run_uyunitec_sim()
