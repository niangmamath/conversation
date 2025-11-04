
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(
    page_title="NIAPPA AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

import os
from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# Load environment variables
load_dotenv()  # Charge les variables du fichier .env
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    st.warning("OPENAI_API_KEY non trouvée. Crée un fichier .env avec OPENAI_API_KEY=<ta_cle> et relance l'application.")

st.markdown("""
<style>
  .chat-container { max-width: 900px; margin: 0 auto; }
  .msg { padding: 12px 16px; border-radius: 16px; margin: 8px 0; display: inline-block; max-width: 78%; }
  .human { background: #E6F0FF; color: #03396c; align-self: flex-end; }
  .assistant { background: #F1F3F4; color: #111827; }
  .system { font-size: 0.8rem; color: #6b7280; margin-bottom: 12px; }
  .row { display:flex; flex-direction: row; gap:8px; }
  .row.reverse { flex-direction: row-reverse; }
  .meta { font-size:0.8rem; color:#6b7280; margin-bottom:6px; }
  .header { display:flex; align-items:center; gap:12px; }
  .brand { font-weight:700; font-size:1.2rem; }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div class="header">
      <div class="brand">NIAPPA AI — assistant conversationnel</div>
      <div class="meta">Posez une question — réponse rapide basée sur LangChain + OpenAI</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.sidebar.title("Paramètres")
    if api_key:
        st.sidebar.success("OPENAI_API_KEY configurée")
    else:
        st.sidebar.warning("OPENAI_API_KEY manquante — ajoutez-la dans .env ou dans les secrets Streamlit")
    if st.sidebar.button("Réinitialiser la conversation"):
        st.session_state.sessionMessages = [SystemMessage(content="You are a helpful assistant.")]

# Initialize the chat model
try:
    chat = ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
except Exception as e:
    st.error(f"Erreur d'initialisation du modèle: {str(e)}")
    chat = None

if "sessionMessages" not in st.session_state:
    st.session_state.sessionMessages = [SystemMessage(content="You are a helpful assistant.")]


def load_answer(question):
    """Append the human question, call the model, store the assistant reply and return text."""
    if chat is None:
        st.error("Le modèle n'est pas initialisé. Vérifiez votre clé API.")
        return "Erreur : Modèle non disponible"

    st.session_state.sessionMessages.append(HumanMessage(content=question))

    try:
        assistant_answer = chat.invoke(st.session_state.sessionMessages)

    # assistant_answer may be a LangChain Generation result
        reply_text = getattr(assistant_answer, "content", None)
        if reply_text is None:
            # support the object returned earlier where .content exists on the returned generation
            try:
                reply_text = assistant_answer.generations[0][0].text
            except Exception:
                reply_text = str(assistant_answer)

        st.session_state.sessionMessages.append(AIMessage(content=reply_text))
        return reply_text
    except Exception as e:
        error_message = f"Erreur lors de la génération de la réponse : {str(e)}"
        st.error(error_message)
        return error_message


def render_messages():
    """Render the conversation from session state using simple HTML bubbles."""
    html = ""
    for msg in st.session_state.sessionMessages:
        if isinstance(msg, SystemMessage):
            html += f"<div class='system'>{msg.content}</div>"
            continue
        role = 'human' if isinstance(msg, HumanMessage) else 'assistant'
        row_class = 'row reverse' if role == 'human' else 'row'
        avatar = '🧑' if role == 'human' else '🤖'
        html += (
            f"<div class='{row_class}'><div class='msg {role}'><div><strong>{avatar}</strong></div>"
            f"<div style='display:inline-block; margin-left:8px'>{msg.content}</div></div></div>"
        )
    st.markdown(f"<div class='chat-container'>{html}</div>", unsafe_allow_html=True)


with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input("Vous:")
    submit = st.form_submit_button("Envoyer")

if submit and user_input:
    with st.spinner("Génération en cours…"):
        response = load_answer(user_input)

    # Render messages after update
    render_messages()
else:
    render_messages()

# Initialize the chat model
try:
    chat = ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
except Exception as e:
    st.error(f"Erreur d'initialisation du modèle: {str(e)}")

