import streamlit as st

# Título y Configuración
st.set_page_config(page_title="Coach de Basket Virtual", page_icon="🏀")

st.title("🏀 Tu Coach Personal de Baloncesto")
st.write("Bienvenido. Ingresa tus datos para generar un plan personalizado.")

# --- BARRA LATERAL (Datos del usuario) ---
st.sidebar.header("Tus Datos")

nivel = st.sidebar.selectbox(
    "Selecciona tu nivel de experiencia:",
    ("Novato", "Intermedio", "Experto")
)

sexo = st.sidebar.radio("Sexo:", ("Masculino", "Femenino"))

altura = st.sidebar.number_input("Altura (en cm):", min_value=100, max_value=230, value=175)
peso = st.sidebar.number_input("Peso (en kg):", min_value=30, max_value=150, value=70)

biotipo = st.sidebar.selectbox(
    "¿Cuál es tu biotipo corporal?",
    ("Ectomorfo (Delgado, cuesta ganar músculo)", 
     "Mesomorfo (Atlético, gana músculo fácil)", 
     "Endomorfo (Estructura ósea grande, tiende a acumular grasa)")
)

# --- LÓGICA Y RESULTADOS ---

st.header(f"Plan para jugador: {nivel}")

# 1. Cálculo de IMC (Índice de Masa Corporal)
imc = peso / ((altura/100) ** 2)
st.metric(label="Tu IMC Actual", value=f"{imc:.2f}")

# 2. Consejos de Nutrición según Biotipo
st.subheader("🥗 Estrategia Nutricional")

if "Ectomorfo" in biotipo:
    st.info("""
    **Tu biotipo es Ectomorfo:**
    * **Objetivo:** Ganar masa muscular y fuerza para no ser desplazado en la pintura.
    * **Nutrición:** Necesitas un superávit calórico. Come muchos carbohidratos complejos (arroz, pasta, avena).
    * **Tip:** Come cada 3 horas. No te saltes comidas.
    """)
elif "Mesomorfo" in biotipo:
    st.success("""
    **Tu biotipo es Mesomorfo:**
    * **Objetivo:** Mantener la potencia y mejorar la explosividad.
    * **Nutrición:** Dieta balanceada (40% carbohidratos, 30% proteínas, 30% grasas).
    * **Tip:** Tienes genética atlética, enfócate en la calidad de la comida para rendir los 40 minutos del partido.
    """)
elif "Endomorfo" in biotipo:
    st.warning("""
    **Tu biotipo es Endomorfo:**
    * **Objetivo:** Controlar el porcentaje de grasa manteniendo la fuerza para los choques.
    * **Nutrición:** Prioriza proteínas y vegetales. Reduce los carbohidratos simples (azúcar, harinas blancas).
    * **Tip:** Hidrátate bien. Tu ventaja es tu fuerza natural, úsala para ganar la posición bajo el aro.
    """)

# 3. Consejos de Entrenamiento según Nivel
st.subheader("🏀 Enfoque de Entrenamiento")

if nivel == "Novato":
    st.markdown("""
    * **Fundamentos:** Dedica el 80% del tiempo al bote (dribbling) y mecánica de tiro básica.
    * **Físico:** Mejora tu resistencia cardiovascular general.
    * **Mental:** Aprende las reglas básicas y posicionamiento en la cancha.
    """)
elif nivel == "Intermedio":
    st.markdown("""
    * **Táctica:** Aprende a leer la defensa (pick and roll, cortes a la canasta).
    * **Físico:** Introduce entrenamiento de pliometría (saltos) para mejorar tu vertical.
    * **Tiro:** Practica el tiro tras bote y situaciones de juego real.
    """)
else: # Experto
    st.markdown("""
    * **Perfeccionamiento:** Trabaja en la velocidad de reacción y toma de decisiones bajo presión.
    * **Especialización:** Perfecciona tu "movimiento firma" (signature move).
    * **Recuperación:** El descanso y la prevención de lesiones son tan importantes como el entreno.
    """)

# Botón extra
if st.button("¡Generar Rutina Diaria!"):
    st.write("✅ **Hoy:** 15 min calentamiento + 30 min técnica individual + 20 min físico.")
