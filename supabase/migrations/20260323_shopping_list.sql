-- Shopping sections (store aisles)
create table if not exists public.shopping_sections (
  id uuid primary key default gen_random_uuid(),
  calendar_id text not null references public.calendars(id) on delete cascade,
  name text not null,
  emoji text not null default '',
  sort_order int not null default 0,
  is_preset boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (calendar_id, name)
);
alter table public.shopping_sections disable row level security;

-- Shopping items
create table if not exists public.shopping_items (
  id uuid primary key default gen_random_uuid(),
  calendar_id text not null references public.calendars(id) on delete cascade,
  name text not null,
  section_id uuid references public.shopping_sections(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table public.shopping_items disable row level security;

-- Learned keyword mappings (user teaches the system)
create table if not exists public.shopping_keyword_overrides (
  id uuid primary key default gen_random_uuid(),
  calendar_id text not null references public.calendars(id) on delete cascade,
  keyword text not null,
  section_id uuid not null references public.shopping_sections(id) on delete cascade,
  created_at timestamptz not null default now(),
  unique (calendar_id, keyword)
);
alter table public.shopping_keyword_overrides disable row level security;
