
import streamlit as st

from app.services.api_vault_service import (
    APIVaultService
)


def render():

    st.title(
        "🔑 API Vault"
    )

    provider = st.selectbox(

        "Provider",

        [

            "OpenAI",
            "Groq",
            "Gemini",
            "Anthropic",
            "OpenRouter"

        ]
    )

    api_key = st.text_input(
        "API Key",
        type="password"
    )

    if st.button(
        "Save Key"
    ):

        APIVaultService.save_key(
            provider,
            api_key
        )

        st.success(
            "Key Saved"
        )

    st.subheader(
        "Stored Providers"
    )

    keys = (
        APIVaultService
        .get_keys()
    )

    for row in keys:

        st.info(
            row["provider"]
        )
