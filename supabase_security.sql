-- =======================================================
-- 🛡️ SUPABASE SECURITY FIX SCRIPT
-- RUN THIS IN YOUR SUPABASE DASHBOARD > SQL EDITOR
-- =======================================================

-- 1. Enable Row Level Security (RLS) on tables
-- This ensures no one can access data unless a Policy allows it.
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;

-- 2. Create Security Policies for 'notes' (Robust Cast)
-- "Users can only see/edit their own notes"
create policy "Users can ALL on own notes"
on notes for all
using ( auth.uid()::text = user_id::text )
with check ( auth.uid()::text = user_id::text );

-- 3. Create Security Policies for 'events' (Robust Cast)
-- "Users can only see/edit their own events"
create policy "Users can ALL on own events"
on events for all
using ( auth.uid()::text = user_id::text )
with check ( auth.uid()::text = user_id::text );

-- 4. (Optional) Verify User Profiles if you have that table
-- ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
