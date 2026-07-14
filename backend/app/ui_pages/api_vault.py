
import streamlit as st

from app.services.api_vault_service import (
    APIVaultService
)
from app.services.current_user_service import (
    BaseDataService
)


def render():

    st.title(
        "🔓 API Vault"
    )

    # Display current user info
    current_user = BaseDataService.get_user()
    if current_user:
        st.info(f"Currently logged in as: {current_user.get('email', 'N/A')}")
    else:
        st.warning("No user logged in. API Keys are user-specific.")

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

    if keys:
        for row in keys:
            st.info(
                row["provider"]
            )
    else:
        st.info("No API keys stored for this user.")
