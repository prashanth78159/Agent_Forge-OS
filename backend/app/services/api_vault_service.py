from app.config.database import db
from app.services.base_data_service import BaseDataService

class APIVaultService:
    @staticmethod
    def save_key(provider, api_key):
        uid = BaseDataService.current_user_id()
        if not uid: return None
        return db.client.table("user_api_keys").upsert({
            "user_id": uid,
            "provider": provider,
            "api_key": api_key
        }).execute()

    @staticmethod
    def get_keys():
        uid = BaseDataService.current_user_id()
        # CRITICAL FIX: Return empty list if no UUID is available to prevent 22P02 error
        if not uid or str(uid) == 'None':
            return []
        
        result = db.client.table("user_api_keys")\
            .select("*")\
            .eq("user_id", uid)\
            .execute()
        return result.data