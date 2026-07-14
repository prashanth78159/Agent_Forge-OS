
from app.services.current_user_service import (
    BaseDataService
)

class BaseDataService:
    @staticmethod
    def current_user_id():
        """
        Retrieves the current authenticated user's ID for RLS compliance.
        """
        return (
            BaseDataService
            .get_user_id()
        )
