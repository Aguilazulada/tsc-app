import streamlit as st

def run_uyunitec_sim():
    # --- 1. PARÁMETROS FIJOS ---
    TANQUE_MAX = 70  # Capacidad total del Fulwin T10
    PRECIO_LITRO_BS = 6.96
    CONSUMO_LC_BASE = 22 # Litros/100km Land Cruiser

    st.title("🏔️ UyuniTec: Simulador de Misión")
    st.subheader("Cerebro de Predicción para Chery Fulwin T10 4x4")

    # --- 2. ENTRADAS DE USUARIO ---
    with st.sidebar:
        st.header("⛽ Estado del Tanque")
        # El ícono y la capacidad
        st.write(f"📂 **Capacidad Total:** {TANQUE_MAX} Litros")
        gasolina_inicial = st.slider("¿Con cuántos litros sales?", 0, TANQUE_MAX, 70)
        
        st.write("---")
        st.header("🗺️ Parámetros de Ruta")
        distancia = st.number_input("Distancia Total (km)", value=100, min_value=1)
        terreno = st.selectbox("Tipo de Terreno", ["pavimento", "salar (seco)", "calamina", "arena"])
        altitud = st.slider("Altitud Promedio (msnm)", 3000, 5000, 3800)

    # --- 3. LÓGICA DE CÁLCULO ---
    factores_terreno = {"pavimento": 1.0, "salar (seco)": 1.1, "calamina": 1.3, "arena": 1.6}
    penalizacion = factores_terreno.get(terreno, 1.0)
    eficiencia_altitud = max(0.6, 1 - (altitud / 12000)) 
    
    consumo_estimado_100km = (5.75 * penalizacion) / eficiencia_altitud
    litros_necesarios = round((distancia / 100) * consumo_estimado_100km, 2)

    # --- 4. RESULTADOS ---
    if st.button("🚀 Ejecutar Simulación de Misión"):
        litros_finales = round(gasolina_inicial - litros_necesarios, 2)
        porcentaje_final = max(0, int((litros_finales / TANQUE_MAX) * 100))
        
        # Comparativa Económica
        costo_lc = (distancia / 100) * CONSUMO_LC_BASE * PRECIO_LITRO_BS
        costo_fulwin = litros_necesarios * PRECIO_LITRO_BS
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Consumo Necesario", f"{litros_necesarios} L")
        col2.metric("Ahorro vs LC", f"Bs {round(costo_lc - costo_fulwin, 2)}")
        col3.metric("Nivel al Llegar", f"{porcentaje_final}%")
        
        # --- EL TABLERO REALISTA ---
        st.write(f"### 📊 Estado de Combustible")
        
        if litros_finales < 0:
            st.error(f"❌ **MISIÓN IMPOSIBLE:** Te faltarían {abs(litros_finales)} litros para completar la ruta con lo que tienes.")
            st.warning("Necesitas cargar gasolina antes de salir o llevar bidones extra.")
            st.progress(0)
        else:
            st.success(f"✅ **MISIÓN VIABLE:** Llegarías con {litros_finales} litros restantes.")
            st.write(f"Autonomía restante estimada: {porcentaje_final}% del tanque.")
            st.progress(porcentaje_final)

        # Mostrar capacidad vs actual de forma visual
        st.info(f"💡 Info de Tanque: {gasolina_inicial}L actuales / {TANQUE_MAX}L de capacidad máxima.")

# Esto es para que no falle al importar
if __name__ == "__main__":
    run_uyunitec_sim()
