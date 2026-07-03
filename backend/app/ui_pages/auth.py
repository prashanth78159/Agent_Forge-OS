
import streamlit as st

from app.services.auth_service import (
    AuthService
)


def render():

    st.title(
        "🔐 Authentication"
    )

    tab1, tab2 = st.tabs(
        [
            "Login",
            "Sign Up"
        ]
    )

    with tab1:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login"
        ):

            try:

                result = (
                    AuthService
                    .sign_in(
                        email,
                        password
                    )
                )

                st.session_state[
                    "user"
                ] = result.user

                st.session_state[
                    "logged_in"
                ] = True

                st.success(
                    "Login Successful"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    str(e)
                )

    with tab2:

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        if st.button(
            "Sign Up"
        ):

            try:

                AuthService.sign_up(
                    email,
                    password
                )

                st.success(
                    "Check your email for verification."
                )

            except Exception as e:

                st.error(
                    str(e)
                )
