import streamlit as st

def run_uyunitec_sim():
    # --- PARÁMETROS ---
    TANQUE_MAX = 70 
    BATERIA_MAX_KWH = 40  # Estimado para el sistema de largo alcance
    PRECIO_LITRO_BS = 6.96
    CONSUMO_LC_BASE = 22 

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción Híbrida 4x4")

    # --- 1. BARRA LATERAL: ESTADO DE ENERGÍA ---
    with st.sidebar:
        st.header("⚡ Estado Inicial")
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
        terreno = st.selectbox("Terreno:", ["pavimento", "salar (seco)", "calamina", "arena"])
        altitud = st.slider("Altitud (msnm)", 3000, 5000, 3800)

    # --- 2. LÓGICA DE CONSUMO DUAL ---
    factores_terreno = {"pavimento": 1.0, "salar (seco)": 1.1, "calamina": 1.3, "arena": 1.6}
    penalizacion = factores_terreno.get(terreno, 1.0)
    eficiencia_altitud = max(0.6, 1 - (altitud / 12000))
    
    # Lógica de desgaste de batería según el modo
    descarga_bateria_base = (distancia / 4)  # Supuesto: 400km de rango EV ideal
    if modo_energia == "Máximo Eléctrico (EV Mode)":
        consumo_gasolina_factor = 0.65
        descarga_bateria_factor = 1.4
    elif modo_energia == "Prioridad Motor Térmico (Save)":
        consumo_gasolina_factor = 1.2
        descarga_bateria_factor = 0.2 # Casi no gasta batería
    else: # Smart
        consumo_gasolina_factor = 1.0
        descarga_bateria_factor = 1.0

    # Cálculo final
    consumo_l = (5.75 * penalizacion * consumo_gasolina_factor) / eficiencia_altitud
    litros_necesarios = round((distancia / 100) * consumo_l, 2)
    
    perdida_bateria = (descarga_bateria_base * penalizacion * descarga_bateria_factor) / eficiencia_altitud
    bateria_final = round(bateria_inicial - perdida_bateria, 1)

    # --- 3. DASHBOARD DE RESULTADOS ---
    if st.button("🚀 Ejecutar Simulación"):
        litros_finales = round(gasolina_inicial - litros_necesarios, 2)
        ahorro = ((distancia / 100) * CONSUMO_LC_BASE * PRECIO_LITRO_BS) - (litros_necesarios * PRECIO_LITRO_BS)
        
        st.markdown(f"### Análisis de Energía: {modo_energia}")
        
        # Tres métricas principales
        m1, m2, m3 = st.columns(3)
        m1.metric("Gasolina Necesaria", f"{litros_necesarios} L")
        m2.metric("Ahorro vs LC", f"Bs {round(ahorro, 2)}")
        m3.metric("Batería al Llegar", f"{max(0, bateria_final)}%")
        
        st.write("---")
        
        # Visualización dual de depósitos
        col_gas, col_bat = st.columns(2)
        
        with col_gas:
            st.write(f"⛽ **Depósito Gasolina:** {max(0, litros_finales)}L")
            porc_gas = max(0, int((litros_finales / TANQUE_MAX) * 100))
            st.progress(porc_gas)
            if litros_finales < 5: st.warning("⚠️ Combustible en reserva")

        with col_bat:
            st.write(f"⚡ **Nivel de Batería:** {max(0, bateria_final)}%")
            st.progress(max(0, int(bateria_final)))
            if bateria_final < 15: st.warning("⚠️ Batería baja")

        # Mensaje de Misión
        if litros_finales < 0 and bateria_final <= 0:
            st.error("❌ **MISIÓN FALLIDA:** Te quedas sin energía total antes de llegar.")
        elif litros_finales < 0:
            st.warning("⛽ Sin gasolina, pero podrías intentar llegar con lo que queda de batería.")
        else:
            st.success(f"✅ **MISIÓN VIABLE:** Llegas con un colchón de {litros_finales}L de combustible.")

if __name__ == "__main__":
    run_uyunitec_sim()
