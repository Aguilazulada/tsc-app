import streamlit as st

def run_uyunitec_x3l_v5():
    # --- 1. CONSTANTES TÉCNICAS (X3L) ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40
    PRECIO_KWH_BS = 0.85 
    KM_LITRO_GAS = 13.5
    RENDIMIENTO_BAT_BASE = 1.5 
    CONSUMO_LC_100KM = 22 

    st.title("🏔️ UyuniTec: Simulador Fulwin X3L")
    st.subheader("Cerebro v5.0: Salar, Agua y Viento")

    # --- 2. ENTRADAS LATERALES ---
    with st.sidebar:
        st.header("⛽ Energía Inicial")
        precio_gas_bs = st.number_input("Precio Gasolina (Bs/L):", value=6.96)
        gas_ini = st.slider("Litros actuales:", 0, TANQUE_MAX, 70)
        bat_ini = st.slider("Carga Batería (%):", 0, 100, 100)
        
        st.write("---")
        st.header("🗺️ Factores de Ruta")
        distancia = st.number_input("Distancia Ruta (km):", value=100)
        
        # INCLUSIÓN DE TERRENO CRÍTICO
        terreno = st.selectbox("Tipo de Suelo:", 
                               ["pavimento", "salar (seco)", "salar (con agua/espejo)", "tierra", "calamina", "arena"])
        
        # FACTOR VIENTO
        viento_fuerte = st.checkbox("💨 Viento fuerte en contra (Lagunas/Sol de Mañana)")
        
        st.write("---")
        modo = st.selectbox("Modo de Conducción:", ["Híbrido Automático (Smart)", "Prioridad Térmico (Save)", "Máximo Eléctrico (EV Mode)"])

    # --- 3. LÓGICA DE CÁLCULO ---
    f_suelo = {
        "pavimento": 1.0, 
        "salar (seco)": 1.1, 
        "salar (con agua/espejo)": 1.45, 
        "tierra": 1.15, 
        "calamina": 1.25, 
        "arena": 1.6
    }
    penalizacion = f_suelo.get(terreno, 1.0)
    
    # Aplicación del factor viento (15% extra de esfuerzo)
    if viento_fuerte:
        penalizacion *= 1.15

    # Esfuerzo por modo
    if modo == "Máximo Eléctrico (EV Mode)":
        g_coef, b_coef = 0.05, 1.0
    elif modo == "Prioridad Térmico (Save)":
        g_coef, b_coef = 1.25, 0.1
    else:
        g_coef, b_coef = 0.75, 0.75

    # Consumo Final
    litros_gastados = (distancia / KM_LITRO_GAS) * penalizacion * g_coef
    bat_gastada = (distancia / RENDIMIENTO_BAT_BASE) * penalizacion * b_coef
    
    # --- 4. DASHBOARD DE RESULTADOS ---
    if st.button("🚀 Iniciar Simulación de Misión"):
        l_fin = max(0.0, gas_ini - litros_gastados)
        b_fin = max(0.0, bat_ini - bat_gastada)
        
        st.markdown("### 📊 Estado al Llegar")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("⛽ Gasolina", f"{int((l_fin/TANQUE_MAX)*100)}%", f"{round(l_fin,1)} L")
            st.progress(int((l_fin/TANQUE_MAX)*100))
        with c2:
            st.metric("⚡ Batería", f"{int(b_fin)}%", f"-{round(bat_gastada,1)}%")
            st.progress(int(b_fin))

        # --- ANÁLISIS DE AHORRO ---
        costo_lc = (distancia / 100) * CONSUMO_LC_100KM * precio_gas_bs
        costo_gas_fw = litros_gastados * precio_gas_bs
        
        # Kilómetros que la batería "cubrió" realmente
        km_cubiertos_bat = (bat_gastada * RENDIMIENTO_BAT_BASE) / penalizacion
        ahorro_ev_puro = (km_cubiertos_bat / KM_LITRO_GAS * precio_gas_bs) - (bat_gastada/100 * BATERIA_MAX_KWH * PRECIO_KWH_BS)

        st.write("---")
        st.subheader("💰 Rentabilidad y Ahorro")
        a, b, c = st.columns(3)
        a.metric("Vs Land Cruiser", f"Bs {round(costo_lc - costo_gas_fw, 2)}")
        b.metric("Ahorro Uso EV", f"Bs {round(max(0, ahorro_ev_puro), 2)}")
        c.metric("Alcance Total", f"~{round(l_fin*KM_LITRO_GAS + b_fin*RENDIMIENTO_BAT_BASE, 1)} km")

        # --- LOGÍSTICA ---
        st.write("---")
        kwh_usados = (bat_gastada / 100) * BATERIA_MAX_KWH
        st.info(f"🕒 **Carga Necesaria:** {round(kwh_usados/2.3, 1)} horas (Pared) | **Costo:** Bs {round(kwh_usados * PRECIO_KWH_BS, 2)}")
        
        if terreno == "salar (con agua/espejo)":
            st.warning("⚠️ **Aviso de Tracción:** El Salar inundado aumenta el arrastre. Monitoree la temperatura del sistema híbrido.")

if __name__ == "__main__":
    run_uyunitec_x3l_v5()
