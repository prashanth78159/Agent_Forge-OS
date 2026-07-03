
from app.config.database import db


class ExecutionService:

    @staticmethod
    def save_execution(
        execution_id,
        status,
        final_output
    ):

        return db.save_execution(
            execution_id,
            status,
            final_output
        )

    @staticmethod
    def save_log(
        execution_id,
        step,
        input_data,
        output_data
    ):

        return db.save_log(
            execution_id,
            step,
            input_data,
            output_data
        )
