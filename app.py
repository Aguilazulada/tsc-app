import streamlit as st

def run_uyunitec_sim():
    # --- 1. PARÁMETROS CALIBRADOS ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40  
    PRECIO_KWH_BS = 0.85 
    CONSUMO_LC_BASE = 22 
    
    # Tus factores de rendimiento real:
    KM_POR_LITRO = 13.5
    KM_POR_PORCENTAJE_BAT = 1.5 # 100% = 150km

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción Híbrida 4x4")

    # --- 2. ENTRADAS ---
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

    # --- 3. LÓGICA DE CONSUMO ---
    factores_terreno = {"pavimento": 1.0, "salar (seco)": 1.1, "tierra/terroso": 1.2, "calamina": 1.3, "arena": 1.6}
    penalizacion = factores_terreno.get(terreno, 1.0)
    eficiencia_altitud = max(0.6, 1 - (altitud / 12000))
    
    # Factores según modo
    c_gas_f = {"Híbrido Automático (Smart)": 1.0, "Prioridad Térmico (Save)": 1.25, "Máximo Eléctrico (EV Mode)": 0.65}[modo_energia]
    c_bat_f = {"Híbrido Automático (Smart)": 1.0, "Prioridad Térmico (Save)": 0.2, "Máximo Eléctrico (EV Mode)": 1.5}[modo_energia]

    # Cálculo basado en tus rendimientos
    litros_nec = (distancia / KM_POR_LITRO) * penalizacion * c_gas_f / eficiencia_altitud
    porc_bat_nec = (distancia / KM_POR_PORCENTAJE_BAT) * penalizacion * c_bat_f / eficiencia_altitud
    
    # --- 4. DASHBOARD VISUAL ---
    if st.button("🚀 Iniciar Simulación"):
        l_fin = round(gasolina_inicial - litros_nec, 2)
        b_fin = round(bateria_inicial - porc_bat_nec, 1)
        
        st.markdown("### 📊 Estado Final de Energía")
        
        col_g, col_b = st.columns(2)
        with col_g:
            p_gas = max(0, int((l_fin / TANQUE_MAX) * 100))
            st.write(f"⛽ **Gasolina: {p_gas}%** ({max(0, l_fin)}L)")
            st.progress(p_gas)
            if 0 < l_fin <= 10:
                km_reserva_g = round(max(0, l_fin) * KM_POR_LITRO, 1)
                st.warning(f"⚠️ **RESERVA:** Te quedan {max(0, l_fin)}L (~{km_reserva_g} km)")
            elif l_fin <= 0:
                st.error("🚨 TANQUE VACÍO")

        with col_b:
            p_bat = max(0, int(b_fin))
            st.write(f"⚡ **Batería: {p_bat}%**")
            st.progress(p_bat)
            if 0 < b_fin <= 10:
                km_reserva_b = round(max(0, b_fin) * KM_POR_PORCENTAJE_BAT, 1)
                st.warning(f"⚠️ **BATERÍA CRÍTICA:** Te queda {p_bat}% (~{km_reserva_b} km)")
            elif b_fin <= 0:
                st.error("🚨 BATERÍA AGOTADA")

        st.write("---")
        # Comparativa y Ahorro
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * precio_gasolina
        costo_total_fulwin = (litros_nec * precio_gasolina) + ((porc_bat_nec/100*BATERIA_MAX_KWH)*PRECIO_KWH_BS)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Gasto Fulwin", f"Bs {round(costo_total_fulwin, 2)}")
        c2.metric("Ahorro Neto", f"Bs {round(costo_lc - costo_total_fulwin, 2)}")
        c3.metric("Alcance Final", f"~{round(max(0,l_fin)*KM_POR_LITRO + max(0,b_fin)*KM_POR_PORCENTAJE_BAT, 1)} km")

        st.info(f"💡 Autonomía Total Restante: Tienes combustible y carga para recorrer aproximadamente {round(max(0,l_fin)*KM_POR_LITRO + max(0,b_fin)*KM_POR_PORCENTAJE_BAT, 1)} km más.")

if __name__ == "__main__":
    run_uyunitec_sim()
