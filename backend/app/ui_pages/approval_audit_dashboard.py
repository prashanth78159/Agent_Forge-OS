import streamlit as st
import pandas as pd
from app.config.database import db

def render():
    st.title("📜 Approval Auditing")
    st.subheader("Approval History & Logs")

    try:
        # Fetch data from workflow_approvals join with user_profiles if needed
        result = db.client.table("workflow_approvals")            .select("id, execution_id, node_id, status, created_at, approver_group, approval_comments")            .order("created_at", desc=True)            .execute()
        
        audit_data = result.data or []

        if audit_data:
            df = pd.DataFrame(audit_data)
            st.dataframe(df, width="stretch")
            
            # Summary Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Decisions", len(df))
            c2.metric("Approved", len(df[df['status'] == 'APPROVED']))
            c3.metric("Rejected", len(df[df['status'] == 'REJECTED']))
        else:
            st.info("No approval audit records found.")
            
    except Exception as e:
        st.error(f"Error loading audit logs: {e}")