import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


if "endpoint" in st.session_state and "deployment" in st.session_state and "api_version" in st.session_state and "api_key":
    try:
        st.title("ChatGPT-like clone")

        # Set OpenAI API key from Streamlit secrets
        #client = AzureOpenAI(
        #    api_version=os.getenv("API_VERSION"),
        #    azure_endpoint=os.getenv("ENDPOINT"),
        #    api_key=os.getenv("OPEN_API_KEY"),
        #)

        client = AzureOpenAI(
            api_version=st.session_state["api_version"],
            azure_endpoint=st.session_state["endpoint"],
            api_key=st.session_state["api_key"],
        )

        # Set a default model
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = st.session_state["deployment"]

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Inserisci il tuo messaggio"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
    except:
        st.error("Autenticazione non riuscita")
else:
    st.write("Devi prima autenticarti")
