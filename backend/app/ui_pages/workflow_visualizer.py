
import streamlit as st
import networkx as nx
import plotly.graph_objects as go

def render(stored_workflows):

    st.title("📈 Workflow Visualizer")

    if not stored_workflows:
        st.warning("No workflows available.")
        return

    workflow_name = st.selectbox(
        "Select Workflow",
        list(stored_workflows.keys())
    )

    workflow = stored_workflows[workflow_name]

    G = nx.DiGraph()

    for node in workflow.nodes:
        G.add_node(node.id)

    for edge in workflow.edges:
        G.add_edge(edge.source, edge.target)

    pos = nx.spring_layout(G, seed=42)

    edge_x = []
    edge_y = []

    for edge in G.edges():

        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2),
        hoverinfo="none"
    )

    node_x = []
    node_y = []
    node_text = []

    for node in G.nodes():

        x, y = pos[node]

        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="bottom center",
        marker=dict(
            size=35,
            color="lightblue"
        )
    )

    fig = go.Figure(
        data=[edge_trace, node_trace]
    )

    fig.update_layout(
        showlegend=False,
        height=600
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("Node Details")

    for node in workflow.nodes:

        with st.expander(node.id):

            st.write("Type:", node.type)
            st.json(node.config)
