
create table if not exists workflow_versions (

    id bigint generated always as identity primary key,

    workflow_id text,

    version_number integer,

    workflow_json jsonb,

    created_at timestamptz default now()

);
