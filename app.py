import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# 1. Configuración de página
st.set_page_config(
    page_title="GhostQuery AI",
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar las variables de entorno (API Key)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# --- CSS PARA ESTILO MINIMALISTA Y ANIMACIONES ---
st.markdown("""
    <style>
    /* Bajar el contenido principal al centro */
    .main .block-container {
        padding-top: 10vh;
    }
    
    /* Ocultar el botón de contraer (<<) para que el panel NUNCA se cierre */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* TRUCO VISUAL: Resaltar la categoría seleccionada con color y subrayado */
    div[role="radiogroup"] label:has(input:checked) {
        background-color: rgba(255, 75, 75, 0.15) !important;
        border-bottom: 2px solid #FF4B4B !important;
        border-radius: 6px !important;
        padding-top: 5px !important;
        padding-bottom: 5px !important;
        padding-left: 10px !important;
        transition: all 0.3s ease-in-out !important;
    }

    /* TRUCO DEL FORMULARIO INVISIBLE */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background-color: transparent !important;
    }
    
    /* Estilo del botón (alineado a la izquierda) */
    div.stFormSubmitButton > button:first-child {
        background-color: #2b2d31 !important;
        color: #E8EAED !important;
        border-radius: 24px !important;
        border: 1px solid #444746 !important;
        padding: 8px 24px !important;
        transition: all 0.3s ease !important;
    }
    div.stFormSubmitButton > button:first-child:hover {
        background-color: #383a40 !important;
        border-color: #FF4B4B !important;
    }
    
    /* EFECTO GLOW PARA LA RESPUESTA DE LA IA */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
        border: 1px solid #444746 !important;
        background-color: #161719 !important;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3) !important;
    }

    /* Limpieza total de la interfaz */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- PANEL LATERAL CON CATEGORÍAS Y FIRMA ---
with st.sidebar:
    st.header("💡 Categorías Populares")
    st.markdown("¿No sabes por dónde empezar? Elige un área:")
    
    opcion_rapida = st.radio(
        label="Opciones:",
        label_visibility="collapsed",
        options=[
            "✍️ Escribir mi propia tarea", 
            "💻 Desarrollo Web Frontend",
            "⚙️ Desarrollo Backend y APIs",
            "📊 Análisis de Datos",
            "🛡️ Ciberseguridad (Blue Team)",
            "🗡️ Ciberseguridad (Red Team)",
            "🤖 Agentes de IA y Chatbots",
            "🏔️ Negocios de Turismo",
            "📱 Marketing Digital y SEO",
            "📝 Copywriting y Contenido",
            "🎨 Diseño Gráfico y Arte",
            "🎬 Edición de Video y Guiones",
            "🎮 Optimización de Gaming",
            "📈 Trading y Finanzas",
            "⚖️ Asistencia Legal",
            "🏫 Tutoría y Educación",
            "🏢 Recursos Humanos",
            "🛠️ DevOps y Servidores",
            "🌐 Traducción de Software",
            "🛒 Creación de E-commerce",
            "🎵 Música y Sonido",
            "🏡 Arquitectura y 3D"
        ]
    )

    # --- FIRMA DEL DESARROLLADOR (AHORA DENTRO DEL PANEL) ---
    st.markdown("""
        <div style="text-align: center; color: #9AA0A6; font-size: 0.95rem; font-family: monospace; margin-top: 30px; padding-top: 15px; border-top: 1px solid #444746;">
            ⚡ by <b>Ghost Max</b>
        </div>
    """, unsafe_allow_html=True)

# --- INTERFAZ PRINCIPAL ---

espacio_izq, col_centro, espacio_der = st.columns([1, 2.5, 1])

with col_centro:
    st.markdown("<h1 style='text-align: center;'>🎯 AI Skill & Prompt Recommender</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem; margin-bottom: 2rem;'>Descubre la herramienta ideal y el prompt perfecto para tu próxima tarea.</p>", unsafe_allow_html=True)

    # Autocompletado inteligente
    texto_por_defecto = ""
    if opcion_rapida != "✍️ Escribir mi propia tarea":
        tema = opcion_rapida[2:].strip()
        texto_por_defecto = f"Tengo un proyecto de {tema.lower()} y necesito saber qué IA específica usar, qué habilidades requiero y un prompt avanzado para empezar a trabajar."

    # --- FORMULARIO CON CTRL+ENTER ---
    with st.form(key="buscador_ia", clear_on_submit=False):
        tarea_usuario = st.text_area(
            "Ingresa tu problema:", 
            value=texto_por_defecto, 
            height=120,
            label_visibility="collapsed",
            placeholder="Escribe la tarea o trabajo que necesitas realizar, y te generaré la IA recomendada, las habilidades necesarias y un Prompt exacto listo para copiar y pegar."
        )
        
        # Botón alineado a la izquierda naturalmente
        ejecutar = st.form_submit_button("🚀 Generar Estrategia de IA")

    # --- LÓGICA DE PROCESAMIENTO (Con Toasts modernos) ---
    if ejecutar:
        if not api_key:
            st.toast("⚠️ Falta la API Key en el archivo .env", icon="🚨")
        elif not tarea_usuario.strip():
            st.toast("⚠️ Escribe una tarea primero.", icon="⚠️")
        else:
            with st.spinner("🧠 Diseñando tu estrategia..."):
                try:
                    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

                    template = """
                    Actúa como un experto de clase mundial en Prompt Engineering. 
                    El usuario necesita ayuda con esta tarea: '{tarea}'

                    Responde ESTRICTAMENTE con este formato visual:

                    ### 🤖 IA Recomendada
                    [Indica la mejor IA para esto y una breve razón]

                    ### 🧠 Skills / Conocimientos Necesarios
                    * [Skill 1]
                    * [Skill 2]
                    * [Skill 3]

                    ### ✍️ Prompt Listo para Usar
                    Copia y pega el siguiente texto en la IA recomendada:
                    ```text
                    [Escribe aquí el prompt altamente detallado y profesional]
                    ```
                    """
                    
                    prompt_estructurado = PromptTemplate(template=template, input_variables=["tarea"])
                    cadena = prompt_estructurado | llm
                    respuesta = cadena.invoke({"tarea": tarea_usuario})
                    
                    # Notificación moderna flotante
                    st.toast("¡Estrategia generada con éxito!", icon="✨")
                    
                    # Resultado mostrado dentro del contenedor con nuevo diseño Glow
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.container(border=True):
                        st.markdown(respuesta.content)
                    
                except Exception as e:
                    st.toast(f"Error de conexión: {e}", icon="❌")