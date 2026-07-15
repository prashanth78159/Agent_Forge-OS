from app.services.admin_guard import AdminGuard
import streamlit as st
from app.config.database import db
from app.services.base_data_service import BaseDataService

def render():
    AdminGuard.require_admin()
    st.title("👥 User Management")
    st.subheader("Users")
    
    result = (
        db.client
        .table("user_profiles")
        .select("*")
        .execute()
    )
    
    users = result.data or []
    if users:
        st.dataframe(
            users,
            width="stretch"
        )
    else:
        st.info("No users found.")

    st.divider()
    st.subheader("Create User")

    email = st.text_input("Email")
    full_name = st.text_input("Full Name")
    role = st.selectbox(
        "Role",
        ["Admin", "Manager", "Director", "Finance", "Viewer"]
    )

    if st.button("Create User"):
        try:
            # Fetch current user ID to satisfy RLS policies
            current_uid = BaseDataService.current_user_id()
            
            db.client.table(
                "user_profiles"
            ).insert(
                {
                    "email": email,
                    "full_name": full_name,
                    "role": role,
                    "user_id": current_uid
                }
            ).execute()
            st.success("User created successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")