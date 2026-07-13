
import streamlit as st

from app.services.auth_service import (
    AuthService
)


def render():

    st.title(
        "🔒 Authentication"
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

                # Call the refactored AuthService.sign_in
                user = (
                    AuthService
                    .sign_in(
                        email,
                        password
                    )
                )

                if user: # Check if a user object was returned

                    st.session_state[
                        "user"
                    ] = user # Store the user object

                    st.session_state[
                        "logged_in"
                    ] = True

                    st.success(
                        "Logged in successfully"
                    )
                    st.rerun()

                else:

                    st.error(
                        "Authentication failed. Please check your credentials."
                    )

            except Exception as e:

                st.error(
                    str(e)
                )

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

                # Assuming AuthService.sign_up exists and handles user creation
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
