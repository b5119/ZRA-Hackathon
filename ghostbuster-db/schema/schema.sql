-- Companies Table
create table companies (
  id uuid primary key default gen_random_uuid(),
  company_name text not null,
  tpin text not null,
  registration_no text,
  is_flagged boolean default false,
  flag_reasons jsonb
);

-- Employees Table
create table employees (
  id uuid primary key default gen_random_uuid(),
  company_id uuid references companies(id) on delete cascade,
  name text not null,
  nrc text not null,
  is_valid_nrc boolean default true,
  exists_in_napsa boolean default true,
  is_duplicate_nrc boolean default false
);

-- Mock NAPSA Records Table
create table napsa_records (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  nrc text not null unique
);

-- PACRA Registry Table
create table pacra_registry (
  id uuid primary key default gen_random_uuid(),
  business_name text not null,
  tpin text not null,
  registration_no text not null
);
