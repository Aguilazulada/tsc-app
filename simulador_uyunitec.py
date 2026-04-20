import streamlit as st

def run_uyunitec_x3l_v3():
    # --- 1. CONSTANTES TÉCNICAS (X3L) ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40
    PRECIO_KWH_BS = 0.85 
    KM_LITRO_GAS = 13.5
    RENDIMIENTO_BAT_BASE = 1.5 
    CONSUMO_LC_100KM = 22 

    st.title("🏔️ UyuniTec: Simulador Fulwin X3L")
    st.subheader("Cerebro de Expedición Calibrado v3.1")

    # --- 2. ENTRADAS LATERALES ---
    with st.sidebar:
        st.header("⛽ Energía Inicial")
        precio_gas_bs = st.number_input("Precio Gasolina (Bs/L):", value=6.96)
        gas_ini = st.slider("Litros actuales:", 0, TANQUE_MAX, 70)
        bat_ini = st.slider("Carga Batería (%):", 0, 100, 100)
        
        st.write("---")
        st.header("🗺️ Parámetros de Ruta")
        distancia = st.number_input("Distancia Total (km):", value=100)
        # TERRENO ACTUALIZADO: INCLUYE SALAR CON AGUA
        terreno = st.selectbox("Tipo de Suelo:", 
                               ["pavimento", "salar (seco)", "salar (con agua/espejo)", "tierra", "calamina", "arena"])
        viento_en_contra = st.checkbox("💨 ¿Viento fuerte en contra?")
        altitud = st.slider("Altitud (msnm):", 3000, 5000, 3800)
        
        st.write("---")
        modo = st.selectbox("Estrategia de Motores:", 
                            ["Híbrido Automático (Smart)", "Prioridad Térmico (Save)", "Máximo Eléctrico (EV Mode)"])

    # --- 3. LÓGICA DE CONSUMO RECALIBRADA ---
    f_suelo = {
        "pavimento": 1.0, 
        "salar (seco)": 1.1, 
        "salar (con agua/espejo)": 1.45, # Factor de succión e inercia
        "tierra": 1.15, 
        "calamina": 1.25, 
        "arena": 1.6
    }
    penalizacion = f_suelo.get(terreno, 1.0)
    
    # Factor Viento: Suma 15% de esfuerzo si está activo
    f_viento = 1.15 if viento_en_contra else 1.0
    
    # Ajuste por altitud
    ajuste_alt_gas = 1 + ((altitud - 3000) / 6000) 
    ajuste_alt_bat = 1 + ((altitud - 3000) / 12000)

    # Esfuerzo según modo
    if modo == "Máximo Eléctrico (EV Mode)":
        g_uso, b_uso = 0.05, 1.0 
    elif modo == "Prioridad Térmico (Save)":
        g_uso, b_uso = 1.25, 0.1  
    else:
        g_uso, b_uso = 0.75, 0.75

    # Cálculo de consumo total
    litros_gastados = (distancia / KM_LITRO_GAS) * penalizacion * f_viento * g_uso * ajuste_alt_gas
    bat_gastada = (distancia / RENDIMIENTO_BAT_BASE) * penalizacion * f_viento * b_uso * ajuste_alt_bat
    
    # --- 4. RESULTADOS ---
    if st.button("🚀 Ejecutar Misión"):
        l_fin = max(0.0, gas_ini - litros_gastados)
        b_fin = max(0.0, bat_ini - bat_gastada)
        
        st.markdown("### 📊 Estado Final de Energía")
        col_g, col_b = st.columns(2)
        
        with col_g:
            st.metric("⛽ Gasolina", f"{int((l_fin/TANQUE_MAX)*100)}%", f"{round(l_fin,1)} L")
            st.progress(int((l_fin/TANQUE_MAX)*100))
            if l_fin <= 10: st.warning(f"⚠️ Reserva: ~{round(l_fin * KM_LITRO_GAS, 1)} km")

        with col_b:
            st.metric("⚡ Batería", f"{int(b_fin)}%", f"-{round(bat_gastada,1)}%")
            st.progress(int(b_fin))
            if b_fin <= 10: st.warning(f"⚠️ Crítico: ~{round(b_fin * RENDIMIENTO_BAT_BASE, 1)} km")

        # --- ANÁLISIS ECONÓMICO ---
        st.write("---")
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * precio_gas_bs
        costo_gas_fw = litros_gastados * precio_gas_bs
        
        # Ahorro EV: Comparativa de km cubiertos por batería vs su costo en gas
        km_ev = (bat_gastada * RENDIMIENTO_BAT_BASE) / (penalizacion * f_viento)
        ahorro_luz = (km_ev / KM_LITRO_GAS * precio_gas_bs) - (bat_gastada/100 * BATERIA_MAX_KWH * PRECIO_KWH_BS)

        st.subheader("💰 Rentabilidad de la Ruta")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ahorro vs LC", f"Bs {round(costo_lc - costo_gas_fw, 2)}")
        c2.metric("Ahorro Uso EV", f"Bs {round(max(0, ahorro_luz), 2)}")
        c3.metric("Alcance Final", f"~{round(l_fin*KM_LITRO_GAS + b_fin*RENDIMIENTO_BAT_BASE, 1)} km")

        # --- LOGÍSTICA DE CARGA ---
        st.write("---")
        st.subheader("🕒 Recuperación de Energía")
        kwh_usados = (bat_gastada / 100) * BATERIA_MAX_KWH
        st.info(f"Para recuperar el nivel actual, necesitas **{round(kwh_usados/2.3, 1)} horas** en enchufe de pared.")
        st.success(f"Costo de la recarga: **Bs {round(kwh_usados * PRECIO_KWH_BS, 2)}**")

if __name__ == "__main__":
    run_uyunitec_x3l_v3()
        
       
        
   
        
        
        
