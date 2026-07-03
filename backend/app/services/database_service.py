
from supabase import create_client


class DatabaseService:

    def __init__(self, url, key):

        self.client = create_client(
            url,
            key
        )

    # ----------------------
    # HEALTH
    # ----------------------

    def health(self):

        try:

            self.client.table(
                "users"
            ).select("*").limit(1).execute()

            return True

        except Exception:

            return False

    # ----------------------
    # WORKFLOWS
    # ----------------------

    def save_workflow(
        self,
        name,
        workflow_json
    ):

        return (
            self.client
            .table("workflows")
            .insert(
                {
                    "name": name,
                    "workflow_json": workflow_json
                }
            )
            .execute()
        )

    def get_workflows(self):

        result = (
            self.client
            .table("workflows")
            .select("*")
            .execute()
        )

        return result.data

    # ----------------------
    # EXECUTIONS
    # ----------------------

    def save_execution(
        self,
        execution_id,
        status,
        final_output
    ):

        return (
            self.client
            .table("executions")
            .insert(
                {
                    "id": execution_id,
                    "status": status,
                    "final_output": final_output
                }
            )
            .execute()
        )

    def get_executions(self):

        result = (
            self.client
            .table("executions")
            .select("*")
            .execute()
        )

        return result.data

    # ----------------------
    # LOGS
    # ----------------------

    def save_log(
        self,
        execution_id,
        step,
        input_data,
        output_data
    ):

        return (
            self.client
            .table("execution_logs")
            .insert(
                {
                    "execution_id": execution_id,
                    "step": step,
                    "input_data": str(input_data),
                    "output_data": str(output_data)
                }
            )
            .execute()
        )

    def get_logs(
        self,
        execution_id
    ):

        result = (
            self.client
            .table("execution_logs")
            .select("*")
            .eq(
                "execution_id",
                execution_id
            )
            .execute()
        )

        return result.data

