
import streamlit as st
from app.services.llm_service import LLMService

def render():

    st.title("⚙ Settings")

    provider = st.selectbox(
        "Provider",
        list(LLMService.AVAILABLE_MODELS.keys())
    )

    st.write("Selected:", provider)

    models = LLMService.AVAILABLE_MODELS.get(provider, [])

    if models:

        model = st.selectbox(
            "Model",
            models
        )

        st.write("Model:", model)

    st.slider(
        "Temperature",
        0.0,
        1.0,
        0.7
    )
