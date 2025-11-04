
import streamlit as st
from dotenv import load_dotenv

st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
import os
#As Langchain team has been working aggresively on improving the tool, we can see a lot of changes happening every weeek,
#As a part of it, the below import has been depreciated
#from langchain.chat_models import ChatOpenAI

#New import from langchain, which replaces the above
from langchain_openai import ChatOpenAI
load_dotenv()  # Charge les variables du fichier .env
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
else:
    st.warning("OPENAI_API_KEY non trouvée. Crée un fichier .env avec OPENAI_API_KEY=<ta_cle> et relance l'application.")
# ...existing code..

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# From here down is all the StreamLit UI
st.header("Hey, je suis NIAPPA AI, demandez-moi n'importe quoi!")



if "sessionMessages" not in st.session_state:
     st.session_state.sessionMessages = [
        SystemMessage(content="You are a helpful assistant.")
    ]



def load_answer(question):

    st.session_state.sessionMessages.append(HumanMessage(content=question))

    assistant_answer  = chat.invoke(st.session_state.sessionMessages )

    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))

    return assistant_answer.content


def get_text():
    input_text = st.text_input("You: ")
    return input_text


#chat = ChatOpenAI(
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
    #)

# Try to build an explicit OpenAI client and pass it to ChatOpenAI.
# This avoids letting LangChain construct the client with kwargs that
# the installed OpenAI client may not accept (e.g. 'proxies').
try:
    from openai import OpenAI as OpenAIClient
    openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))
    # Do not pass the raw OpenAI client to ChatOpenAI because some
    # installed OpenAI client versions don't expose the methods
    # langchain expects (e.g. `with_raw_response.create`). Instead,
    # initialize ChatOpenAI via the API key so LangChain can construct
    # a compatible internal client.
    chat = ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
except Exception:
    # If anything goes wrong, fall back to the same API-key based init.
    chat = ChatOpenAI(
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )


user_input=get_text()
submit = st.button('Generate')  

if submit:
    
    response = load_answer(user_input)
    st.subheader("Answer:")

    st.write(response)

