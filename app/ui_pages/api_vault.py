
import streamlit as st
from app.services.llm_service import LLMService

def render():

    st.title(
        "🔑 API Vault"
    )

    providers = (
        LLMService
        .AVAILABLE_MODELS
        .keys()
    )

    for provider in providers:

        st.text_input(
            f"{provider} API Key",
            type="password"
        )
