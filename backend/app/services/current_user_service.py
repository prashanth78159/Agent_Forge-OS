from app.config.database import db
import streamlit as st

class CurrentUserService:
    @staticmethod
    def get_user():
        # Check session state first for speed and reliability in Streamlit
        if 'user' in st.session_state and st.session_state.user:
            return st.session_state.user
        
        try:
            response = db.client.auth.get_user()
            if response and response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email
                }
        except Exception:
            return None
        return None

    @staticmethod
    def get_user_id():
        user = CurrentUserService.get_user()
        if not user or not user.get('id'):
            return None
        return user['id']