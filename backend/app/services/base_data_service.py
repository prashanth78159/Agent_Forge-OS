
from app.services.current_user_service import (
    CurrentUserService
)

class BaseDataService:
    @staticmethod
    def current_user_id():
        """
        Retrieves the current authenticated user's ID for RLS compliance.
        """
        return (
            CurrentUserService
            .get_user_id()
        )
