import streamlit as st
from app.services.base_data_service import BaseDataService

def render():
    st.title("👤 User Service Check")
    user_id = BaseDataService.current_user_id()
    if user_id:
        st.success(f"Authenticated User ID: {user_id}")
    else:
        st.warning("No active session found.")