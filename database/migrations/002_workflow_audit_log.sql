
create table if not exists workflow_audit_log (

    id bigint generated always as identity primary key,

    user_id uuid,

    workflow_id text,

    event_type text,

    event_details text,

    created_at timestamptz default now()

);
