import streamlit as st
from app.config.database import db

def render():
    st.title("📜 Approval Audit Dashboard")
    
    try:
        result = (
            db.client
            .table("workflow_approvals")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        rows = result.data or []
        
        if rows:
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("No approval records found.")
    except Exception as e:
        st.error(f"Error fetching audit records: {e}")