import streamlit as st

def run_uyunitec_sim():
    # --- 1. PARÁMETROS DE COSTOS (Bolivia 2026) ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40  
    PRECIO_LITRO_BS = 6.96
    PRECIO_KWH_BS = 0.85  # Tarifa promedio domiciliaria/comercial en Bolivia
    CONSUMO_LC_BASE = 22 

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción Híbrida 4x4")

    # --- 2. CONFIGURACIÓN EN BARRA LATERAL ---
    with st.sidebar:
        st.header("⚡ Energía Inicial")
        gasolina_inicial = st.slider("Litros de Gasolina:", 0, TANQUE_MAX, 70)
        bateria_inicial = st.slider("Carga de Batería (%):", 0, 100, 100)
        
        st.write("---")
        st.header("🔌 Gestión")
        modo_energia = st.selectbox(
            "Modo de Conducción:",
            ["Híbrido Automático (Smart)", "Prioridad Motor Térmico (Save)", "Máximo Eléctrico (EV Mode)"]
        )

        st.write("---")
        st.header("🗺️ Ruta")
        distancia = st.number_input("Distancia (km)", value=100, min_value=1)
        # NUEVO TERRENO: TIERRA
        terreno = st.selectbox("Terreno:", ["pavimento", "salar (seco)", "tierra/terroso", "calamina", "arena"])
        altitud = st.slider("Altitud (msnm)", 3000, 5000, 3800)

    # --- 3. LÓGICA DE CONSUMO Y COSTOS ---
    factores_terreno = {
        "pavimento": 1.0, 
        "salar (seco)": 1.1, 
        "tierra/terroso": 1.2, # Nuevo factor
        "calamina": 1.3, 
        "arena": 1.6
    }
    
    penalizacion = factores_terreno.get(terreno, 1.0)
    eficiencia_altitud = max(0.6, 1 - (altitud / 12000))
    
    # Lógica de consumo dual
    if modo_energia == "Máximo Eléctrico (EV Mode)":
        c_gas_f, c_bat_f = 0.60, 1.5
    elif modo_energia == "Prioridad Motor Térmico (Save)":
        c_gas_f, c_bat_f = 1.25, 0.2
    else:
        c_gas_f, c_bat_f = 1.0, 1.0

    # Cálculos finales
    litros_nec = round((distancia / 100) * (5.75 * penalizacion * c_gas_f / eficiencia_altitud), 2)
    kwh_nec = (distancia / 4) * penalizacion * c_bat_f / eficiencia_altitud
    porc_bat_nec = round(kwh_nec, 1) # Simplificado para el %
    
    # --- 4. RESULTADOS Y COSTOS REALES ---
    if st.button("🚀 Ejecutar Simulación"):
        litros_fin = round(gasolina_inicial - litros_nec, 2)
        bat_fin = round(bateria_inicial - porc_bat_nec, 1)
        
        # Costos comparativos
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * PRECIO_LITRO_BS
        costo_gas_fulwin = litros_nec * PRECIO_LITRO_BS
        # Costo de la energía consumida (basado en lo que sacamos de la batería)
        costo_elec_fulwin = (porc_bat_nec / 100 * BATERIA_MAX_KWH) * PRECIO_KWH_BS
        costo_total_fulwin = costo_gas_fulwin + costo_elec_fulwin
        
        st.markdown(f"### Análisis de Costo Total")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gasto Total Fulwin", f"Bs {round(costo_total_fulwin, 2)}")
        c2.metric("Ahorro vs LC", f"Bs {round(costo_lc - costo_total_fulwin, 2)}")
        c3.metric("Costo Electricidad", f"Bs {round(costo_elec_fulwin, 2)}", help="Costo de recargar los kWh usados")

        st.write("---")
        # Visualización de depósitos
        cg, cb = st.columns(2)
        with cg:
            st.write(f"⛽ Gasolina al llegar: {max(0, litros_fin)}L")
            st.progress(max(0, int(litros_fin/TANQUE_MAX*100)))
        with cb:
            st.write(f"⚡ Batería al llegar: {max(0, bat_fin)}%")
            st.progress(max(0, int(bat_fin)))

        st.info(f"💡 Cargar la batería al 100% en Uyuni te cuesta solo Bs {round(BATERIA_MAX_KWH * PRECIO_KWH_BS, 2)}. ¡Es casi gratis comparado con la gasolina!")

if __name__ == "__main__":
    run_uyunitec_sim()
