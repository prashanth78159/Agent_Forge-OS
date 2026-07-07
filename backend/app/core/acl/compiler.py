
from app.core.models.workflow import Workflow


class ACLCompiler:

    def compile(
        self,
        ast
    ):

        return Workflow(

            id=ast["name"],

            name=ast["name"],

            nodes=[],

            edges=[]

        )
