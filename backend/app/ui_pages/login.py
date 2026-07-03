
import streamlit as st

def render():

    st.title(
        "🔐 Login"
    )

    email = st.text_input(
        "Email"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login"
    ):

        st.session_state[
            "user_email"
        ] = email

        st.success(
            "Login successful"
        )

        st.rerun()
