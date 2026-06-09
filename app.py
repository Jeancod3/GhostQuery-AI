import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# =========================
# CONFIGURACIÓN DE PÁGINA
# =========================
st.set_page_config(
    page_title="GhostQuery AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CARGAR API KEY
# =========================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# =========================
# SESSION STATE
# =========================
if "respuesta_actual" not in st.session_state:
    st.session_state.respuesta_actual = ""

if "tarea_actual" not in st.session_state:
    st.session_state.tarea_actual = ""

if "categoria_actual" not in st.session_state:
    st.session_state.categoria_actual = ""

if "modo_actual" not in st.session_state:
    st.session_state.modo_actual = ""

if "tarea_input" not in st.session_state:
    st.session_state.tarea_input = ""

if "ultima_categoria" not in st.session_state:
    st.session_state.ultima_categoria = ""

# =========================
# FUNCIONES AUXILIARES
# =========================
def extraer_seccion(texto, inicio, finales):
    try:
        indice_inicio = texto.find(inicio)

        if indice_inicio == -1:
            return ""

        indice_inicio += len(inicio)
        indices_finales = []

        for final in finales:
            indice_final = texto.find(final, indice_inicio)
            if indice_final != -1:
                indices_finales.append(indice_final)

        if indices_finales:
            indice_fin = min(indices_finales)
            return texto[indice_inicio:indice_fin].strip()

        return texto[indice_inicio:].strip()

    except Exception:
        return ""


def mostrar_resultado_en_tabs(contenido):
    analisis = extraer_seccion(
        contenido,
        "### 🎯 Análisis de la Tarea",
        [
            "### 🥇 IA Principal Recomendada",
            "### 🧠 Otras IAs Recomendadas",
            "### 🛠️ Skills / Conocimientos Necesarios",
            "### 🚀 Flujo de Trabajo Recomendado",
            "### ✍️ Prompt Listo para Usar",
            "### ✅ Recomendación Final"
        ]
    )

    ia_principal = extraer_seccion(
        contenido,
        "### 🥇 IA Principal Recomendada",
        [
            "### 🧠 Otras IAs Recomendadas",
            "### 🛠️ Skills / Conocimientos Necesarios",
            "### 🚀 Flujo de Trabajo Recomendado",
            "### ✍️ Prompt Listo para Usar",
            "### ✅ Recomendación Final"
        ]
    )

    otras_ias = extraer_seccion(
        contenido,
        "### 🧠 Otras IAs Recomendadas",
        [
            "### 🛠️ Skills / Conocimientos Necesarios",
            "### 🚀 Flujo de Trabajo Recomendado",
            "### ✍️ Prompt Listo para Usar",
            "### ✅ Recomendación Final"
        ]
    )

    skills = extraer_seccion(
        contenido,
        "### 🛠️ Skills / Conocimientos Necesarios",
        [
            "### 🚀 Flujo de Trabajo Recomendado",
            "### ✍️ Prompt Listo para Usar",
            "### ✅ Recomendación Final"
        ]
    )

    flujo = extraer_seccion(
        contenido,
        "### 🚀 Flujo de Trabajo Recomendado",
        [
            "### ✍️ Prompt Listo para Usar",
            "### ✅ Recomendación Final"
        ]
    )

    prompt = extraer_seccion(
        contenido,
        "### ✍️ Prompt Listo para Usar",
        [
            "### ✅ Recomendación Final"
        ]
    )

    final = extraer_seccion(
        contenido,
        "### ✅ Recomendación Final",
        []
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🎯 Resumen", "🤖 IAs", "🧠 Skills", "✍️ Prompt", "📄 Completo"]
    )

    with tab1:
        st.markdown("### 🎯 Análisis de la Tarea")
        st.markdown(analisis if analisis else "No se detectó el análisis.")

        if flujo:
            st.markdown("### 🚀 Flujo de Trabajo Recomendado")
            st.markdown(flujo)

        if final:
            st.markdown("### ✅ Recomendación Final")
            st.markdown(final)

    with tab2:
        st.markdown("### 🥇 IA Principal Recomendada")
        st.markdown(ia_principal if ia_principal else "No se detectó la IA principal.")

        st.markdown("### 🧠 Otras IAs Recomendadas")
        st.markdown(otras_ias if otras_ias else "No se detectaron otras IAs recomendadas.")

    with tab3:
        st.markdown("### 🛠️ Skills / Conocimientos Necesarios")
        st.markdown(skills if skills else "No se detectaron skills.")

    with tab4:
        st.markdown("### ✍️ Prompt Listo para Usar")
        st.markdown(prompt if prompt else "No se detectó el prompt.")

    with tab5:
        st.markdown(contenido)


def eliminar_chat_actual():
    st.session_state.respuesta_actual = ""
    st.session_state.tarea_actual = ""
    st.session_state.categoria_actual = ""
    st.session_state.modo_actual = ""


# =========================
# CSS
# =========================
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 10vh;
    }
    
    div[role="radiogroup"] label:has(input:checked) {
        background-color: rgba(255, 75, 75, 0.15) !important;
        border-bottom: 2px solid #FF4B4B !important;
        border-radius: 6px !important;
        padding-top: 5px !important;
        padding-bottom: 5px !important;
        padding-left: 10px !important;
        transition: all 0.3s ease-in-out !important;
    }

    div.stButton {
        display: inline-block !important;
    }

    div.stButton > button {
        background-color: #2b2d31 !important;
        color: #E8EAED !important;
        border-radius: 22px !important;
        border: 1px solid #444746 !important;
        padding: 8px 18px !important;
        min-height: 42px !important;
        width: auto !important;
        min-width: fit-content !important;
        white-space: nowrap !important;
        transition: all 0.3s ease !important;
        font-size: 0.98rem !important;
    }

    div.stButton > button:hover {
        background-color: #383a40 !important;
        border-color: #FF4B4B !important;
        color: #FFFFFF !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
        border: 1px solid #444746 !important;
        background-color: #161719 !important;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.3) !important;
    }

    pre {
        border-radius: 10px !important;
        border: 1px solid #333842 !important;
    }

    code {
        font-size: 0.95rem !important;
    }

    .modo-card {
        background: linear-gradient(135deg, rgba(255,75,75,0.14), rgba(255,255,255,0.04));
        border: 1px solid #444746;
        border-radius: 14px;
        padding: 14px;
        margin-top: 10px;
        font-size: 0.88rem;
        color: #E8EAED;
        box-shadow: 0px 4px 14px rgba(0,0,0,0.20);
    }

    .modo-card-title {
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 8px;
        font-size: 0.95rem;
    }

    .modo-item {
        margin: 6px 0;
        color: #C9CDD3;
        line-height: 1.35;
    }

    .modo-item b {
        color: #FFFFFF;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: visible !important;
        background: transparent !important;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# CATEGORÍAS AGRUPADAS
# =========================
categorias_por_grupo = {
    "💻 Tecnología y Código": [
        "✍️ Escribir mi propia tarea",
        "💻 Desarrollo Web Frontend",
        "⚙️ Desarrollo Backend y APIs",
        "📊 Análisis de Datos",
        "🤖 Agentes de IA y Chatbots",
        "🛠️ DevOps y Servidores",
        "🌐 Traducción de Software",
        "🛒 Creación de E-commerce"
    ],

    "🎨 Creatividad y Contenido": [
        "🎨 Diseño Gráfico y Arte",
        "🎬 Edición de Video y Guiones",
        "📝 Copywriting y Contenido",
        "🎵 Música y Sonido",
        "🏡 Arquitectura y 3D"
    ],

    "📈 Negocios y Marketing": [
        "🏔️ Negocios de Turismo",
        "📱 Marketing Digital y SEO",
        "📈 Trading y Finanzas",
        "🏢 Recursos Humanos"
    ],

    "🛡️ Seguridad y Legal": [
        "🛡️ Ciberseguridad (Blue Team)",
        "🗡️ Ciberseguridad (Red Team)",
        "⚖️ Asistencia Legal"
    ],

    "🏫 Educación y Gaming": [
        "🏫 Tutoría y Educación",
        "🎮 Optimización de Gaming"
    ]
}

categorias_codigo = [
    "💻 Desarrollo Web Frontend",
    "⚙️ Desarrollo Backend y APIs",
    "📊 Análisis de Datos",
    "🤖 Agentes de IA y Chatbots",
    "🛠️ DevOps y Servidores",
    "🛒 Creación de E-commerce"
]

# =========================
# PROMPTS PERSONALIZADOS
# =========================
prompts_categoria = {
    "💻 Desarrollo Web Frontend": (
        "Quiero crear una interfaz web moderna, responsiva y profesional. "
        "Necesito recomendaciones de IAs especializadas en programación frontend, diseño UI, HTML, CSS, JavaScript, React, Tailwind, componentes visuales y experiencia de usuario."
    ),

    "⚙️ Desarrollo Backend y APIs": (
        "Quiero desarrollar un backend con APIs seguras, escalables y bien estructuradas. "
        "Necesito recomendaciones de IAs especializadas en programación backend, endpoints, bases de datos, autenticación, lógica del servidor y arquitectura."
    ),

    "📊 Análisis de Datos": (
        "Tengo datos y quiero analizarlos usando herramientas modernas. "
        "Necesito recomendaciones de IAs para limpieza de datos, Python, notebooks, visualizaciones, interpretación de resultados y generación de reportes."
    ),

    "🛡️ Ciberseguridad (Blue Team)": (
        "Quiero proteger sistemas, detectar amenazas y mejorar la seguridad defensiva. "
        "Necesito saber qué IA usar para análisis de logs, hardening, monitoreo, detección de vulnerabilidades y respuesta a incidentes."
    ),

    "🗡️ Ciberseguridad (Red Team)": (
        "Quiero realizar evaluaciones de seguridad ética y autorizada. "
        "Necesito saber qué IA usar para planificación, análisis de vulnerabilidades, documentación técnica y reportes profesionales."
    ),

    "🤖 Agentes de IA y Chatbots": (
        "Quiero crear un chatbot o agente de IA que pueda responder usuarios, mantener contexto, usar herramientas y automatizar tareas. "
        "Necesito recomendaciones de IAs y frameworks para construirlo de forma profesional."
    ),

    "🏔️ Negocios de Turismo": (
        "Quiero mejorar o crear un negocio de turismo usando IA. "
        "Necesito herramientas para marketing, atención al cliente, rutas turísticas, contenido visual, automatización y estrategia comercial."
    ),

    "📱 Marketing Digital y SEO": (
        "Quiero crear una estrategia de marketing digital y SEO. "
        "Necesito saber qué IA usar para investigar palabras clave, analizar competencia, crear contenido, mejorar posicionamiento y generar campañas."
    ),

    "📝 Copywriting y Contenido": (
        "Quiero crear textos persuasivos y contenido profesional para redes, ventas o marca personal. "
        "Necesito herramientas de IA para ideas, estructura, tono, storytelling y optimización del mensaje."
    ),

    "🎨 Diseño Gráfico y Arte": (
        "Quiero crear diseños visuales profesionales usando IA. "
        "Necesito herramientas para imágenes, branding, logos, piezas gráficas, estilos visuales y prompts creativos."
    ),

    "🎬 Edición de Video y Guiones": (
        "Quiero crear o editar videos con ayuda de IA. "
        "Necesito herramientas para guiones, edición, generación de video, subtítulos, voz, música y estructura narrativa."
    ),

    "🎮 Optimización de Gaming": (
        "Quiero optimizar mi experiencia gaming, rendimiento, configuración, contenido o streaming. "
        "Necesito herramientas de IA para análisis técnico, recomendaciones, guiones, overlays o mejora de rendimiento."
    ),

    "📈 Trading y Finanzas": (
        "Quiero analizar información financiera, riesgos, tendencias o estrategias de inversión. "
        "Necesito herramientas de IA para investigación, análisis de datos, noticias, gráficos y toma de decisiones informada."
    ),

    "⚖️ Asistencia Legal": (
        "Quiero apoyo para entender, redactar o analizar documentos legales de forma general. "
        "Necesito herramientas de IA para resumir, estructurar, comparar cláusulas y preparar borradores no definitivos."
    ),

    "🏫 Tutoría y Educación": (
        "Quiero aprender o enseñar un tema usando IA. "
        "Necesito herramientas para explicar conceptos, crear ejercicios, resolver dudas, generar material educativo y practicar."
    ),

    "🏢 Recursos Humanos": (
        "Quiero mejorar procesos de recursos humanos usando IA. "
        "Necesito herramientas para CVs, entrevistas, perfiles de puesto, evaluación de candidatos y comunicación interna."
    ),

    "🛠️ DevOps y Servidores": (
        "Quiero administrar servidores, despliegues, automatización o infraestructura. "
        "Necesito herramientas de IA especializadas en scripts, Docker, CI/CD, monitoreo, cloud y solución de errores."
    ),

    "🌐 Traducción de Software": (
        "Quiero traducir una app, página web o software manteniendo contexto técnico y naturalidad. "
        "Necesito herramientas de IA para localización, revisión, consistencia y adaptación cultural."
    ),

    "🛒 Creación de E-commerce": (
        "Quiero crear o mejorar una tienda online. "
        "Necesito herramientas de IA para desarrollo web, productos, descripciones, diseño, automatización, marketing, atención al cliente y conversión."
    ),

    "🎵 Música y Sonido": (
        "Quiero crear música, efectos de sonido, voces o mejorar audio usando IA. "
        "Necesito herramientas para composición, mezcla, voz, narración y prompts musicales."
    ),

    "🏡 Arquitectura y 3D": (
        "Quiero crear diseños arquitectónicos, renders o modelos 3D con ayuda de IA. "
        "Necesito herramientas para planos, inspiración visual, modelado, renderizado y presentación."
    )
}

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.header("💡 Categorías Populares")
    st.markdown("Elige un grupo y luego una categoría:")

    grupo_categoria = st.selectbox(
        "Grupo:",
        options=list(categorias_por_grupo.keys())
    )

    opcion_rapida = st.radio(
        label="Categoría:",
        options=categorias_por_grupo[grupo_categoria],
        label_visibility="visible"
    )

    st.markdown("---")

    st.subheader("⚙️ Modo de respuesta")

    modo_respuesta = st.selectbox(
        "Selecciona el modo:",
        options=[
            "⚡ Rápido",
            "🧠 Experto",
            "🛠️ Técnico",
            "🎨 Creativo"
        ]
    )

    st.markdown("""
        <div class="modo-card">
            <div class="modo-card-title">✨ Guía rápida de modos</div>
            <div class="modo-item"><b>⚡ Rápido:</b> respuesta corta, clara y directa.</div>
            <div class="modo-item"><b>🧠 Experto:</b> análisis más completo y mejor explicado.</div>
            <div class="modo-item"><b>🛠️ Técnico:</b> más herramientas, pasos y detalles prácticos.</div>
            <div class="modo-item"><b>🎨 Creativo:</b> ideas más originales y prompts más potentes.</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align: center; color: #9AA0A6; font-size: 0.95rem; font-family: monospace; margin-top: 30px; padding-top: 15px; border-top: 1px solid #444746;">
            ⚡ by <b>Ghost Max</b>
        </div>
    """, unsafe_allow_html=True)

# =========================
# ACTUALIZAR TEXTO POR CATEGORÍA
# =========================
texto_por_defecto = ""

if opcion_rapida in categorias_codigo:
    texto_por_defecto = prompts_categoria.get(
        opcion_rapida,
        "Necesito recomendaciones de IAs especializadas en desarrollo, código o análisis de datos."
    )
elif opcion_rapida != "✍️ Escribir mi propia tarea":
    texto_por_defecto = prompts_categoria.get(
        opcion_rapida,
        "Necesito saber qué IA usar, qué habilidades requiero y un prompt avanzado para empezar."
    )
else:
    texto_por_defecto = ""

if st.session_state.ultima_categoria != opcion_rapida:
    st.session_state.tarea_input = texto_por_defecto
    st.session_state.ultima_categoria = opcion_rapida

# =========================
# INTERFAZ PRINCIPAL
# =========================
espacio_izq, col_centro, espacio_der = st.columns([1, 2.6, 1])

with col_centro:
    st.markdown(
        "<h1 style='text-align: center;'>🎯 AI Skill & Prompt Recommender</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align: center; font-size: 1.1rem; margin-bottom: 2rem;'>Descubre la herramienta ideal, las skills necesarias y el prompt perfecto para tu próxima tarea.</p>",
        unsafe_allow_html=True
    )

    st.text_area(
        "Ingresa tu problema:",
        key="tarea_input",
        height=120,
        label_visibility="collapsed",
        placeholder="Escribe la tarea o trabajo que necesitas realizar, y te generaré la IA recomendada, las habilidades necesarias y un prompt exacto listo para copiar y pegar."
    )

    espacio_btn_izq, col_generar, col_limpiar, espacio_btn_der = st.columns([1.0, 1.15, 0.9, 1.2])

    with col_generar:
        ejecutar = st.button("🚀 Generar recomendación")

    with col_limpiar:
        if st.button("🧹 Limpiar chat"):
            eliminar_chat_actual()
            st.toast("Chat actual eliminado.", icon="🧹")
            st.rerun()

    if ejecutar:
        tarea_usuario = st.session_state.tarea_input

        if not api_key:
            st.toast("⚠️ Falta la API Key en el archivo .env", icon="🚨")

        elif not tarea_usuario.strip():
            st.toast("⚠️ Escribe una tarea primero.", icon="⚠️")

        else:
            with st.spinner("🧠 Diseñando tu estrategia..."):
                try:
                    llm = ChatGoogleGenerativeAI(
                        model="gemini-2.5-flash",
                        google_api_key=api_key,
                        temperature=0.7
                    )

                    template = r'''
Actúa como un consultor experto en inteligencia artificial, herramientas IA actuales del 2026, desarrollo de software, análisis de datos, productividad digital y prompt engineering.

El usuario necesita ayuda con esta tarea:
{tarea}

Modo de respuesta seleccionado por el usuario:
{modo_respuesta}

INSTRUCCIONES SEGÚN EL MODO:
- Si el modo es "⚡ Rápido": responde de forma breve, clara y directa.
- Si el modo es "🧠 Experto": responde con más profundidad, mejor argumentación y recomendaciones más completas.
- Si el modo es "🛠️ Técnico": responde con enfoque técnico, herramientas específicas, flujo de trabajo detallado y skills más concretos.
- Si el modo es "🎨 Creativo": responde con ideas originales, enfoques distintos y prompts más creativos.

REGLAS IMPORTANTES:
- La respuesta debe adaptarse totalmente a la categoría o tarea del usuario.
- No repitas siempre las mismas IAs.
- No recomiendes modelos antiguos como GPT-4, Claude 3, Bard o versiones viejas de DeepSeek.
- Usa herramientas y modelos actuales del 2026.
- Recomienda varias opciones, no solo una.
- Explica siempre por qué recomiendas cada IA.
- Usa un lenguaje claro, directo y fácil de entender.
- No respondas de forma genérica.
- El prompt final debe estar adaptado exactamente a la tarea del usuario.

REGLAS PARA CATEGORÍAS TÉCNICAS, CÓDIGO Y DATOS:
Si la tarea está relacionada con programación, desarrollo web, frontend, backend, APIs, análisis de datos, Python, notebooks, visualización de datos, DevOps, servidores, agentes de IA, apps, automatización, bases de datos o e-commerce técnico:

- NO recomiendes Gemini 2.5 como IA principal.
- La IA principal recomendada debe ser preferentemente una de estas tres:
  1. Codex de ChatGPT
  2. Claude Code
  3. Cursor

- Elige la IA principal según el tipo de tarea:
  - Para escribir, corregir, ejecutar o estructurar código: recomienda Codex de ChatGPT.
  - Para trabajar con proyectos completos, revisar archivos, depurar y modificar código existente: recomienda Claude Code.
  - Para programar directamente dentro de un editor con autocompletado y contexto del proyecto: recomienda Cursor.
  - Para análisis de datos con código, Python, notebooks, limpieza de datos o visualizaciones: recomienda Codex de ChatGPT como principal.
  - Para frontend: recomienda Codex de ChatGPT, Claude Code o Cursor como principal.
  - Para backend y APIs: recomienda Claude Code, Codex de ChatGPT o Cursor como principal.
  - Para DevOps: recomienda Claude Code o Codex de ChatGPT como principal.
  - Para agentes de IA y chatbots: recomienda Codex de ChatGPT o Claude Code como principal.
  - Para e-commerce técnico: recomienda Codex de ChatGPT, Claude Code o Cursor como principal.

- Las demás herramientas deben ir en “Otras IAs Recomendadas”, no como primera opción:
  - Windsurf
  - Replit AI
  - DeepSeek V4 Pro
  - GitHub Copilot
  - Mistral
  - Perplexity AI
  - NotebookLM

- Explica por qué cada herramienta ayuda en esa tarea.
- Si la tarea es frontend, menciona diseño UI, componentes, responsive design y frameworks.
- Si la tarea es backend, menciona APIs, base de datos, autenticación, seguridad y arquitectura.
- Si la tarea es análisis de datos, menciona Python, limpieza de datos, visualización, interpretación y reportes.
- Si la tarea es DevOps, menciona Docker, CI/CD, servidores, cloud, monitoreo y automatización.

REGLAS PARA CATEGORÍAS QUE NO SON TÉCNICAS:
Si la tarea NO es de programación, desarrollo o análisis de datos, recomienda herramientas según el área:
- Investigación y búsqueda: Perplexity AI, ChatGPT con navegación, NotebookLM.
- Escritura y análisis largo: ChatGPT con GPT-5.5, Claude Opus 4.8.
- Diseño gráfico: Canva AI, Midjourney, DALL-E / ChatGPT Images, Adobe Firefly.
- Video: Runway, Pika, Kling.
- Voz y audio: ElevenLabs, Suno.
- Educación: ChatGPT, NotebookLM, Claude, Microsoft Copilot.
- Productividad empresarial: Microsoft Copilot, ChatGPT, Claude.
- Marketing y SEO: Perplexity AI, ChatGPT, Claude, Canva AI.
- Arquitectura y 3D: Midjourney, DALL-E, Firefly, herramientas de renderizado IA.
- Legal: ChatGPT, Claude, Perplexity, herramientas especializadas de revisión documental.
- Finanzas: Perplexity, ChatGPT, Claude, herramientas de análisis financiero.

CATÁLOGO DE IA ACTUALES QUE PUEDES USAR:

Para código, desarrollo y datos:
- Codex de ChatGPT: ideal para escribir, revisar, ejecutar, corregir y mejorar código. También sirve para Python, análisis de datos, notebooks y automatizaciones.
- Claude Code: ideal para trabajar sobre proyectos completos, leer archivos, modificar código, depurar errores y construir funcionalidades.
- Cursor: ideal para programar dentro del editor con asistencia contextual, autocompletado y comprensión del proyecto.
- Windsurf: ideal para desarrollo asistido por IA en proyectos completos.
- Replit AI: ideal para crear prototipos, apps rápidas y proyectos web desde el navegador.
- DeepSeek V4 Pro: ideal para razonamiento técnico, programación avanzada y análisis de código.
- GitHub Copilot: ideal para autocompletado, sugerencias de código y productividad diaria.
- Mistral: ideal para soluciones técnicas rápidas, modelos abiertos y automatización.

Para investigación y búsqueda:
- Perplexity AI: ideal para buscar información actualizada y comparar fuentes.
- ChatGPT con navegación: ideal para análisis, síntesis y explicación de información.
- NotebookLM: ideal para estudiar documentos, resumir fuentes y trabajar con material cargado por el usuario.

Para diseño y contenido visual:
- Canva AI: ideal para presentaciones, posts, branding y piezas gráficas.
- Midjourney: ideal para imágenes artísticas, conceptuales y estilos visuales avanzados.
- DALL-E / ChatGPT Images: ideal para generar imágenes desde instrucciones detalladas.
- Adobe Firefly: ideal para diseño comercial, edición visual y piezas profesionales.

Para video y audio:
- Runway: ideal para generación y edición de video con IA.
- Pika: ideal para videos cortos creativos.
- Kling: ideal para video generativo avanzado.
- ElevenLabs: ideal para voz, narración y doblaje.
- Suno: ideal para música generada con IA.

Para productividad, educación y empresa:
- ChatGPT con GPT-5.5: ideal para razonamiento, planificación, documentos, prompts complejos y productividad.
- Claude Opus 4.8: ideal para escritura larga, análisis profundo y trabajo con mucho contexto.
- Microsoft Copilot: ideal para Word, Excel, PowerPoint, Outlook y trabajo empresarial.
- Gemini: ideal para ecosistema Google, documentos, análisis multimodal y productividad con Google Workspace.

FORMATO DE RESPUESTA OBLIGATORIO:

### 🎯 Análisis de la Tarea
Explica brevemente qué quiere lograr el usuario y qué tipo de herramienta IA necesita.

### 🥇 IA Principal Recomendada
**IA:** Nombre de la IA más adecuada.  
**Por qué la recomiendo:** Explicación específica según la tarea.  
**Ideal para:** Uso principal.

### 🧠 Otras IAs Recomendadas
1. **IA 1** — Explica por qué sirve para esta tarea.
2. **IA 2** — Explica por qué sirve para esta tarea.
3. **IA 3** — Explica por qué sirve para esta tarea.
4. **IA 4** — Explica por qué sirve para esta tarea.
5. **IA 5** — Explica por qué sirve para esta tarea.

### 🛠️ Skills / Conocimientos Necesarios
Copia estos skills si quieres usarlos como guía:

```text
- Skill específico 1
- Skill específico 2
- Skill específico 3
- Skill específico 4
- Skill específico 5
```

### 🚀 Flujo de Trabajo Recomendado
1. Paso 1
2. Paso 2
3. Paso 3
4. Paso 4
5. Paso 5

### ✍️ Prompt Listo para Usar
Copia y pega el siguiente texto en la IA recomendada:

```text
Escribe aquí un prompt avanzado, específico, profesional y listo para copiar. Debe estar adaptado exactamente a la tarea del usuario.
```

### ✅ Recomendación Final
Explica en una frase qué IA usar primero y cuáles usar como complemento.
'''

                    prompt_estructurado = PromptTemplate(
                        template=template,
                        input_variables=["tarea", "modo_respuesta"]
                    )

                    cadena = prompt_estructurado | llm

                    respuesta = cadena.invoke({
                        "tarea": tarea_usuario,
                        "modo_respuesta": modo_respuesta
                    })

                    contenido = respuesta.content

                    st.session_state.respuesta_actual = contenido
                    st.session_state.tarea_actual = tarea_usuario
                    st.session_state.categoria_actual = opcion_rapida
                    st.session_state.modo_actual = modo_respuesta

                    st.toast("¡Recomendación generada con éxito!", icon="✨")
                    st.rerun()

                except Exception as e:
                    st.toast(
                        "Ocurrió un problema al generar la recomendación. Revisa tu API Key o conexión.",
                        icon="❌"
                    )
                    st.error(f"Detalle del error: {e}")

    if st.session_state.respuesta_actual:
        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(border=True):
            st.caption(
                f"Categoría: {st.session_state.categoria_actual} | Modo: {st.session_state.modo_actual}"
            )
            mostrar_resultado_en_tabs(st.session_state.respuesta_actual)