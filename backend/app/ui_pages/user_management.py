import streamlit as st
import uuid
from app.services.user_service import UserService
from app.services.rbac_service import RBACService
from app.config.database import db

def render():
    st.title("👤 User Management")

    if not RBACService.has_role("admin"):
        st.error("Access Denied: Admin privileges required.")
        return

    tab1, tab2 = st.tabs(["User Directory", "Create New User"])

    with tab1:
        st.subheader("System Users")
        try:
            # Fetch users from the public.user_profiles table
            result = db.client.table("user_profiles").select("*").execute()
            users = result.data or []
            if users:
                st.dataframe(users, use_container_width=True)
            else:
                st.info("No users found in system directory.")
        except Exception as e:
            st.error(f"Error loading directory: {e}")

    with tab2:
        st.subheader("Provision Enterprise User")
        with st.form("create_user_form"):
            new_email = st.text_input("Email")
            new_full_name = st.text_input("Full Name")
            new_pass = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["Admin", "Manager", "Director", "Finance", "Viewer"], index=4)

            if st.form_submit_button("Create User"):
                if new_email and new_pass and new_full_name:
                    try:
                        # 1. Generate a manual UUID to satisfy the NOT NULL constraint on 'id'
                        manual_user_id = str(uuid.uuid4())
                        
                        # 2. Insert into the database first to ensure constraints are met
                        db.client.table("user_profiles").insert({
                            "id": manual_user_id,
                            "email": new_email,
                            "full_name": new_full_name,
                            "role": new_role
                        }).execute()

                        # 3. Provision the user in Supabase Auth (requires service_role permissions in UserService)
                        UserService.create_user(new_email, new_pass, roles=[new_role.lower()])
                        
                        st.success(f"User created successfully: {new_email}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to create user: {e}")
                else:
                    st.error("All fields (Email, Full Name, Password) are required.")