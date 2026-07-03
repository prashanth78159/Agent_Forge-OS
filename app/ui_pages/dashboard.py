
import streamlit as st

def render(orchestrator, stored_workflows):

    st.markdown('''
    <div style='margin-bottom:20px'>
        <h1 style='color:#58A6FF;'>🚀 AgentForge OS</h1>
        <h4 style='color:#8b949e;'>
            Enterprise AI Agent Platform
        </h4>
    </div>
    ''',
    unsafe_allow_html=True)

    if not orchestrator:
        st.warning(
            "Configure API Key in Settings."
        )
        return

    executions = len(
        orchestrator.store.executions
    )

    workflows = len(
        stored_workflows
    )

    memory_entries = len(
        orchestrator.long_term_memory.store
    )

    total_cost = 0
    total_tokens = 0

    metrics = (
        orchestrator
        .metrics_manager
        .get_all_executions_metrics()
    )

    for execution in metrics.values():

        for item in execution:

            total_cost += item.get(
                "total_cost",
                0
            )

            total_tokens += item.get(
                "total_tokens",
                0
            )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Executions",
        executions
    )

    c2.metric(
        "Workflows",
        workflows
    )

    c3.metric(
        "Memory",
        memory_entries
    )

    c4.metric(
        "Tokens",
        total_tokens
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader(
            "🤖 Agent Health"
        )

        st.success(
            "Planner Agent"
        )

        st.success(
            "Research Agent"
        )

        st.success(
            "Writer Agent"
        )

        st.success(
            "Critic Agent"
        )

    with right:

        st.subheader(
            "📊 Platform Status"
        )

        st.success(
            "Runtime Online"
        )

        st.success(
            "Memory Online"
        )

        st.success(
            "Replay Online"
        )

        st.success(
            "Metrics Online"
        )

    st.divider()

    st.subheader(
        "🕒 Recent Executions"
    )

    execution_ids = list(
        orchestrator
        .store
        .executions
        .keys()
    )

    if execution_ids:

        for execution_id in reversed(
            execution_ids[-10:]
        ):

            st.info(
                execution_id
            )

    else:

        st.warning(
            "No executions available"
        )

    st.divider()

    st.subheader(
        "🔥 Activity Feed"
    )

    activity = []

    for execution_id, logs in (
        orchestrator.store.executions.items()
    ):

        for log in logs:

            activity.append(
                f"{execution_id} → {log['step']}"
            )

    if activity:

        for item in reversed(
            activity[-15:]
        ):

            st.write(
                "•",
                item
            )

    else:

        st.info(
            "No activity yet"
        )

    st.divider()

    st.subheader(
        "💰 Cost Summary"
    )

    st.metric(
        "Total Estimated Cost ($)",
        round(total_cost, 6)
    )
