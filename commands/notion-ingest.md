# /notion-ingest — Notion Workspace Crawler

> Crawls a Notion workspace to extract business terms, metrics, product docs,
> and team structure. Populates the organization knowledge system.

## Trigger
Invoked as `/notion-ingest` or `/notion-ingest {workspace_url}`

## Prerequisites
- Notion integration token configured in `.knowledge/user/integrations.yaml`
- Organization directory exists at `.knowledge/organizations/{org}/`
- If no token: "Notion integration token not found. Add it to `.knowledge/user/integrations.yaml` under `notion.token`. See [Notion Integration Guide](https://developers.notion.com/docs/create-a-notion-integration) for setup."

## Overview

This skill uses a breadth-first crawl strategy to systematically traverse a Notion
workspace, converting pages to structured knowledge entries. It does NOT require
external Python packages — all Notion API calls use inline HTTP requests.

## Step 1: Authentication Check

```python
import yaml, os

# Load integration config
integrations_path = ".knowledge/user/integrations.yaml"
with open(integrations_path) as f:
    config = yaml.safe_load(f)

notion_token = config.get("notion", {}).get("token")
if not notion_token:
    print("❌ No Notion token found. Add to .knowledge/user/integrations.yaml")
    # HALT
```

Verify token works with a simple API call:
```
GET https://api.notion.com/v1/users/me
Authorization: Bearer {token}
Notion-Version: 2022-06-28
```

## Step 2: Workspace Discovery

Ask the user for crawl scope:
```
Notion workspace connected. How would you like to crawl?

1. **Full workspace** — Crawl all accessible pages (may be slow for large workspaces)
2. **Specific database** — Provide a database URL to crawl
3. **Specific page tree** — Provide a root page URL to crawl its children
4. **Search by keyword** — Search for pages matching specific terms
```

## Step 3: BFS Crawl Strategy

```
Algorithm: Breadth-First Search (BFS)

Queue ← [root_page_id]
Visited ← {}
Results ← []

WHILE Queue is not empty:
    page_id ← Queue.dequeue()
    IF page_id IN Visited: CONTINUE
    Visited.add(page_id)

    page ← fetch_page(page_id)        # GET /v1/pages/{id}
    children ← fetch_children(page_id) # GET /v1/blocks/{id}/children

    result ← convert_to_knowledge(page, children)
    Results.append(result)

    # Enqueue child pages and linked databases
    FOR child IN children:
        IF child.type == "child_page" OR child.type == "child_database":
            Queue.enqueue(child.id)

    rate_limit_pause()  # See Step 4
```

### Page Fetch
```
GET https://api.notion.com/v1/pages/{page_id}
Authorization: Bearer {token}
Notion-Version: 2022-06-28
```

### Block Children Fetch (paginated)
```
GET https://api.notion.com/v1/blocks/{block_id}/children?page_size=100
Authorization: Bearer {token}
Notion-Version: 2022-06-28
```

Handle pagination via `has_more` and `next_cursor`.

## Step 4: Rate Limiting

Notion API limits: 3 requests per second for integration tokens.

```python
import time

class RateLimiter:
    """Simple token-bucket rate limiter for Notion API."""

    def __init__(self, requests_per_second=2.5):
        self.min_interval = 1.0 / requests_per_second
        self.last_request = 0

    def wait(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()
```

**Backoff strategy:**
- On 429 (rate limited): wait `Retry-After` header seconds, minimum 1s
- On 5xx: exponential backoff (1s, 2s, 4s), max 3 retries
- On 4xx (not 429): log error, skip page, continue crawl

## Step 5: Page-to-Markdown Conversion

Convert Notion block types to markdown:

| Notion Block Type | Markdown Output |
|-------------------|-----------------|
| paragraph | Plain text |
| heading_1 | `# Title` |
| heading_2 | `## Title` |
| heading_3 | `### Title` |
| bulleted_list_item | `- Item` |
| numbered_list_item | `1. Item` |
| code | ` ```lang\ncode\n``` ` |
| quote | `> Quote` |
| callout | `> ℹ️ Callout` |
| table | Markdown table |
| divider | `---` |
| toggle | Treat as heading + nested content |
| child_page | `[Page Title](notion://page_id)` |
| child_database | `[Database Title](notion://db_id)` |

