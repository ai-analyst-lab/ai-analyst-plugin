# Skill: Data Inspect

## Purpose
Show the active dataset's schema — tables, columns, row counts, and relationships. Optionally drill into a specific table.

## When to Use
Invoke as `/data` to see the full schema summary, or `/data {table}` to see column details for a specific table.

## Instructions

### Mode 1: `/data` (full schema overview)

1. Read `.knowledge/active.yaml` to get the active dataset
2. Read `.knowledge/datasets/{active}/schema.md`
3. Display a condensed summary:

```
Active Dataset: {display_name}
Connection: {type} ({database}.{schema})

Tables:
  users          ~50,000 rows   8 columns   user_id (PK)
  products           500 rows   7 columns   product_id (PK)
  events        ~6.5M rows     9 columns   event_id (PK)
  sessions       ~1.4M rows    8 columns   session_id (PK)
  orders        ~30-50K rows   6 columns   order_id (PK)
  order_items         — rows   4 columns   order_id + product_id
  memberships         — rows   4 columns   user_id
  support_tickets ~20K rows    7 columns   ticket_id (PK)
  nps_responses   ~8K rows     5 columns   user_id
  experiment_assignments ~20K  4 columns   user_id + experiment_id
  promotions          5 rows   7 columns   promo_id (PK)
  experiments         2 rows   8 columns   experiment_id (PK)
  calendar          366 rows   4 columns   date (PK)

Use `/data {table}` for column details.
```

### Mode 2: `/data {table}` (table detail)

1. Read `.knowledge/datasets/{active}/schema.md`
2. Find the section for the requested table
3. Display the full column listing with types and descriptions
4. Show key relationships (FKs to/from this table)

### Mode 3: No active dataset

If `.knowledge/active.yaml` has no `active_dataset` or the brain doesn't exist:
- Display: "No active dataset. Run `/connect-data` to connect one, or `/datasets` to see available options."

## Anti-Patterns

1. **Never query the database just to show schema** — read from the cached schema.md file for speed
2. **Never show the full schema.md raw** — always format into the condensed table view
