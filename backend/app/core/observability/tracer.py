
import time

class ExecutionTracer:

    def __init__(self):
        self.logs = []

    def log(
        self,
        step,
        input_data,
        output_data
    ):

        self.logs.append({
            "step": step,
            "input": input_data,
            "output": output_data,
            "timestamp": time.time()
        })

    def get_logs(self):
        return self.logs
