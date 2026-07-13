import streamlit as st


class CurrentUserService:

    @staticmethod
    def get_user():

        return st.session_state.get(
            "user"
        )

    @staticmethod
    def get_user_id():

        user = (
            CurrentUserService
            .get_user()
        )

        if not user:
            return None

        return user['id']
