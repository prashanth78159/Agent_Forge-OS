from app.services.current_user_service import CurrentUserService

class BaseDataService:
    @staticmethod
    def current_user_id():
        return CurrentUserService.get_user_id()

    @staticmethod
    def get_user_id():
        return CurrentUserService.get_user_id()