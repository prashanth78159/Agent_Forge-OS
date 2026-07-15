import streamlit as st
from app.config.database import db
from app.services.admin_guard import AdminGuard

def render():
    AdminGuard.require_admin()
    st.title("🔐 Permission Management")
    
    rows = db.client.table("role_permissions").select("*").execute().data
    if rows:
        st.dataframe(rows, width="stretch")
    else:
        st.info("No permissions defined.")