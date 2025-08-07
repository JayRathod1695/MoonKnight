-- 1. Create table
create table if not exists public.user_conversations (
    id          uuid primary key default gen_random_uuid(),
    user_id     uuid not null,
    user_text   text not null,
    ai_text     text not null,
    created_at  timestamptz not null default now()
);

-- 2. Row Level Security (RLS) ON
alter table public.user_conversations enable row level security;

-- 3. Policies: users can only read / insert their own rows
create policy "Users can insert own rows"
    on public.user_conversations
    for insert
    with check (auth.uid() = user_id);

create policy "Users can view own rows"
    on public.user_conversations
    for select
    using (auth.uid() = user_id);