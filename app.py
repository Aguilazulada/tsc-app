import streamlit as st
import pandas as pd

def run_uyunitec_sim():
    # --- CONFIGURACIÓN DE LA MISIÓN ---
    TANQUE_TOTAL = 70  # Litros

    def simulador_uyunitec(distancia, terreno_tipo, altitud_avg):
        consumo_base = 5.75 
        
        # FACTORES DE TERRENO ACTUALIZADOS
        factores_terreno = {
            "pavimento": 1.0, 
            "salar (seco)": 1.1,  # Eficiente pero con resistencia salina
            "calamina": 1.3, 
            "arena": 1.6
        }
        
        penalizacion = factores_terreno.get(terreno_tipo, 1.0)
        eficiencia_altitud = max(0.6, 1 - (altitud_avg / 12000)) 
        
        consumo_final = (consumo_base * penalizacion) / eficiencia_altitud
        total_combustible = (distancia / 100) * consumo_final
        
        return round(total_combustible, 2)

    # --- INTERFAZ ---
    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción para Chery Fulwin T10 4x4")

    col_p, col_a = st.columns(2)
    with col_p:
        distancia = st.number_input("Distancia Total (km)", value=100)
        terreno = st.selectbox("Tipo de Terreno", ["pavimento", "salar (seco)", "calamina", "arena"])
    with col_a:
        altitud = st.slider("Altitud Promedio (msnm)", 3000, 5000, 3800)

    if st.button("🚀 Ejecutar Simulación"):
        litros = simulador_uyunitec(distancia, terreno, altitud)
        
        # Cálculos de Porcentaje
        porcentaje_usado = min(100, int((litros / TANQUE_TOTAL) * 100))
        porcentaje_restante = 100 - porcentaje_usado
        litros_restantes = round(TANQUE_TOTAL - litros, 2)
        
        costo_gasolina = 6.96
        costo_lc = (distancia / 100) * 22 * costo_gasolina
        costo_fulwin = litros * costo_gasolina
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Consumo Fulwin", f"{litros} L")
        c2.metric("Ahorro vs LC", f"Bs {round(costo_lc - costo_fulwin, 2)}")
        c3.metric("Tanque Restante", f"{porcentaje_restante}%")
        
        if litros > TANQUE_TOTAL:
            st.error(f"⚠️ ¡ALERTA! Te faltarían {abs(litros_restantes)} litros para llegar. Necesitas bidones.")
        else:
            st.success(f"✅ Te sobran {litros_restantes} litros ({porcentaje_restante}% del tanque).")
        
        # Barra de progreso mejorada
        st.write(f"**Uso del tanque: {porcentaje_usado}%**")
        st.progress(porcentaje_usado)


   
