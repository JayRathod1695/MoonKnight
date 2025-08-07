-- Create table for usage logs
create table if not exists public.usage_logs (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid not null,
    model       text not null,
    tokens      int not null,
    cost        float not null,
    created_at  timestamptz not null default now()
);

-- RLS
alter table public.usage_logs enable row level security;

create policy "Users can insert own usage"
    on public.usage_logs
    for insert
    with check (auth.uid() = user_id);

create policy "Users can view own usage"
    on public.usage_logs
    for select
    using (auth.uid() = user_id);
