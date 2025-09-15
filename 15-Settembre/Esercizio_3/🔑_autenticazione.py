import streamlit as st

# Create a placeholder for the login form
placeholder = st.empty()

# Insert the login form into the placeholder
with placeholder.form("login_form"):
    st.markdown("### Login")
    endpoint = st.text_input("Endpoint")
    model = st.text_input("Deployment")
    api_version = st.text_input("Api Verson")
    api_key = st.text_input("Api Key", type="password")
    submit = st.form_submit_button("Login")

# Validate credentials
if submit:
    if not endpoint or not model or not api_version or not api_key:
        st.error("Tutti i campi sono obbligatori!")
    else:
        st.session_state["endpoint"] = endpoint
        st.session_state["deployment"] = model
        st.session_state["api_version"] = api_version
        st.session_state["api_key"] = api_key