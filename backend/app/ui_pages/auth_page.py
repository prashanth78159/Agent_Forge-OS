
import streamlit as st

from app.services.auth_service import (
    AuthService
)


def render():

    st.title(
        "🔐 Authentication"
    )

    login_tab, signup_tab = st.tabs(
        [
            "Login",
            "Sign Up"
        ]
    )

    with login_tab:

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

                # st.write("LOGIN RESULT:")
                # st.write(result)

                if result.user:

                    st.session_state[
                        "user"
                    ] = result.user

                    st.session_state[
                        "logged_in"
                    ] = True

                    st.success(
                        "Logged in successfully"
                    )
                    st.rerun()

                    # st.write(
                    #     result.user
                    # )

                else:

                    st.error(
                        "No user returned"
                    )

            except Exception as e:

                st.error(
                    str(e)
                )
                # st.write(result)

    with signup_tab:

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
                    "Check your email verification link."
                )

            except Exception as e:

                st.error(
                    str(e)
                )
