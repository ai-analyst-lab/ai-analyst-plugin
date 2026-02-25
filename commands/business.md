# /business — Business Context Browser

> Interactive browser for your organization's knowledge system. Explore terms,
> products, metrics, objectives, and team structure.

## Trigger
Invoked as `/business` or `/business {subcommand}`

## Prerequisites
- Organization context must exist at `.knowledge/organizations/{org}/`
- Read `.knowledge/setup-state.yaml` to find active organization
- If no org configured: "No organization context found. Run `/setup` Phase 3 to configure business context, or create one manually at `.knowledge/organizations/{name}/`."

## Subcommands

### `/business` (no args) — Overview
Display a summary of available business context:

```
📊 Business Context: {org_name}

  Glossary:    {n} terms defined
  Products:    {n} products cataloged
  Metrics:     {n} metrics specified
  Objectives:  {n} OKRs/goals tracked
  Teams:       {n} teams mapped

Type /business {category} for details.
```

**Implementation:**
1. Read `.knowledge/organizations/{org}/manifest.yaml` for org name
2. Use `helpers/business_context.py` → `load_business_context(org_path)`
3. Count entries in each category
4. Display summary table

### `/business glossary` — Browse Terms
Display all business term definitions:

```
📖 Glossary ({n} terms)

  Term              | Definition                          | Category
  ──────────────────|─────────────────────────────────────|──────────
  Active User       | User with ≥1 session in last 30d    | Engagement
  Churn             | No activity for 60+ days            | Retention
  ...
```

**Implementation:**
1. Load from `business/glossary/terms.yaml`
2. Sort alphabetically
3. Show first 20 terms; offer "Show all" if more
4. If empty: "No glossary terms defined. Add terms to `.knowledge/organizations/{org}/business/glossary/terms.yaml`."

### `/business products` — View Product Catalog
Display product hierarchy:

```
📦 Products ({n} total)

  Product           | Category    | Status    | Key Metrics
  ──────────────────|─────────────|───────────|────────────
  Core Platform     | SaaS        | Active    | MAU, Revenue
  Mobile App        | Mobile      | Active    | DAU, Retention
  ...
```

**Implementation:**
1. Load from `business/products/index.yaml`
2. Display in table format
3. If empty: "No products defined. Add products to `.knowledge/organizations/{org}/business/products/index.yaml`."

### `/business metrics` — Inspect Metric Definitions
Display metric dictionary:

```
📏 Metrics ({n} defined)

  Metric            | Type        | Formula/Definition        | Owner
  ──────────────────|─────────────|───────────────────────────|──────
  Conversion Rate   | Ratio       | signups / visitors        | Growth
  MRR               | Currency    | SUM(active_subscriptions) | Finance
  ...
```

**Implementation:**
1. Load from `business/metrics/index.yaml`
2. Cross-reference with `.knowledge/datasets/{active}/metrics/` if available
3. Show definition, type, owner
4. If empty: "No metrics defined. Use `/metrics add` to define metrics, or add to `.knowledge/organizations/{org}/business/metrics/index.yaml`."

### `/business objectives` — Review OKRs/Goals
Display current objectives:

```
🎯 Objectives ({n} active)

  Objective                      | Key Results              | Status
  ───────────────────────────────|──────────────────────────|────────
  Increase activation rate       | +15% by Q2               | On Track
  Reduce churn                   | <5% monthly by Q3        | At Risk
  ...
```

**Implementation:**
1. Load from `business/objectives/index.yaml`
2. Show status indicators (On Track / At Risk / Behind)
3. If empty: "No objectives defined. Add OKRs to `.knowledge/organizations/{org}/business/objectives/index.yaml`."

### `/business teams` — Show Team Structure
Display team organization:

```
👥 Teams ({n} mapped)

  Team              | Lead        | Focus Area        | Analysts
  ──────────────────|─────────────|───────────────────|──────────
  Growth            | Jane D.     | Acquisition       | 2
  Product           | John S.     | Core Experience   | 3
  ...
```

**Implementation:**
1. Load from `business/teams/index.yaml`
2. Show team summary
3. If empty: "No teams defined. Add team structure to `.knowledge/organizations/{org}/business/teams/index.yaml`."

### `/business lookup {term}` — Search
Search across all categories for a term:

1. Search glossary terms (exact + fuzzy match)
2. Search product names
3. Search metric names
4. Search objective text
5. Display all matches with category labels

If no match: "No results for '{term}'. Try a different search term or browse categories with `/business`."

**Implementation:**
1. Use `helpers/business_context.py` → `get_glossary()`, `get_products()`, etc.
2. Case-insensitive substring match across all categories
3. Rank: exact match > starts-with > contains
4. Show top 10 results with category badge

## Error Handling
- Missing org directory → suggest `/setup` Phase 3
- Empty categories → show helpful "how to add" message with file path
- Malformed YAML → show parse error, suggest checking file syntax
- Partial context (some categories empty) → show what exists, note gaps

## Display Rules
- Use tables for structured data (align columns)
- Limit initial display to 20 rows; offer pagination
- Always show file paths so users know where to edit
- Adapt detail level: summary for `/business`, detail for subcommands
