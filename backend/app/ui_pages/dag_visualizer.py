
import json
import streamlit as st

from graphviz import Digraph

from app.services.workflow_service import (
    WorkflowService
)

from app.config.database import db


def get_node_statuses():

    try:

        result = (
            db.client
            .table(
                "workflow_node_status"
            )
            .select("*")
            .execute()
        )

        statuses = {}

        for row in result.data:

            statuses[
                row["node_name"]
            ] = row["status"]

        return statuses

    except Exception:

        return {}


def render():

    st.title(
        "🕸 DAG Visualizer"
    )

    workflows = (
        WorkflowService.get_workflows()
    )

    if not workflows:

        st.warning(
            "No workflows found."
        )

        return

    workflow_name = st.selectbox(

        "Select Workflow",

        [
            w["name"]
            for w in workflows
        ]

    )

    workflow = next(

        w

        for w in workflows

        if w["name"] == workflow_name

    )

    workflow_json = workflow.get(
        "workflow_json",
        {}
    )

    nodes = workflow_json.get(
        "nodes",
        []
    )

    edges = workflow_json.get(
        "edges",
        []
    )

    statuses = get_node_statuses()

    graph = Digraph()

    graph.attr(
        rankdir="LR"
    )

    for node in nodes:

        node_id = node.get(
            "id",
            "unknown"
        )

        status = statuses.get(
            node_id,
            "PENDING"
        )

        retries = node.get(
            "retries",
            3
        )

        if status == "COMPLETED":

            color = "lightgreen"

        elif status == "RUNNING":

            color = "gold"

        elif status == "FAILED":

            color = "lightcoral"

        else:

            color = "lightgray"

        graph.node(

            node_id,

            f"{node_id}\n{status}\nRetries:{retries}",

            style="filled",

            fillcolor=color,

            shape="box"

        )

    for edge in edges:

        source = edge.get(
            "source"
        )

        target = edge.get(
            "target"
        )

        if source and target:

            graph.edge(
                source,
                target
            )

    st.subheader(
        "Workflow DAG"
    )

    st.graphviz_chart(
        graph,
        use_container_width=True
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Nodes",
        len(nodes)
    )

    c2.metric(
        "Edges",
        len(edges)
    )

    root_nodes = [

        node["id"]

        for node in nodes

        if not any(

            edge["target"]
            ==
            node["id"]

            for edge in edges

        )

    ]

    c3.metric(
        "Root Nodes",
        len(root_nodes)
    )

    st.markdown(
        """
### Status Legend

🟢 COMPLETED

🟡 RUNNING

🔴 FAILED

⚪ PENDING
"""
    )

    with st.expander(
        "Root Nodes"
    ):

        st.write(
            root_nodes
        )

    with st.expander(
        "Workflow JSON"
    ):

        st.code(

            json.dumps(
                workflow_json,
                indent=2
            ),

            language="json"
        )
