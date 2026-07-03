
import streamlit as st

from app.core.acl.lexer import tokenize
from app.core.acl.parser import Parser
from app.core.acl.compiler import ACLCompiler

def render():

    st.title("🏗 Workflow Builder")

    acl_code = st.text_area(
        "ACL Code",
        height=300,
        value='''
agent demo {

step1: llm("Explain AI")
step2: tool("print","done")

step1 -> step2

}
'''
    )

    workflow_name = st.text_input(
        "Workflow Name",
        value="demo"
    )

    if st.button("Compile Workflow"):

        try:

            tokens = tokenize(acl_code)

            parser = Parser(tokens)

            ast = parser.parse()

            compiler = ACLCompiler()

            workflow = compiler.compile(ast)

            st.session_state                 .stored_workflows[
                    workflow_name
                ] = workflow

            st.success(
                "Workflow Saved"
            )

            st.json(
                workflow.model_dump()
            )

        except Exception as e:

            st.error(str(e))
