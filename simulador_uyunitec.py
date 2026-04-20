import streamlit as st
import pandas as pd

def run_uyunitec_sim():
    # --- CONFIGURACIÓN DE LA MISIÓN ---
    ST_GRAVITY = 9.81
    AIR_DENSITY_SEA_LEVEL = 1.225  # kg/m^3

    def calcular_resistencia_aire(altitud, velocidad_kmh):
        # La densidad del aire baja con la altura (ventaja para el auto)
        densidad_aire = AIR_DENSITY_SEA_LEVEL * (1 - (0.000022557 * altitud))**5.255
        v_ms = velocidad_kmh / 3.6
        # Cd del Fulwin T10 aprox 0.30
        fuerza_arrastre = 0.5 * densidad_aire * (v_ms**2) * 0.30 * 2.5 
        return fuerza_arrastre

    def simulador_uyunitec(distancia, terreno_tipo, altitud_avg):
        # Consumo base del Fulwin T10 en modo híbrido (L/100km)
        consumo_base = 5.75 # Ajustado a nuestra comparativa ruda
        
        # Penalización por terreno (Calamina = +30%, Arena = +60%)
        factores_terreno = {"pavimento": 1.0, "calamina": 1.3, "arena": 1.6}
        penalizacion = factores_terreno.get(terreno_tipo, 1.0)
        
        # El motor térmico sufre en la altura (compensamos con motores eléctricos)
        eficiencia_motor_termico = max(0.6, 1 - (altitud_avg / 12000)) 
        
        consumo_final = (consumo_base * penalizacion) / eficiencia_motor_termico
        total_combustible = (distancia / 100) * consumo_final
        
        return round(total_combustible, 2)

    # --- INTERFAZ STREAMLIT ---
    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción para Chery Fulwin T10 4x4")

    st.info("Comparando rendimiento vs. Land Cruiser automática clásica.")

    col_p, col_a = st.columns(2)
    with col_p:
        distancia = st.number_input("Distancia Total (km)", value=100)
        terreno = st.selectbox("Tipo de Terreno", ["pavimento", "calamina", "arena"])
    with col_a:
        altitud = st.slider("Altitud Promedio (msnm)", 3000, 5000, 3800)

    if st.button("🚀 Ejecutar Simulación"):
        litros = simulador_uyunitec(distancia, terreno, altitud)
        
        # Comparativa Ruda y Cruda
        costo_gasolina = 6.96 # Bs por litro (Especial+)
        costo_lc = (distancia / 100) * 22 * costo_gasolina # LC gasta 22L/100km
        costo_fulwin = litros * costo_gasolina
        ahorro = costo_lc - costo_fulwin
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Consumo Fulwin", f"{litros} L")
        c2.metric("Costo Estimado", f"Bs {round(costo_fulwin, 2)}")
        c3.metric("Ahorro vs LC", f"Bs {round(ahorro, 2)}", delta_color="normal")
        
        st.success(f"✅ Con el tanque de 70L del Fulwin, te sobrarían {round(70 - litros, 2)} litros.")
        
        # Barra de progreso de tanque
        st.progress(max(0, min(100, int((litros/70)*100))), text="Uso del tanque (%)")

# Para ejecutarlo como módulo independiente
if __name__ == "__main__":
    run_uyunitec_sim()
       
   
        
       
