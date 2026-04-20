import streamlit as st

def run_uyunitec_sim():
    TANQUE_MAX = 70 
    PRECIO_LITRO_BS = 6.96
    CONSUMO_LC_BASE = 22 

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción para Chery Fulwin T10 4x4")

    # --- 1. BARRA LATERAL (CONFIGURACIÓN) ---
    with st.sidebar:
        st.header("⛽ Combustible Inicial")
        gasolina_inicial = st.slider("Litros en el tanque:", 0, TANQUE_MAX, 70)
        
        st.write("---")
        st.header("🔌 Gestión de Energía")
        # LA NUEVA OPCIÓN DE EXPERIMENTACIÓN
        modo_energia = st.selectbox(
            "Modo de Conducción:",
            ["Híbrido Automático (Smart)", "Prioridad Motor Térmico (Save)", "Máximo Eléctrico (EV Mode)"]
        )
        st.info("El modo influye en cuánto esfuerzo hace el motor a gasolina.")

        st.write("---")
        st.header("🗺️ Ruta")
        distancia = st.number_input("Distancia (km)", value=100, min_value=1)
        terreno = st.selectbox("Terreno:", ["pavimento", "salar (seco)", "calamina", "arena"])
        altitud = st.slider("Altitud (msnm)", 3000, 5000, 3800)

    # --- 2. LÓGICA CON MODOS DE ENERGÍA ---
    # Factores según modo (cuánta gasolina usa relativo al base)
    factores_modo = {
        "Híbrido Automático (Smart)": 1.0,      # Consumo balanceado
        "Prioridad Motor Térmico (Save)": 1.15, # Gasta más gasolina para guardar batería
        "Máximo Eléctrico (EV Mode)": 0.70      # Ahorra gasolina usando la batería a tope
    }
    
    modificador_modo = factores_modo.get(modo_energia, 1.0)
    factores_terreno = {"pavimento": 1.0, "salar (seco)": 1.1, "calamina": 1.3, "arena": 1.6}
    
    penalizacion = factores_terreno.get(terreno, 1.0)
    eficiencia_altitud = max(0.6, 1 - (altitud / 12000)) 
    
    # Cálculo final ajustado por el modo elegido por el chofer
    consumo_ajustado = (5.75 * penalizacion * modificador_modo) / eficiencia_altitud
    litros_necesarios = round((distancia / 100) * consumo_ajustado, 2)

    # --- 3. RESULTADOS ---
    if st.button("🚀 Simular con este perfil"):
        litros_finales = round(gasolina_inicial - litros_necesarios, 2)
        porcentaje_final = max(0, int((litros_finales / TANQUE_MAX) * 100))
        ahorro = ((distancia / 100) * CONSUMO_LC_BASE * PRECIO_LITRO_BS) - (litros_necesarios * PRECIO_LITRO_BS)
        
        st.markdown(f"### Resultado en Modo: **{modo_energia}**")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Necesitas", f"{litros_necesarios} L")
        col2.metric("Ahorro", f"Bs {round(ahorro, 2)}")
        col3.metric("Llegada", f"{porcentaje_final}%")
        
        if litros_finales < 0:
            st.error(f"❌ **FALLO DE MISIÓN:** Con {modo_energia} te quedas corto por {abs(litros_finales)}L.")
        else:
            st.success(f"✅ **RUTA COMPLETADA:** Te quedan {litros_finales}L.")
            st.progress(porcentaje_final)

if __name__ == "__main__":
    run_uyunitec_sim()
