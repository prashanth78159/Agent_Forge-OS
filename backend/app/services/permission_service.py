from app.config.database import db

class PermissionService:
    @staticmethod
    def has_permission(role, permission):
        result = (
            db.client
            .table("role_permissions")
            .select("*")
            .eq("role", role)
            .eq("permission", permission)
            .execute()
        )
        return bool(result.data)