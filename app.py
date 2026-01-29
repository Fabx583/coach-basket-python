import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Coach Basket Pro", layout="wide", page_icon="🏀")

# --- BASE DE DATOS DE JUGADORES (SIMULADA) ---
DB_JUGADORES = {
    "Stephen Curry": {
        "estilo": "Tirador Élite & Movimiento sin balón",
        "video": "https://www.youtube.com/watch?v=rK0N9Fj6dHM",  # Ejemplo de tutorial de tiro
        "rutina": [
            "1. Calentamiento: 50 tiros libres seguidos.",
            "2. Dribbling: Bote con pelota de tenis en la otra mano.",
            "3. Tiros: 5 series de 10 triples desde 5 puntos diferentes.",
            "4. Condición: Sprints suicidas (línea a línea)."
        ],
        "quiz": {"p": "¿Qué es lo más importante en el tiro de Curry?", "r": ["Salto muy alto", "Mecánica rápida y fluida", "Tirar con dos manos"], "correcta": "Mecánica rápida y fluida"}
    },
    "LeBron James": {
        "estilo": "Potencia Física & IQ de Juego",
        "video": "https://www.youtube.com/watch?v=O9dYqJukgYs", # Ejemplo entrenamiento físico
        "rutina": [
            "1. Pesas: Sentadillas y Peso Muerto (Fuerza explosiva).",
            "2. Cancha: Entradas al aro con contacto (usar almohadillas).",
            "3. Pases: Práctica de pases a una mano cruzando la cancha.",
            "4. Core: Planchas y abdominales (15 min)."
        ],
        "quiz": {"p": "¿Cuál es la mayor virtud de LeBron?", "r": ["Solo tirar triples", "Su visión de juego y físico", "Driblar como base pequeño"], "correcta": "Su visión de juego y físico"}
    },
    "Kyrie Irving": {
        "estilo": "El mejor manejo de balón (Handles) & Finalización",
        "video": "https://www.youtube.com/watch?v=OpZDKZJbUfs", # Tutorial de dribbling
        "rutina": [
            "1. Miken Drill: Finalizaciones bajo el aro (ambas manos).",
            "2. Bolsas de plástico: Envuelve el balón para reducir el agarre.",
            "3. Conos: Zig-zag dribbling a máxima velocidad.",
            "4. 1vs1: Juega partidos cortos limitados a 3 botes."
        ],
        "quiz": {"p": "¿Cómo mantiene Kyrie el balón tan bajo?", "r": ["Flexionando rodillas y dedos abiertos", "Mirando el balón", "Usando guantes"], "correcta": "Flexionando rodillas y dedos abiertos"}
    }
}

# --- INICIALIZAR HISTORIAL (SESSION STATE) ---
if 'historial' not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["Fecha", "Jugador Objetivo", "Enfoque", "Estado"])

def main():
    st.title("🏀 NBA Player Trainer: Conviértete en Leyenda")
    
    # --- BARRA LATERAL ---
    with st.sidebar:
        st.header("👤 Tu Perfil")
        nombre = st.text_input("Tu Nombre", "Rookie")
        
        st.subheader("🎯 Tu Objetivo")
        jugador_fav = st.selectbox("¿A quién quieres parecerte?", list(DB_JUGADORES.keys()))
        
        st.write("---")
        st.info(f"Modo seleccionado: **Estilo {jugador_fav}**")

    # --- PESTAÑAS PRINCIPALES ---
    tab1, tab2, tab3 = st.tabs(["🏋️‍♂️ Entrenamiento", "🧠 Quiz de Conocimiento", "mei Historial de Evolución"])

    # PESTAÑA 1: ENTRENAMIENTO
    with tab1:
        st.header(f"Plan de Entrenamiento: Estilo {jugador_fav}")
        data = DB_JUGADORES[jugador_fav]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📹 Video Análisis")
            st.video(data["video"])
            st.caption("Mira este video para entender la mecánica.")

        with col2:
            st.subheader("📋 Tu Rutina de Hoy")
            st.write(f"Sigue estos pasos para ganar el estilo de {data['estilo']}:")
            for i, paso in enumerate(data["rutina"]):
                st.success(paso)
            
            st.warning("⚠️ Nota: Ajusta las cargas (peso/repeticiones) según tu nivel actual.")

            # Botón para registrar entrenamiento
            if st.button("✅ ¡Terminé mi entrenamiento de hoy!"):
                nueva_fila = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Jugador Objetivo": jugador_fav,
                    "Enfoque": data["estilo"],
                    "Estado": "Completado"
                }
                # Convertir el diccionario a DataFrame y concatenarlo
                nueva_fila_df = pd.DataFrame([nueva_fila])
                st.session_state.historial = pd.concat([st.session_state.historial, nueva_fila_df], ignore_index=True)
                st.toast("¡Entrenamiento registrado en tu historial!", icon="🔥")

    # PESTAÑA 2: QUIZ
    with tab2:
        st.header(f"¿Qué tanto sabes del juego de {jugador_fav}?")
        quiz_data = DB_JUGADORES[jugador_fav]["quiz"]
        
        respuesta = st.radio(quiz_data["p"], quiz_data["r"])
        
        if st.button("Comprobar Respuesta"):
            if respuesta == quiz_data["correcta"]:
                st.balloons()
                st.success("¡Correcto! Entiendes el juego.")
            else:
                st.error("Incorrecto. Vuelve a estudiar los videos.")

    # PESTAÑA 3: HISTORIAL
    with tab3:
        st.header(f"📊 Evolución de {nombre}")
        st.write("Aquí queda registrado tu progreso mientras mantengas esta sesión abierta.")
        
        if not st.session_state.historial.empty:
            st.dataframe(st.session_state.historial, use_container_width=True)
            
            entrenamientos = len(st.session_state.historial)
            st.metric("Entrenamientos Totales", entrenamientos)
            
            if entrenamientos > 2:
                st.success("¡Vas por buen camino! La constancia es clave.")
        else:
            st.info("Aún no has registrado entrenamientos hoy. Ve a la pestaña 'Entrenamiento' y completa uno.")

if __name__ == "__main__":
    main()
