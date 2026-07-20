
class PromptAuditRepository:

    def __init__(self, supabase):
        self.supabase = supabase

    def log(
        self,
        payload
    ):

        return (
            self.supabase
            .table("prompt_audit_log")
            .insert(payload)
            .execute()
        )
