import streamlit as st

def main():
    st.set_page_config(page_title="Coach de Basket Virtual", page_icon="🏀")

    # Título e introducción
    st.title("🏀 Tu Entrenador de Basket Personal")
    st.write("Completa tu perfil para recibir consejos personalizados sobre tu juego y nutrición.")

    st.markdown("---")

    # --- COLUMNA 1: DATOS DEL JUGADOR ---
    col1, col2 = st.columns(2)

    with col1:
        st.header("1. Tu Perfil")
        sexo = st.radio("Sexo:", ("Masculino", "Femenino"))
        nivel = st.selectbox("Nivel de experiencia:", ["Novato", "Intermedio", "Experto"])
        biotipo = st.selectbox("Biotipo Corporal:", 
                               ["Ectomorfo (Delgado, cuesta ganar peso)", 
                                "Mesomorfo (Atlético, gana músculo fácil)", 
                                "Endomorfo (Estructura ósea grande, gana grasa fácil)"])

    with col2:
        st.header("2. Medidas")
        altura = st.number_input("Altura (en cm):", min_value=100, max_value=250, value=180)
        peso = st.number_input("Peso (en kg):", min_value=30, max_value=200, value=75)

    st.markdown("---")

    # BOTÓN PARA GENERAR REPORTE
    if st.button("🏀 Generar Plan de Mejora"):
        
        # Lógica básica de IMC (Índice de Masa Corporal)
        altura_m = altura / 100
        imc = peso / (altura_m ** 2)
        
        st.success(f"¡Perfil analizado! Tu IMC es de {imc:.2f}")

        # --- CONSEJOS SEGÚN NIVEL ---
        st.subheader(f"📌 Consejos de Entrenamiento para nivel {nivel}")
        if nivel == "Novato":
            st.info("Concéntrate en los fundamentos: Dribbling con ambas manos, mecánica de tiro cerca del aro y pases básicos. No intentes triples lejanos todavía.")
        elif nivel == "Intermedio":
            st.info("Es hora de mejorar tu IQ de juego. Trabaja en lecturas de defensa, pick and roll y mejora tu resistencia cardiovascular para partidos completos.")
        else: # Experto
            st.info("Perfecciona los detalles. Trabaja en situaciones de juego específicas, velocidad de reacción y liderazgo en la cancha. El gimnasio es obligatorio.")

        # --- CONSEJOS DE NUTRICIÓN SEGÚN BIOTIPO ---
        st.subheader(f"🍎 Nutrición recomendada para {biotipo.split()[0]}")
        
        if "Ectomorfo" in biotipo:
            st.warning("**Objetivo: Ganar masa muscular.**\n\n"
                       "- Necesitas un superávit calórico.\n"
                       "- Come carbohidratos complejos (avena, arroz, pasta) antes de entrenar.\n"
                       "- No te saltes comidas. La proteína es clave para aguantar el contacto físico en la pintura.")
        elif "Mesomorfo" in biotipo:
            st.warning("**Objetivo: Mantener potencia y explosividad.**\n\n"
                       "- Tienes genética atlética, aprovéchala con dieta balanceada.\n"
                       "- Proteína moderada y grasas saludables (aguacate, nueces).\n"
                       "- Hidratación es tu clave para no perder rendimiento.")
        else: # Endomorfo
            st.warning("**Objetivo: Control de peso y agilidad.**\n\n"
                       "- Prioriza proteínas magras (pollo, pescado) y vegetales.\n"
                       "- Reduce carbohidratos simples y azúcares.\n"
                       "- Tu ventaja es la fuerza natural, úsala para postear, pero mantén la grasa baja para no perder velocidad.")

        st.caption("Nota: Estos son consejos generales generados por Python. Consulta a un médico para dietas estrictas.")

if __name__ == "__main__":
    main()