**Rich text extraction:**
- Bold → `**text**`
- Italic → `*text*`
- Code → `` `text` ``
- Links → `[text](url)`
- Mentions → `@{mention_name}`

## Step 6: Knowledge Extraction

For each crawled page, attempt to classify and extract structured knowledge:

### Auto-Classification Rules
| Page Contains | Classification | Target File |
|---------------|---------------|-------------|
| Term definitions, glossary entries | Glossary term | `business/glossary/terms.yaml` |
| KPI, metric, formula | Metric definition | `business/metrics/index.yaml` |
| Product name, feature list | Product entry | `business/products/index.yaml` |
| OKR, objective, key result | Objective | `business/objectives/index.yaml` |
| Team name, org chart | Team entry | `business/teams/index.yaml` |
| SQL query, data pattern | Query archaeology | `.knowledge/query-archaeology/raw/` |

### Classification Heuristics
- **Glossary:** Page title contains "glossary", "definitions", "terms", OR
  content has definition-like patterns ("X is defined as", "X means")
- **Metrics:** Content contains "KPI", "metric", "formula", "calculated as",
  OR has numeric targets/thresholds
- **Products:** Content contains "product", "feature", "roadmap", OR is in
  a database with product-like properties
- **Objectives:** Content contains "OKR", "objective", "key result", "goal",
  "target", OR has quarterly references
- **Teams:** Content contains "team", "squad", "org chart", OR has role/person
  properties

### Raw Storage
All crawled pages are saved as raw markdown to:
```
.knowledge/query-archaeology/raw/notion_{page_id_short}.md
```

With YAML frontmatter:
```yaml
---
source: notion
page_id: {full_page_id}
title: {page_title}
url: {page_url}
crawled_at: {timestamp}
classification: {auto_class or "unclassified"}
---
```

## Step 7: Progress Reporting

During crawl, show progress:
```
🔄 Crawling Notion workspace...

  Pages crawled:    45/~120 (estimated)
  Terms extracted:  12
  Metrics found:    5
  Products found:   3
  Errors:           1 (skipped)

  Current: "Q4 2025 OKR Tracker"
```

## Step 8: Post-Crawl Summary

After crawl completes:
```
✅ Notion ingest complete!

  Pages crawled:     127
  Pages skipped:     3 (errors logged)

  Knowledge extracted:
    Glossary terms:  23 → business/glossary/terms.yaml
    Metrics:         8  → business/metrics/index.yaml
    Products:        5  → business/products/index.yaml
    Objectives:      12 → business/objectives/index.yaml
    Teams:           4  → business/teams/index.yaml

  Raw pages saved:   127 → .knowledge/query-archaeology/raw/

  Review extracted knowledge with `/business` to verify accuracy.
  Auto-classifications may need manual correction.
```

## Step 9: Capture to Query Archaeology

For pages containing SQL queries or data patterns, create cookbook entries:

```python
from helpers.archaeology_helpers import capture_cookbook_entry

# For each page with SQL content
capture_cookbook_entry(
    title=page_title,
    sql=extracted_sql,
    description=f"From Notion: {page_title}",
    tags=["notion-import", classification],
    source=f"notion:{page_id}"
)
```

## Error Handling

| Error | Response |
|-------|----------|
| Invalid token | "Notion token is invalid or expired. Update in `.knowledge/user/integrations.yaml`." |
| Permission denied (403) | "Cannot access page '{title}'. Check integration permissions in Notion." |
| Rate limited (429) | Auto-retry with backoff (transparent to user) |
| Network error | Retry 3x, then skip page and continue |
| Empty workspace | "No accessible pages found. Verify the integration has access to your workspace." |
| Large workspace (500+) | "Large workspace detected (~{n} pages). This may take several minutes. Continue? [Y/n]" |

## Incremental Updates

For subsequent runs, support incremental mode:
```
/notion-ingest --incremental
```

1. Read `.knowledge/organizations/{org}/notion_sync_state.yaml` for last sync timestamp
2. Use Notion search API with `filter.timestamp.last_edited_time.after` parameter
3. Only process pages modified since last sync
4. Update sync state after completion

## Reset
`/notion-ingest reset` — Clears all raw Notion pages and sync state. Does NOT remove
extracted knowledge entries (those must be cleaned via `/business` or manually).
