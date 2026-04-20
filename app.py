import streamlit as st
def run_uyunitec_sim():
    # --- 1. PARÁMETROS CALIBRADOS (Realidad Altiplano) ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40
    PRECIO_KWH_BS = 0.85 
    CONSUMO_LC_BASE = 22 
    
    # Tus leyes de rendimiento real:
    KM_POR_LITRO = 13.5
    KM_POR_PORCENTAJE_BAT = 1.5 # 100% = 150km

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción Híbrida 4x4")

    # --- 2. CONFIGURACIÓN EN BARRA LATERAL ---
    with st.sidebar:
        st.header("⛽ Energía Disponible")
        precio_gasolina = st.number_input("Precio Gasolina (Bs/L):", value=6.96, step=0.01)
        gasolina_inicial = st.slider("Litros actuales en tanque:", 0, TANQUE_MAX, 70)
        bateria_inicial = st.slider("Carga actual Batería (%):", 0, 100, 100)
        
        st.write("---")
        st.header("🔌 Gestión de Motores")
        modo_energia = st.selectbox(
            "Modo de Conducción:",
            ["Híbrido Automático (Smart)", "Prioridad Motor Térmico (Save)", "Máximo Eléctrico (EV Mode)"]
        )

        st.write("---")
        st.header("🗺️ Parámetros de Ruta")
        distancia = st.number_input("Distancia a recorrer (km)", value=100, min_value=1)
        terreno = st.selectbox("Terreno:", ["pavimento", "salar (seco)", "tierra/terroso", "calamina", "arena"])
        altitud = st.slider("Altitud Promedio (msnm)", 3000, 5000, 3800)

    # --- 3. LÓGICA DE CONSUMO ---
    factores_terreno = {"pavimento": 1.0, "salar (seco)": 1.1, "tierra/terroso": 1.2, "calamina": 1.3, "arena": 1.6}
    penalizacion = factores_terreno.get(terreno, 1.0)
    eficiencia_altitud = max(0.6, 1 - (altitud / 12000))
    
    # Factores según el modo elegido
    c_gas_f = {"Híbrido Automático (Smart)": 1.0, "Prioridad Motor Térmico (Save)": 1.25, "Máximo Eléctrico (EV Mode)": 0.65}[modo_energia]
    c_bat_f = {"Híbrido Automático (Smart)": 1.0, "Prioridad Motor Térmico (Save)": 0.2, "Máximo Eléctrico (EV Mode)": 1.5}[modo_energia]

    litros_nec = (distancia / KM_POR_LITRO) * penalizacion * c_gas_f / eficiencia_altitud
    porc_bat_nec = (distancia / KM_POR_PORCENTAJE_BAT) * penalizacion * c_bat_f / eficiencia_altitud
    
    # --- 4. RESULTADOS AL EJECUTAR ---
    if st.button("🚀 Ejecutar Simulación de Misión"):
        l_fin = round(gasolina_inicial - litros_nec, 2)
        b_fin = round(bateria_inicial - porc_bat_nec, 1)
        
        st.markdown("### 📊 Estado de Energía al Llegar")
        
        col_g, col_b = st.columns(2)
        with col_g:
            p_gas = max(0, int((l_fin / TANQUE_MAX) * 100))
            st.write(f"⛽ **Gasolina: {p_gas}%** ({max(0, l_fin)}L)")
            st.progress(p_gas)
            if 0 < l_fin <= 10:
                km_reserva_g = round(max(0, l_fin) * KM_POR_LITRO, 1)
                st.warning(f"⚠️ **RESERVA:** {max(0, l_fin)}L restantes (~{km_reserva_g} km)")
            elif l_fin <= 0:
                st.error("🚨 GASOLINA AGOTADA")

        with col_b:
            p_bat = max(0, int(b_fin))
            st.write(f"⚡ **Batería: {p_bat}%**")
            st.progress(p_bat)
            if 0 < b_fin <= 10:
                km_reserva_b = round(max(0, b_fin) * KM_POR_PORCENTAJE_BAT, 1)
                st.warning(f"⚠️ **CRÍTICO:** {p_bat}% restante (~{km_reserva_b} km)")
            elif b_fin <= 0:
                st.error("🚨 BATERÍA AGOTADA")

        st.write("---")
        
        # --- SECCIÓN ECONÓMICA Y AHORRO ---
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * precio_gasolina
        costo_gas_fulwin = litros_nec * precio_gasolina
        ahorro_gasolina = costo_lc - costo_gas_fulwin
        
        # Ahorro por haber usado electricidad en lugar de gasolina
        km_ev_puros = (distancia - (litros_nec * KM_POR_LITRO))
        ahorro_uso_ev = max(0, (km_ev_puros / KM_POR_LITRO * precio_gasolina) - (porc_bat_nec/100 * BATERIA_MAX_KWH * PRECIO_KWH_BS))

        st.subheader("💰 Análisis de Ahorro para el Chofer")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ahorro Gasolina", f"Bs {round(ahorro_gasolina, 2)}")
        c2.metric("Ahorro Uso EV", f"Bs {round(ahorro_uso_ev, 2)}")
        c3.metric("Alcance Final", f"~{round(max(0,l_fin)*KM_POR_LITRO + max(0,b_fin)*KM_POR_PORCENTAJE_BAT, 1)} km")

        # --- SECCIÓN DE RECARGA ---
        st.write("---")
        st.subheader("🕒 Logística y Costo de Recarga")
        kwh_a_recargar = BATERIA_MAX_KWH * (1 - (max(0, b_fin)/100))
        
        tr1, tr2 = st.columns(2)
        tr1.info(f"**Enchufe Pared (2.3kW):**\n\n{round(kwh_a_recargar/2.3, 1)} horas")
        tr2.info(f"**Cargador Rápido (DC):**\n\n~45 min (al 80%)")
        
        st.success(f"Cargar los kWh consumidos te costará solo **Bs {round(kwh_a_recargar * PRECIO_KWH_BS, 2)}**")

if __name__ == "__main__":
    run_uyunitec_sim()
