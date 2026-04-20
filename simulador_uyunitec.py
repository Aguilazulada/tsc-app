import streamlit as st

def run_uyunitec_x3l_v2():
    # --- 1. PARÁMETROS TÉCNICOS X3L ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40
    PESO_KG = 1892
    PRECIO_KWH_BS = 0.85 
    CONSUMO_LC_BASE = 22 
    KM_LITRO_GAS = 13.5
    KM_POR_100_BAT = 150 

    st.title("🏔️ UyuniTec: Simulador Fulwin X3L")
    st.subheader("Plataforma de Expedición Inteligente")

    # --- 2. ENTRADAS ---
    with st.sidebar:
        st.header("⛽ Energía y Costos")
        precio_gasolina = st.number_input("Precio Gasolina (Bs/L):", value=6.96, step=0.01)
        gasolina_inicial = st.slider("Litros actuales:", 0, TANQUE_MAX, 70)
        bateria_inicial = st.slider("Batería inicial (%):", 0, 100, 100)
        
        st.write("---")
        modo_energia = st.selectbox(
            "Modo de Conducción:",
            ["Híbrido Automático (Smart)", "Prioridad Térmico (Save)", "Máximo Eléctrico (EV Mode)"]
        )
        distancia = st.number_input("Distancia Ruta (km)", value=100, min_value=1)
        # NUEVO TERRENO: SALAR CON AGUA
        terreno = st.selectbox("Suelo:", ["pavimento", "salar (seco)", "salar (con agua/espejo)", "tierra/terroso", "calamina", "arena"])
        altitud = st.slider("Altitud (msnm)", 3000, 5000, 3800)

    # --- 3. LÓGICA DE CONSUMO RECALIBRADA ---
    f_terreno = {
        "pavimento": 1.0, 
        "salar (seco)": 1.1, 
        "salar (con agua/espejo)": 1.45, # Resistencia hidrodinámica alta
        "tierra/terroso": 1.15, 
        "calamina": 1.25, 
        "arena": 1.6
    }
    penalizacion = f_terreno.get(terreno, 1.0)
    
    eficiencia_gas = max(0.6, 1 - (altitud / 12000))
    eficiencia_bat = max(0.85, 1 - (altitud / 25000)) 
    
    if modo_energia == "Máximo Eléctrico (EV Mode)":
        esf_gas, esf_bat = 0.05, 1.0 
    elif modo_energia == "Prioridad Térmico (Save)":
        esf_gas, esf_bat = 1.15, 0.1 
    else:
        esf_gas, esf_bat = 0.75, 0.75

    litros_nec = (distancia / KM_LITRO_GAS) * penalizacion * esf_gas / eficiencia_gas
    porc_bat_nec = (distancia / KM_POR_100_BAT * 100) * penalizacion * esf_bat / eficiencia_bat
    
    # --- 4. DASHBOARD ---
    if st.button("🚀 Iniciar Simulación X3L"):
        l_fin = round(gasolina_inicial - litros_nec, 2)
        b_fin = round(bateria_inicial - porc_bat_nec, 1)
        
        st.markdown("### 📊 Energía al Destino")
        cg, cb = st.columns(2)
        
        with cg:
            p_gas = max(0, int((l_fin / TANQUE_MAX) * 100))
            st.write(f"⛽ Gasolina: {p_gas}% ({max(0, l_fin)}L)")
            st.progress(p_gas)
            if 0 < l_fin <= 10: st.warning(f"⚠️ Reserva: ~{round(max(0, l_fin)*KM_LITRO_GAS, 1)} km")

        with cb:
            p_bat = max(0, int(b_fin))
            st.write(f"⚡ Batería: {p_bat}%")
            st.progress(p_bat)
            if 0 < b_fin <= 10: st.warning(f"⚠️ Crítico: ~{round(max(0, b_fin)*1.5, 1)} km")

        # --- FUNCIÓN TURN TANK ---
        st.write("---")
        st.subheader("🔄 Turn Tank (Giro 360°)")
        if terreno == "salar (con agua/espejo)":
            st.warning("⚡ El giro sobre eje en agua requiere alta tracción. Verifique nivel de batería.")
        
        if b_fin > 15: st.success("✅ Energía disponible para maniobras.")
        else: st.error("❌ Batería baja para Turn Tank.")

        # --- AHORRO Y ALCANCE ---
        st.write("---")
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * precio_gasolina
        costo_gas_fulwin = litros_nec * precio_gasolina
        km_ev_equiv = (porc_bat_nec / 100) * KM_POR_100_BAT
        ahorro_ev = max(0, (km_ev_equiv / KM_LITRO_GAS * precio_gasolina) - (porc_bat_nec/100 * BATERIA_MAX_KWH * PRECIO_KWH_BS))

        c1, c2, c3 = st.columns(3)
        c1.metric("Ahorro Combustible", f"Bs {round(costo_lc - costo_gas_fulwin, 2)}")
        c2.metric("Ahorro por Uso EV", f"Bs {round(ahorro_ev, 2)}")
        c3.metric("Alcance Final", f"~{round(max(0,l_fin)*KM_LITRO_GAS + max(0,b_fin)*1.5, 1)} km")

        # --- FICHA TÉCNICA RÁPIDA ---
        with st.expander("📝 Ficha Técnica del Vehículo (X3L)"):
            st.write(f"**Peso en vacío:** {PESO_KG} kg")
            st.write("**Sistema:** Híbrido Enchufable de alta eficiencia")
            st.write("**Maniobra Especial:** Turn Tank (Giro sobre eje)")
            st.write(f"**Costo de recarga completa (40kWh):** Bs {round(BATERIA_MAX_KWH * PRECIO_KWH_BS, 2)}")

if __name__ == "__main__":
    run_uyunitec_x3l_v2()
