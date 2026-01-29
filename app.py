1. **Arreglo del Quiz (Bug):** Ahora uso la "memoria de sesión" para congelar las preguntas. **Ya no cambiarán** cuando hagas clic en responder. Solo cambiarán si tú pides nuevas preguntas o (opcionalmente) podrías agregar lógica para cambiar al acertar, pero lo más estable es que se mantengan fijas hasta que tú decidas.
2. **Base de Datos Permanente:** El sistema ya usa SQLite (un archivo `.db`). Mientras no borres ese archivo de tu carpeta en GitHub/Codespaces, los usuarios y sus datos (peso, altura, historial) **se guardan para siempre**, incluso si cierras la pestaña.
3. **Regreso de Nutrición:** He añadido una pestaña exclusiva de "🍎 Nutrición" que lee automáticamente el **biotipo** que el usuario registró al crear la cuenta y le da la dieta exacta.

Copia y reemplaza **todo** tu código en `app.py` con este:

```python
import streamlit as st
import pandas as pd
import sqlite3
import hashlib
import random
from datetime import datetime

# --- 1. CONFIGURACIÓN Y BASE DE DATOS ---
st.set_page_config(page_title="NBA Pro Trainer VIP", layout="wide", page_icon="🏀")

def init_db():
    conn = sqlite3.connect('basket_app_final.db')
    c = conn.cursor()
    # Tabla de usuarios con datos físicos
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                 (username TEXT PRIMARY KEY, password TEXT, biotipo TEXT, altura REAL, peso REAL)''')
    # Tabla de progreso
    c.execute('''CREATE TABLE IF NOT EXISTS historial 
                 (username TEXT, fecha TEXT, jugador TEXT, ejercicio TEXT, estado TEXT)''')
    conn.commit()
    conn.close()

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def add_user(username, password, biotipo, altura, peso):
    conn = sqlite3.connect('basket_app_final.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO usuarios(username, password, biotipo, altura, peso) VALUES (?,?,?,?,?)', 
                  (username, make_hashes(password), biotipo, altura, peso))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect('basket_app_final.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE username =? AND password = ?', (username, make_hashes(password)))
    data = c.fetchall()
    conn.close()
    return data

def save_training(username, jugador, ejercicio, estado):
    conn = sqlite3.connect('basket_app_final.db')
    c = conn.cursor()
    c.execute('INSERT INTO historial(username, fecha, jugador, ejercicio, estado) VALUES (?,?,?,?,?)',
              (username, datetime.now().strftime("%Y-%m-%d %H:%M"), jugador, ejercicio, estado))
    conn.commit()
    conn.close()

def get_history(username):
    conn = sqlite3.connect('basket_app_final.db')
    df = pd.read_sql_query(f"SELECT fecha, jugador, ejercicio, estado FROM historial WHERE username='{username}' ORDER BY fecha DESC", conn)
    conn.close()
    return df

init_db()

# --- 2. DATOS COMPLETOS ---
DB_JUGADORES = {
    "Stephen Curry 👨‍🍳": {
        "team_colors": {"bg": "#1D428A", "txt": "#FFC72C", "sec": "#FFFFFF", "name": "Golden State Warriors"},
        "rutina": [
            {"nombre": "Form Shooting", "desc": "Tiro a una mano cerca del aro.", "reps": 50, "link": "https://www.youtube.com/watch?v=KzVvlXgGvXI"},
            {"nombre": "2-Ball Dribble", "desc": "Bote con dos balones.", "reps": 100, "link": "https://www.youtube.com/watch?v=baI4tMaoFfE"},
            {"nombre": "Tiro tras Pantalla", "desc": "Autopase, giro y tiro.", "reps": 20, "link": "https://www.youtube.com/watch?v=rK0N9Fj6dHM"},
            {"nombre": "Floater", "desc": "Bomba ante el defensor.", "reps": 15, "link": "https://www.youtube.com/watch?v=9_dgljdVd_A"},
            {"nombre": "Cardio Shooting", "desc": "Correr y tirar sin parar.", "reps": 10, "link": "https://www.youtube.com/watch?v=JDtOOY0GkHk"}
        ],
        "frases": ["El éxito no es un accidente.", "Puedo aceptar el fracaso, pero no no intentarlo."],
        "quiz": [
            {"p": "¿Récord de triples en una temporada?", "opc": ["380", "402", "395"], "r": "402"},
            {"p": "¿Puntos máximos en un partido?", "opc": ["62", "54", "70"], "r": "62"},
            {"p": "¿Universidad?", "opc": ["Duke", "Davidson", "UNC"], "r": "Davidson"},
            {"p": "¿Año de su primer MVP unánime?", "opc": ["2015", "2016", "2017"], "r": "2016"},
            {"p": "¿Nombre de su compañero 'Splash Brother'?", "opc": ["Draymond", "Klay", "Poole"], "r": "Klay"}
        ]
    },
    "LeBron James 👑": {
        "team_colors": {"bg": "#552583", "txt": "#FDB927", "sec": "#000000", "name": "L.A. Lakers"},
        "rutina": [
            {"nombre": "Bully Ball Drive", "desc": "Proteger balón con el cuerpo.", "reps": 15, "link": "https://www.youtube.com/watch?v=YpG7pXQhWzQ"},
            {"nombre": "Chase Down Block", "desc": "Sprint defensivo.", "reps": 8, "link": "https://www.youtube.com/watch?v=Zn3hMvfk_d4"},
            {"nombre": "Fadeaway Post", "desc": "Tiro hacia atrás en el poste.", "reps": 20, "link": "https://www.youtube.com/watch?v=O9dYqJukgYs"},
            {"nombre": "Pase Cruzado", "desc": "Pase fuerte a una mano.", "reps": 30, "link": "https://www.youtube.com/watch?v=u6tGkFDbOms"},
            {"nombre": "Core", "desc": "Plancha abdominal.", "reps": "60 seg", "link": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
        ],
        "frases": ["Nada se regala. Todo se gana.", "Busco ser el más grande."],
        "quiz": [
            {"p": "¿Año de draft?", "opc": ["2003", "2001", "2004"], "r": "2003"},
            {"p": "¿Equipo original?", "opc": ["Miami", "Cleveland", "Lakers"], "r": "Cleveland"},
            {"p": "¿Cuántos puntos para pasar a Kareem?", "opc": ["38,387", "40,000", "35,000"], "r": "38,387"},
            {"p": "¿Títulos con Miami Heat?", "opc": ["1", "2", "3"], "r": "2"},
            {"p": "¿Apodo?", "opc": ["The King", "The Goat", "Flash"], "r": "The King"}
        ]
    },
    "Michael Jordan 🐐": {
        "team_colors": {"bg": "#CE1141", "txt": "#000000", "sec": "#FFFFFF", "name": "Chicago Bulls"},
        "rutina": [
            {"nombre": "Triple Amenaza", "desc": "Posición de ataque básica.", "reps": 10, "link": "https://www.youtube.com/watch?v=ExmX8LTAhgw"},
            {"nombre": "Fadeaway", "desc": "El tiro clásico de MJ.", "reps": 25, "link": "https://www.youtube.com/watch?v=wL-5tqO_oJ0"},
            {"nombre": "Pivoteo", "desc": "Crear espacio con los pies.", "reps": 20, "link": "https://www.youtube.com/watch?v=ExmX8LTAhgw"},
            {"nombre": "Defensa", "desc": "Desplazamiento lateral.", "reps": 30, "link": "https://www.youtube.com/watch?v=F0pX-CaeIVo"},
            {"nombre": "Media Distancia", "desc": "1 bote y tiro.", "reps": 20, "link": "https://www.youtube.com/watch?v=wL-5tqO_oJ0"}
        ],
        "frases": ["He fallado una y otra vez, por eso triunfo.", "El talento gana partidos, el equipo campeonatos."],
        "quiz": [
            {"p": "¿Cuántos anillos tiene?", "opc": ["5", "6", "7"], "r": "6"},
            {"p": "¿Año de su retiro definitivo?", "opc": ["1998", "2003", "2001"], "r": "2003"},
            {"p": "¿Equipo contra el que hizo 'The Last Shot'?", "opc": ["Jazz", "Suns", "Lakers"], "r": "Jazz"},
            {"p": "¿Puntos en el 'Flu Game'?", "opc": ["38", "45", "50"], "r": "38"},
            {"p": "¿Dorsal al volver en el 95?", "opc": ["23", "45", "12"], "r": "45"}
        ]
    },
    "Kobe Bryant 🐍": {
        "team_colors": {"bg": "#FDB927", "txt": "#552583", "sec": "#FFFFFF", "name": "L.A. Lakers"},
        "rutina": [
            {"nombre": "Suicidios", "desc": "Sprints cancha completa.", "reps": 5, "link": "https://www.youtube.com/watch?v=Zn3hMvfk_d4"},
            {"nombre": "Shadow Shooting", "desc": "Visualización sin balón.", "reps": "10 min", "link": "https://www.youtube.com/watch?v=1Shs05N7Yys"},
            {"nombre": "Pump Fake", "desc": "Finta de tiro y paso.", "reps": 20, "link": "https://www.youtube.com/watch?v=wL-5tqO_oJ0"},
            {"nombre": "400 Tiros", "desc": "Anotar 400 antes de irse.", "reps": 1, "link": "https://www.youtube.com/watch?v=KzVvlXgGvXI"},
            {"nombre": "Defensa 1v1", "desc": "Postura defensiva baja.", "reps": 20, "link": "https://www.youtube.com/watch?v=F0pX-CaeIVo"}
        ],
        "frases": ["Mamba Mentality.", "Descansaré al final, no en el medio."],
        "quiz": [
            {"p": "¿Puntos contra Raptors?", "opc": ["81", "70", "100"], "r": "81"},
            {"p": "¿Draft original?", "opc": ["Hornets", "Lakers", "Sixers"], "r": "Hornets"},
            {"p": "¿Tiros libres con el Aquiles roto?", "opc": ["2", "0", "1"], "r": "2"},
            {"p": "¿Años en la NBA?", "opc": ["20", "18", "15"], "r": "20"},
            {"p": "¿Ganó Oscar?", "opc": ["Sí", "No"], "r": "Sí"}
        ]
    },
    "Kyrie Irving 👁️": {
        "team_colors": {"bg": "#00538C", "txt": "#B8C4CA", "sec": "#000000", "name": "Dallas Mavericks"},
        "rutina": [
            {"nombre": "Miken Drill", "desc": "Finalizaciones bajo aro.", "reps": 50, "link": "https://www.youtube.com/watch?v=2f35G4dF2pk"},
            {"nombre": "In & Out", "desc": "Amague de dribbling.", "reps": 30, "link": "https://www.youtube.com/watch?v=OpZDKZJbUfs"},
            {"nombre": "Jelly Layup", "desc": "Efecto al balón.", "reps": 20, "link": "https://www.youtube.com/watch?v=9_dgljdVd_A"},
            {"nombre": "Bote Sentado", "desc": "Control extremo.", "reps": 100, "link": "https://www.youtube.com/watch?v=baI4tMaoFfE"},
            {"nombre": "Shamgod", "desc": "Dribbling cruzado.", "reps": 15, "link": "https://www.youtube.com/watch?v=I6lUzm8nOVM"}
        ],
        "frases": ["Mantén tu tercer ojo abierto.", "El arte del dribbling."],
        "quiz": [
            {"p": "¿País de nacimiento?", "opc": ["Australia", "USA", "Canadá"], "r": "Australia"},
            {"p": "¿Tiro ganador 2016?", "opc": ["Triple", "Mate", "Tiro libre"], "r": "Triple"},
            {"p": "¿Personaje de cine?", "opc": ["Uncle Drew", "The Professor", "Bone Collector"], "r": "Uncle Drew"},
            {"p": "¿Universidad?", "opc": ["Duke", "Kentucky", "Kansas"], "r": "Duke"},
            {"p": "¿Campeonato mundial?", "opc": ["2014", "2010", "2019"], "r": "2014"}
        ]
    },
    "Carmelo Anthony 7️⃣": {
        "team_colors": {"bg": "#F58426", "txt": "#006BB6", "sec": "#FFFFFF", "name": "N.Y. Knicks"},
        "rutina": [
            {"nombre": "Jab Step", "desc": "Finta con el pie.", "reps": 30, "link": "https://www.youtube.com/watch?v=ExmX8LTAhgw"},
            {"nombre": "Catch & Shoot", "desc": "Recibir y tirar.", "reps": 20, "link": "https://www.youtube.com/watch?v=rK0N9Fj6dHM"},
            {"nombre": "Rebote Ofensivo", "desc": "Saltar y anotar.", "reps": 15, "link": "https://www.youtube.com/watch?v=O9dYqJukgYs"},
            {"nombre": "Poste Medio", "desc": "Tiro desde el codo.", "reps": 20, "link": "https://www.youtube.com/watch?v=wL-5tqO_oJ0"},
            {"nombre": "Resistencia Hombros", "desc": "Brazos arriba.", "reps": "3 min", "link": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
        ],
        "frases": ["Stay Melo.", "Nueva York me hizo duro."],
        "quiz": [
            {"p": "¿Oros Olímpicos?", "opc": ["3", "2", "1"], "r": "3"},
            {"p": "¿Universidad campeona?", "opc": ["Syracuse", "UCLA", "Texas"], "r": "Syracuse"},
            {"p": "¿Puntos en el Garden?", "opc": ["62", "60", "55"], "r": "62"},
            {"p": "¿Draft?", "opc": ["2003", "2004", "2002"], "r": "2003"},
            {"p": "¿Celebración?", "opc": ["3 a la cabeza", "Silencio", "Beso al aro"], "r": "3 a la cabeza"}
        ]
    },
    "Dwyane Wade ⚡": {
        "team_colors": {"bg": "#6F263D", "txt": "#FFB81C", "sec": "#000000", "name": "Cleveland Cavaliers"},
        "rutina": [
            {"nombre": "Eurostep", "desc": "Cambio de dirección.", "reps": 20, "link": "https://www.youtube.com/watch?v=1F4f_jCXuO8"},
            {"nombre": "Puerta Atrás", "desc": "Corte al aro.", "reps": 15, "link": "https://www.youtube.com/watch?v=YpG7pXQhWzQ"},
            {"nombre": "Pull-up Jumper", "desc": "Tiro tras bote.", "reps": 20, "link": "https://www.youtube.com/watch?v=wL-5tqO_oJ0"},
            {"nombre": "Tapón", "desc": "Timing de salto.", "reps": 10, "link": "https://www.youtube.com/watch?v=Zn3hMvfk_d4"},
            {"nombre": "Split P&R", "desc": "Pasar entre dos.", "reps": 15, "link": "https://www.youtube.com/watch?v=OpZDKZJbUfs"}
        ],
        "frases": ["Caete 7 veces, levántate 8.", "This is my house."],
        "quiz": [
            {"p": "¿Apodo?", "opc": ["Flash", "Wade County", "Ambos"], "r": "Ambos"},
            {"p": "¿Primer anillo?", "opc": ["2006", "2012", "2013"], "r": "2006"},
            {"p": "¿Récord tapones?", "opc": ["Guardia con más tapones", "Más tapones totales", "Ninguno"], "r": "Guardia con más tapones"},
            {"p": "¿Marca calzado?", "opc": ["Li-Ning", "Nike", "Adidas"], "r": "Li-Ning"},
            {"p": "¿Dorsal retiro?", "opc": ["3", "9", "6"], "r": "3"}
        ]
    },
    "Ja Morant ✈️": {
        "team_colors": {"bg": "#5D76A9", "txt": "#12173F", "sec": "#F5B112", "name": "Memphis Grizzlies"},
        "rutina": [
            {"nombre": "Depth Jumps", "desc": "Salto reactivo.", "reps": 10, "link": "https://www.youtube.com/watch?v=SvXXRJPtXX8"},
            {"nombre": "360 Layup", "desc": "Entrada con giro.", "reps": 10, "link": "https://www.youtube.com/watch?v=9_dgljdVd_A"},
            {"nombre": "Primer Paso", "desc": "Salida explosiva.", "reps": 20, "link": "https://www.youtube.com/watch?v=sqXw9dD2nOI"},
            {"nombre": "Flotadora", "desc": "Tiro suave.", "reps": 15, "link": "https://www.youtube.com/watch?v=9_dgljdVd_A"},
            {"nombre": "Dunk", "desc": "Intento de mate.", "reps": 10, "link": "https://www.youtube.com/watch?v=SvXXRJPtXX8"}
        ],
        "frases": ["Un perro siempre tiene hambre.", "Bienvenido al show."],
        "quiz": [
            {"p": "¿Universidad?", "opc": ["Murray State", "Duke", "Kentucky"], "r": "Murray State"},
            {"p": "¿Premio 2022?", "opc": ["MIP", "MVP", "ROTY"], "r": "MIP"},
            {"p": "¿Dorsal?", "opc": ["12", "10", "11"], "r": "12"},
            {"p": "¿Estilo?", "opc": ["Slasher", "Tirador", "Poste"], "r": "Slasher"},
            {"p": "¿Altura aprox?", "opc": ["1.88m", "1.95m", "2.00m"], "r": "1.88m"}
        ]
    },
    "Giannis Antetokounmpo 🦌": {
        "team_colors": {"bg": "#00471B", "txt": "#EEE1C6", "sec": "#000000", "name": "Milwaukee Bucks"},
        "rutina": [
            {"nombre": "Eurostep Largo", "desc": "Zancada gigante.", "reps": 20, "link": "https://www.youtube.com/watch?v=1F4f_jCXuO8"},
            {"nombre": "Spin Move", "desc": "Giro de poder.", "reps": 15, "link": "https://www.youtube.com/watch?v=YpG7pXQhWzQ"},
            {"nombre": "Transición", "desc": "Correr botando.", "reps": 10, "link": "https://www.youtube.com/watch?v=baI4tMaoFfE"},
            {"nombre": "Peso Muerto", "desc": "Fuerza espalda.", "reps": 12, "link": "https://www.youtube.com/watch?v=pSHjTRCQxIw"},
            {"nombre": "Ayuda Defensiva", "desc": "Saltar al tablero.", "reps": 15, "link": "https://www.youtube.com/watch?v=Zn3hMvfk_d4"}
        ],
        "frases": ["La humildad te mantiene hambriento.", "Nunca olvides tu origen."],
        "quiz": [
            {"p": "¿Nacionalidad?", "opc": ["Grecia", "Nigeria", "Ambas"], "r": "Ambas"},
            {"p": "¿Apodo?", "opc": ["Greek Freak", "Zeus", "Hercules"], "r": "Greek Freak"},
            {"p": "¿MVP y DPOY mismo año?", "opc": ["2020", "2019", "2021"], "r": "2020"},
            {"p": "¿Hermanos con anillo?", "opc": ["3", "2", "1"], "r": "3"},
            {"p": "¿Película?", "opc": ["Rise", "Hustle", "Space Jam"], "r": "Rise"}
        ]
    }
}

# --- 3. ESTILOS ---
def aplicar_estilo(jugador_nombre):
    colores = DB_JUGADORES[jugador_nombre]["team_colors"]
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{ background-color: {colores['bg']}; }}
        [data-testid="stSidebar"] * {{ color: {colores['sec']} !important; }}
        h1, h2, h3, h4 {{ color: {colores['bg']}; }}
        .stButton>button {{
            background-color: {colores['bg']};
            color: {colores['txt']};
            border: 2px solid {colores['sec']};
        }}
        .stProgress > div > div > div > div {{ background-color: {colores['bg']}; }}
        </style>
    """, unsafe_allow_html=True)
    return colores

# --- 4. LÓGICA DE LOGIN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

if not st.session_state.logged_in:
    st.title("🔐 NBA Trainer VIP - Acceso Seguro")
    st.caption("Tus datos se guardarán permanentemente en la base de datos.")
    
    t1, t2 = st.tabs(["Ingresar", "Crear Cuenta"])
    
    with t1:
        u = st.text_input("Usuario")
        p = st.text_input("Contraseña", type="password")
        if st.button("Entrar a la Cancha"):
            res = login_user(u, p)
            if res:
                st.session_state.logged_in = True
                # Guardamos TODOS los datos del usuario en sesión (Nombre, Pass, Biotipo, Altura, Peso)
                st.session_state.user_info = res[0] 
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Credenciales inválidas")
    
    with t2:
        nu = st.text_input("Nuevo Usuario")
        np = st.text_input("Nueva Contraseña", type="password")
        c1, c2 = st.columns(2)
        bio = c1.selectbox("Biotipo", ["Ectomorfo (Delgado)", "Mesomorfo (Atlético)", "Endomorfo (Robusto)"])
        alt = c2.number_input("Altura (cm)", 100, 250, 180)
        peso = c1.number_input("Peso (kg)", 40, 180, 75)
        if st.button("Registrarme"):
            if add_user(nu, np, bio, alt, peso):
                st.success("¡Registrado! Ahora ve a la pestaña Ingresar.")
            else:
                st.error("Usuario ya existe.")

else:
    # --- 5. APLICACIÓN PRINCIPAL ---
    user = st.session_state.username
    # Recuperamos datos del usuario (indice 2 es biotipo, 3 altura, 4 peso)
    u_biotipo = st.session_state.user_info[2]
    u_altura = st.session_state.user_info[3]
    u_peso = st.session_state.user_info[4]

    with st.sidebar:
        st.title(f"Perfil: {user}")
        st.write(f"📏 {u_altura} cm | ⚖️ {u_peso} kg")
        st.write(f"🧬 {u_biotipo}")
        
        if st.button("Cerrar Sesión"):
            st.session_state.logged_in = False
            st.rerun()
        st.divider()
        st.header("Selecciona Mentor")
        jugador_sel = st.radio("Leyendas:", list(DB_JUGADORES.keys()))

    colors = aplicar_estilo(jugador_sel)
    data = DB_JUGADORES[jugador_sel]

    st.title(f"Modo: {jugador_sel}")
    st.subheader(f"Estilo {data['team_colors']['name']}")

    # PESTAÑAS (Ahora con Nutrición)
    tabs = st.tabs(["🏋️ Rutina", "🧠 Quiz", "🍎 Nutrición", "📺 Videos", "🦁 Motivación", "📅 Historial"])

    # --- 1. RUTINA ---
    with tabs[0]:
        st.write("Completa el circuito:")
        for i, ej in enumerate(data['rutina']):
            with st.expander(f"{i+1}. {ej['nombre']} ({ej['reps']})"):
                st.write(f"**Técnica:** {ej['desc']}")
                st.markdown(f"[Ver Demo]({ej['link']})")
                if st.button(f"Completar {ej['nombre']}", key=f"btn_rut_{i}"):
                    save_training(user, jugador_sel, ej['nombre'], "Completado")
                    st.success("¡Registrado!")

    # --- 2. QUIZ (ARREGLADO: NO CAMBIA SOLO) ---
    with tabs[1]:
        st.header("Examen de Conocimiento")
        
        # LÓGICA DEL BUG: 
        # Guardamos las preguntas en 'session_state' para que NO cambien al hacer clic en botones
        if 'quiz_actual' not in st.session_state or st.session_state.quiz_jugador_actual != jugador_sel:
            # Si entramos por primera vez o cambiamos de jugador, generamos nuevas preguntas
            st.session_state.quiz_actual = random.sample(data['quiz'], 3)
            st.session_state.quiz_jugador_actual = jugador_sel
            st.session_state.quiz_resultados = {} # Limpiar respuestas anteriores

        # Botón para forzar nuevas preguntas
        if st.button("🔄 Generar Nuevas Preguntas"):
            st.session_state.quiz_actual = random.sample(data['quiz'], 3)
            st.session_state.quiz_resultados = {}
            st.rerun()

        st.divider()

        # Mostrar las preguntas congeladas
        for i, q in enumerate(st.session_state.quiz_actual):
            st.markdown(f"**P{i+1}: {q['p']}**")
            
            # Usamos clave única basada en la pregunta para que Streamlit sepa cuál es cuál
            key_radio = f"radio_{jugador_sel}_{i}"
            ans = st.radio("Opción:", q['opc'], key=key_radio)
            
            # Botón de verificar individual
            if st.button(f"Verificar P{i+1}", key=f"check_{jugador_sel}_{i}"):
                if ans == q['r']:
                    st.success("✅ ¡Correcto!")
                else:
                    st.error(f"❌ Incorrecto. La respuesta era: {q['r']}")

    # --- 3. NUTRICIÓN (NUEVO / RECUPERADO) ---
    with tabs[2]:
        st.header(f"Plan Nutricional para {u_biotipo}")
        
        # Calcular IMC
        imc = u_peso / ((u_altura/100)**2)
        st.metric("Tu IMC Actual", f"{imc:.2f}")

        if "Ectomorfo" in u_biotipo:
            st.info("""
            **🔥 Objetivo: Ganar Masa Muscular (Superávit)**
            * **Calorías:** Necesitas comer MÁS de lo que quemas.
            * **Comida Pre-Entreno:** Avena con plátano y mantequilla de maní (Carbos complejos).
            * **Comida Post-Entreno:** Batido de proteína + Arroz blanco y pollo (Carbos rápidos + Proteína).
            * **Tip:** Come cada 3 horas. No te saltes el desayuno nunca.
            """)
        elif "Mesomorfo" in u_biotipo:
            st.success("""
            **⚡ Objetivo: Mantenimiento y Explosividad**
            * **Calorías:** Dieta normativa (Equilibrio).
            * **Comida Pre-Entreno:** Fruta y yogurt griego.
            * **Comida Post-Entreno:** Pescado/Carne magra con batata (camote).
            * **Tip:** Hidratación es tu prioridad. Tienes facilidad genética, no la desperdicies con comida chatarra.
            """)
        else: # Endomorfo
            st.warning("""
            **🛡️ Objetivo: Definición y Fuerza (Control de Grasa)**
            * **Calorías:** Déficit ligero o mantenimiento estricto.
            * **Comida Pre-Entreno:** Manzana verde o frutos rojos (Bajo índice glucémico).
            * **Comida Post-Entreno:** Mucha verdura verde y pechuga de pollo/pavo.
            * **Tip:** Reduce los carbohidratos (pan, pasta) en la cena. Prioriza proteínas para saciarte.
            """)

    # --- 4. VIDEOS ---
    with tabs[3]:
        c1, c2 = st.columns(2)
        for i, ej in enumerate(data['rutina']):
            if i < 3:
                with c1: st.video(ej['link'])
            elif i < 5:
                with c2: st.video(ej['link'])

    # --- 5. MOTIVACIÓN ---
    with tabs[4]:
        st.header(f"Mentalidad {jugador_sel}")
        for f in data['frases']:
            st.markdown(f"### ❝ {f} ❞")

    # --- 6. HISTORIAL ---
    with tabs[5]:
        st.header(f"Progreso de {user}")
        df = get_history(user)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            st.write(f"**Total ejercicios:** {len(df)}")
        else:
            st.info("Sin registros aún.")
