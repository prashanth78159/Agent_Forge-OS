from app.services.admin_guard import AdminGuard
import streamlit as st
from app.config.database import db

def render():
    AdminGuard.require_admin()
    st.title("🛡️ Role Management")
    st.subheader("Manage User Roles")

    try:
        result = db.client.table("user_profiles").select("*").execute()
        users = result.data or []

        if not users:
            st.info("No users found.")
            return

        for user in users:
            with st.container():
                cols = st.columns([3, 2, 1])
                cols[0].write(f"**{user['email']}** ({user.get('full_name', 'N/A')})")
                
                current_role = user.get('role', 'Viewer')
                roles = ["Admin", "Manager", "Director", "Finance", "Viewer"]
                
                new_role = cols[1].selectbox(
                    "Role",
                    roles,
                    index=roles.index(current_role) if current_role in roles else 4,
                    key=f"role_sel_{user['id']}"
                )
                
                if cols[2].button("Update", key=f"btn_upd_{user['id']}"):
                    db.client.table("user_profiles")                        .update({"role": new_role})                        .eq("id", user['id'])                        .execute()
                    st.success(f"Updated {user['email']} to {new_role}")
                    st.rerun()
            st.divider()
            
    except Exception as e:
        st.error(f"Error: {e}")