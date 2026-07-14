import streamlit as st
from app.config.database import db

def render():
    st.title("🛡️ Role Management")
    
    try:
        result = db.client.table("user_profiles").select("*").execute()
        users = result.data or []
        
        for user in users:
            cols = st.columns([3, 2, 1])
            cols[0].write(user["email"])
            new_role = cols[1].selectbox(
                "Role",
                ["Admin", "Manager", "Director", "Finance", "Viewer"],
                index=["Admin", "Manager", "Director", "Finance", "Viewer"].index(user.get("role", "Viewer")),
                key=f"role_{user['id']}"
            )
            if cols[2].button("Update", key=f"btn_{user['id']}"):
                db.client.table("user_profiles").update({"role": new_role}).eq("id", user["id"]).execute()
                st.success(f"Role updated for {user['email']}")
    except Exception as e:
        st.error(f"Error: {e}")