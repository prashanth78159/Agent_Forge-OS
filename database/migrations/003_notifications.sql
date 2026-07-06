
create table if not exists notifications (

    id bigint generated always as identity primary key,

    user_id uuid,

    title text,

    message text,

    is_read boolean default false,

    created_at timestamptz default now()

);
