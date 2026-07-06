
create table if not exists workflow_execution_state (

    execution_id text primary key,

    current_node text,

    status text,

    created_at timestamptz default now()

);
