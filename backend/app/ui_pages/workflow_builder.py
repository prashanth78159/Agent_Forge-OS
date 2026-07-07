
import streamlit as st

from app.core.acl.lexer import tokenize
from app.core.acl.parser import Parser
from app.core.acl.compiler import ACLCompiler

from app.services.workflow_service import (
    WorkflowService
)


def render():

    st.title(
        "🏗 Workflow Builder"
    )

    acl_code = st.text_area(

        "ACL Code",

        height=300,

        value="""
agent demo {

step1: llm("Explain AI")
step2: tool("print","done")

step1 -> step2

}
"""

    )

    workflow_name = st.text_input(

        "Workflow Name",

        value="demo"

    )

    if st.button(
        "Compile Workflow"
    ):

        try:

            tokens = tokenize(
                acl_code
            )

            parser = Parser(
                tokens
            )

            ast = parser.parse()

            compiler = ACLCompiler()

            workflow = compiler.compile(
                ast
            )

            workflow_json = {

                "nodes": [
                    {
                        "id": node["id"]
                    }
                    for node in workflow.nodes
                ],

                "edges": workflow.edges

            }

            WorkflowService.save_workflow(

                workflow_name,

                workflow_json

            )

            st.success(
                "Workflow Saved To Database"
            )

            st.write(
                workflow
            )

        except Exception as e:

            st.error(
                str(e)
            )
