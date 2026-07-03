
import streamlit as st

from app.services.llm_service import (
    LLMService
)

from app.services.settings_service import (
    SettingsService
)

def render():

    st.title("⚙ Settings")

    saved_provider = (
        SettingsService.get_setting(
            "provider"
        )
    )

    provider_options = list(
        LLMService.AVAILABLE_MODELS.keys()
    )

    default_provider = (
        provider_options.index(saved_provider)
        if saved_provider in provider_options
        else 0
    )

    provider = st.selectbox(
        "Provider",
        provider_options,
        index=default_provider
    )

    models = (
        LLMService
        .AVAILABLE_MODELS.get(
            provider,
            []
        )
    )

    saved_model = (
        SettingsService.get_setting(
            "model"
        )
    )

    default_model = (
        models.index(saved_model)
        if saved_model in models
        else 0
    )

    model = st.selectbox(
        "Model",
        models,
        index=default_model
    )

    if st.button(
        "💾 Save Settings"
    ):

        SettingsService.save_setting(
            "provider",
            provider
        )

        SettingsService.save_setting(
            "model",
            model
        )

        st.success(
            "Settings saved"
        )
