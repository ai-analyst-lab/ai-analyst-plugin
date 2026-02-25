# Skill: Query Archaeology Retrieval

## Purpose
Retrieve proven SQL patterns, table cheatsheets, and join patterns from the
query archaeology store so agents reuse validated work instead of writing SQL
from scratch.

## When to Use
- **Automatically** before any analysis agent writes SQL (pre-flight step)
- **Manually** when the user asks about known patterns for a table or join

## Instructions

### Step 1: Check the Index

Read `.knowledge/query-archaeology/curated/index.yaml`. Parse counters:
`cookbook_entries`, `table_cheatsheets`, `join_patterns`.

**If all three are zero (or the file is missing), stop here.** Return nothing
and do not mention archaeology to the user.

### Step 2: Identify Search Terms

From the current analysis context, extract:
- **Table names** the agent is about to query (e.g., `orders`, `events`)
- **Query intent tags** (e.g., `funnel`, `retention`, `revenue`, `cohort`)

### Step 3: Search the Three Stores

Search each store that has entries (per index counts). Match using
**case-insensitive substring** -- `order` matches `orders`, `order_items`.

#### 3a. Cookbook (`curated/cookbook/*.yaml`)
For each file, check:
- `tables` array -- any element contains a search table name as substring?
- `tags` array -- any element matches a query intent tag?

Extract on match: `title`, `sql`, `tables`, `tags`, and any `caveats`/`notes`.

#### 3b. Table Cheatsheets (`curated/tables/*.yaml`)
For each file, check:
- `table_name` contains a search table name as substring?

Extract on match: `table_name`, `grain`, `primary_key`, `common_filters`,
`gotchas`, `common_joins`.

#### 3c. Join Patterns (`curated/joins/*.yaml`)
For each file, check:
- `tables` array -- at least two elements match search table names?
- If only one search table, match if `tables` contains it as substring.

Extract on match: `tables`, `join_sql`, `cardinality`, `notes`, `validated`.

### Step 4: Format Results

Return matched entries as a fenced context block. Omit sections with no matches.

```
--- QUERY ARCHAEOLOGY CONTEXT ---

## Cookbook Patterns
### {title}
Tables: {tables}  |  Tags: {tags}
```sql
{sql}
```
Caveats: {caveats or "none"}

## Table Cheatsheets
### {table_name}
- Grain: {grain}
- Primary key: {primary_key}
- Common filters: {common_filters}
- Gotchas: {gotchas}
- Common joins: {common_joins summary}

## Join Patterns
### {tables[0]} <-> {tables[1]}
Cardinality: {cardinality}  |  Validated: {validated}
```sql
{join_sql}
```
Notes: {notes}

--- END ARCHAEOLOGY CONTEXT ---
```

### Step 5: Agent Handoff

Pass the formatted block as additional context to the analysis agent. The
agent should prefer archaeology SQL over writing from scratch, respect any
gotchas listed, and note in working files when an archaeology pattern was used.

## Anti-Patterns

1. **Never mention archaeology when the store is empty** -- silent skip
2. **Never require exact matches** -- always substring so `order` finds `orders`
3. **Never load all files eagerly** -- check index counts first, skip zero stores
4. **Never modify archaeology files** -- this skill is read-only
5. **Never block analysis if retrieval fails** -- archaeology is additive, not a gate
