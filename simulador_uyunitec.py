import streamlit as st

def run_uyunitec_sim():
    # --- 1. PARÁMETROS CALIBRADOS ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40
    PRECIO_KWH_BS = 0.85 
    CONSUMO_LC_BASE = 22 
    
    KM_POR_LITRO = 13.5
    KM_POR_PORCENTAJE_BAT = 1.5 # 100% = 150km base

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción Híbrida 4x4")

    # --- 2. CONFIGURACIÓN ---
    with st.sidebar:
        st.header("⛽ Energía Disponible")
        precio_gasolina = st.number_input("Precio Gasolina (Bs/L):", value=6.96, step=0.01)
        gasolina_inicial = st.slider("Litros actuales:", 0, TANQUE_MAX, 70)
        bateria_inicial = st.slider("Batería inicial (%):", 0, 100, 100)
        
        st.write("---")
        modo_energia = st.selectbox(
            "Estrategia de Motores:",
            ["Híbrido Automático (Smart)", "Prioridad Térmico (Save)", "Máximo Eléctrico (EV Mode)"]
        )
        distancia = st.number_input("Distancia Ruta (km)", value=100, min_value=1)
        terreno = st.selectbox("Suelo:", ["pavimento", "salar (seco)", "tierra/terroso", "calamina", "arena"])
        altitud = st.slider("Altitud (msnm)", 3000, 5000, 3800)

    # --- 3. LÓGICA DE CONSUMO RECALIBRADA ---
    factores_terreno = {"pavimento": 1.0, "salar (seco)": 1.1, "tierra/terroso": 1.2, "calamina": 1.3, "arena": 1.6}
    penalizacion = factores_terreno.get(terreno, 1.0)
    
    # La altitud afecta menos a la batería que al motor de combustión
    eficiencia_altitud_gas = max(0.6, 1 - (altitud / 12000))
    eficiencia_altitud_bat = max(0.8, 1 - (altitud / 20000)) # Eléctrico es más estable
    
    if modo_energia == "Máximo Eléctrico (EV Mode)":
        c_gas_f, c_bat_f = 0.1, 1.0 # Casi no gasta gasolina, batería rinde según terreno
    elif modo_energia == "Prioridad Térmico (Save)":
        c_gas_f, c_bat_f = 1.25, 0.1
    else:
        c_gas_f, c_bat_f = 0.8, 0.8

    litros_nec = (distancia / KM_POR_LITRO) * penalizacion * c_gas_f / eficiencia_altitud_gas
    # Cálculo de batería más realista
    porc_bat_nec = (distancia / KM_POR_PORCENTAJE_BAT) * penalizacion * c_bat_f / eficiencia_altitud_bat
    
    # --- 4. RESULTADOS ---
    if st.button("🚀 Ejecutar Simulación"):
        l_fin = round(gasolina_inicial - litros_nec, 2)
        b_fin = round(bateria_inicial - porc_bat_nec, 1)
        
        st.markdown("### 📊 Estado de Energía al Llegar")
        col_g, col_b = st.columns(2)
        
        with col_g:
            p_gas = max(0, int((l_fin / TANQUE_MAX) * 100))
            st.write(f"⛽ **Gasolina: {p_gas}%** ({max(0, l_fin)}L)")
            st.progress(p_gas)
            if 0 < l_fin <= 10: st.warning(f"⚠️ RESERVA: ~{round(max(0, l_fin) * KM_POR_LITRO, 1)} km")

        with col_b:
            p_bat = max(0, int(b_fin))
            st.write(f"⚡ **Batería: {p_bat}%**")
            st.progress(p_bat)
            if 0 < b_fin <= 10: st.warning(f"⚠️ CRÍTICO: ~{round(max(0, b_fin) * KM_POR_PORCENTAJE_BAT, 1)} km")
            elif b_fin <= 0: st.error("🚨 BATERÍA AGOTADA")

        st.write("---")
        
        # --- AHORRO REAL ---
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * precio_gasolina
        costo_gas_fulwin = litros_nec * precio_gasolina
        # El ahorro EV es lo que NO gastaste en gasolina gracias a la batería
        ahorro_gas_ev = (distancia * (1 - c_gas_f) / KM_POR_LITRO) * precio_gasolina
        costo_luz = (porc_bat_nec / 100 * BATERIA_MAX_KWH) * PRECIO_KWH_BS
        ahorro_uso_ev = max(0, ahorro_gas_ev - costo_luz)

        st.subheader("💰 Análisis de Ahorro")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ahorro Gasolina", f"Bs {round(costo_lc - costo_gas_fulwin, 2)}")
        c2.metric("Ahorro Uso EV", f"Bs {round(ahorro_uso_ev, 2)}")
        c3.metric("Alcance Final", f"~{round(max(0,l_fin)*KM_POR_LITRO + max(0,b_fin)*KM_POR_PORCENTAJE_BAT, 1)} km")

        # --- RECARGA ---
        st.write("---")
        st.subheader("🕒 Logística de Recarga")
        kwh_a_recargar = BATERIA_MAX_KWH * (min(100, porc_bat_nec) / 100)
        st.info(f"**Tiempo en Enchufe Pared (2.3kW):** {round(kwh_a_recargar/2.3, 1)} horas")
        st.success(f"Costo de recarga: **Bs {round(kwh_a_recargar * PRECIO_KWH_BS, 2)}**")

if __name__ == "__main__":
    run_uyunitec_sim()
