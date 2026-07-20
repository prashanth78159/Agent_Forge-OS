
import streamlit as st

from app.services.prompt_service import PromptService
from app.services.provider_service import ProviderService


prompt_service = PromptService()

provider_service = ProviderService()


def render(user):

    st.title("🧠 Prompt Studio")

    create_tab, library_tab, test_tab = st.tabs(
        [
            "Create",
            "Library",
            "Test Lab"
        ]
    )

    with create_tab:

        st.subheader("Create Prompt")

        name = st.text_input(
            "Name"
        )

        description = st.text_area(
            "Description"
        )

        category = st.selectbox(
            "Category",
            [
                "GENERAL",
                "RESEARCH",
                "CODING",
                "ANALYSIS"
            ]
        )

        prompt = st.text_area(
            "Prompt",
            height=300
        )

        if st.button(
            "Create Prompt"
        ):

            payload = {

                "user_id": user["id"],

                "name": name,

                "description": description,

                "category": category,

                "prompt": prompt,

                "status": "DRAFT",

                "version": 1
            }

            prompt_service.create_prompt(
                payload
            )

            st.success(
                "Prompt Created"
            )

    with library_tab:

        response = (
            prompt_service
            .list_prompts(
                user["id"]
            )
        )

        prompts = response.data or []

        for item in prompts:

            with st.expander(
                item["name"]
            ):

                st.write(item)

    with test_tab:

        st.subheader(
            "Prompt Test Lab"
        )

        provider = st.selectbox(
            "Provider",
            provider_service.get_providers()
        )

        model = st.selectbox(
            "Model",
            provider_service.get_models(
                provider
            )
        )

        test_prompt = st.text_area(
            "Test Prompt",
            height=250
        )

        if st.button(
            "Execute"
        ):

            st.info(
                f"Testing using {provider} / {model}"
            )
