
create table if not exists approval_history (

    id bigint generated always as identity primary key,

    approval_id text,

    action text,

    comments text,

    user_id uuid,

    created_at timestamptz default now()

);
