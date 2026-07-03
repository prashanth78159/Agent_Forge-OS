
import streamlit as st

from app.services.settings_service import (
    SettingsService
)

def render():

    st.title("🔑 API Vault")

    providers = [

        ("Groq API Key", "groq_api_key"),
        ("OpenAI API Key", "openai_api_key"),
        ("Anthropic API Key", "anthropic_api_key"),
        ("Gemini API Key", "gemini_api_key"),
        ("DeepSeek API Key", "deepseek_api_key"),
        ("OpenRouter API Key", "openrouter_api_key")

    ]

    values = {}

    for label, key in providers:

        values[key] = st.text_input(
            label,
            value=SettingsService.get_setting(key) or "",
            type="password"
        )

    if st.button("💾 Save API Keys"):

        for _, key in providers:

            SettingsService.save_setting(
                key,
                values[key].strip()
            )

        st.success(
            "✅ API Keys Saved Successfully"
        )

    st.divider()

    st.subheader("Saved Providers")

    for label, key in providers:

        saved = SettingsService.get_setting(key)

        if saved:

            st.success(
                f"{label}: Configured"
            )

        else:

            st.warning(
                f"{label}: Not Configured"
            )
