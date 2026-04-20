import streamlit as st

def run_uyunitec_sim():
    # --- 1. PARÁMETROS FIJOS ---
    TANQUE_TOTAL = 70  # Litros del Fulwin T10
    PRECIO_LITRO_BS = 6.96
    CONSUMO_LC_BASE = 22 # Litros/100km Land Cruiser

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción para Chery Fulwin T10 4x4")

    # --- 2. ENTRADAS DE USUARIO ---
    col_p, col_a = st.columns(2)
    with col_p:
        distancia = st.number_input("Distancia Total (km)", value=100, min_value=1)
        terreno = st.selectbox("Tipo de Terreno", ["pavimento", "salar (seco)", "calamina", "arena"])
    with col_a:
        altitud = st.slider("Altitud Promedio (msnm)", 3000, 5000, 3800)

    # --- 3. LÓGICA DE CÁLCULO ---
    # Factores de fricción
    factores_terreno = {
        "pavimento": 1.0, 
        "salar (seco)": 1.1, 
        "calamina": 1.3, 
        "arena": 1.6
    }
    
    penalizacion = factores_terreno.get(terreno, 1.0)
    # Pérdida de eficiencia por oxígeno (Motor térmico sufre, eléctrico apoya)
    eficiencia_altitud = max(0.6, 1 - (altitud / 12000)) 
    
    # Consumo final estimado (L/100km)
    consumo_estimado_100km = (5.75 * penalizacion) / eficiencia_altitud
    total_litros_necesarios = round((distancia / 100) * consumo_estimado_100km, 2)

    # --- 4. RESULTADOS ---
    if st.button("🚀 Ejecutar Simulación"):
        porcentaje_usado = min(100, int((total_litros_necesarios / TANQUE_TOTAL) * 100))
        porcentaje_restante = 100 - porcentaje_usado
        litros_restantes = round(TANQUE_TOTAL - total_litros_necesarios, 2)
        
        # Comparativa Económica
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * PRECIO_LITRO_BS
        costo_fulwin = total_litros_necesarios * PRECIO_LITRO_BS
        ahorro = costo_lc - costo_fulwin
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Consumo Fulwin", f"{total_litros_necesarios} L")
        c2.metric("Ahorro vs LC", f"Bs {round(ahorro, 2)}")
        c3.metric("Tanque Restante", f"{porcentaje_restante}%")
        
        # Barra de progreso y alertas
        st.write(f"**Estado del Tanque (Queda el {porcentaje_restante}%)**")
        st.progress(porcentaje_restante) # Ahora la barra muestra lo que queda

        if total_litros_necesarios > TANQUE_TOTAL:
            st.error(f"⚠️ ¡ALERTA! Te faltan {abs(litros_restantes)} L. ¡Lleva bidones!")
        else:
            st.success(f"✅ Misión viable. Te sobran {litros_restantes} L en el tanque.")

# Esto es para que no falle al importar
if __name__ == "__main__":
    run_uyunitec_sim()
   
