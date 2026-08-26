---
name: notion-export
description: >-
  Export analysis results to a Notion page with structure, embedded charts, data stamps, and
  provenance toggles. Trigger on "/export notion", "export to Notion", "create a Notion page",
  "share this in Notion", "put this in Notion", "send to Notion", or mentions of the Analysis
  Gallery database. Handles the Notion connector check, chart hosting, and toggle-block fallback.
---

# Skill: Notion Export

Requires the Notion connector enabled in Cowork.

## Purpose

Export analysis results to Notion as a well-structured page with charts, data stamps,
and provenance. Supports both standalone pages and Analysis Gallery database entries.

## Invocation

`/export notion` — export the latest analysis to Notion

## Instructions

### Step 0: Check Notion Connector Availability

Exact tool names differ by environment, so never hardcode them: discover the Notion connector's
actual tools from the session's available tools. You need two capabilities at minimum: **search**
(find pages/databases in the workspace) and **create pages**. A **read/fetch** capability is
needed for the Step 7 self-check. Read each discovered tool's own schema before calling it; the
parameter shapes below are described by capability, and the tool's schema is the authority.

1. Look for Notion tools among the available tools; attempt the search capability with a test query
2. **If tools available:** Proceed to Step 1
3. **If tools unavailable:** "The Notion connector is not configured. Set up the Notion
   integration first." Hard stop; never fake the export or route the content elsewhere.

### Step 1: Find Source Material

Same as the main export skill — find the latest narrative, charts, validation, and
close-the-loop outputs. Also gather:
- Provenance blocks (assembled from the cross-verification YAML, query log, and each finding's data stamp)
- Query log (for receipt-level detail)
- Confidence grade and score

### Step 2: Auto-Detect Analysis Gallery

Search for an "Analysis Gallery" database in the user's Notion workspace using the connector's
search capability, with a plain query ("Analysis Gallery"). Do not assume an object-type filter
parameter exists: current connectors filter by things like creator or date, if at all, not by
"database". Search plainly and inspect the results yourself for a database (or data source) named
"Analysis Gallery".

**If found:**
- Create a new page within the database
- Set properties: Title, Date, Dataset, Confidence Grade, Status
- Use the database's property schema for structured metadata

**If not found:**
- Create a standalone page
- Inform the user: "No Analysis Gallery database found. Creating a standalone page.
  To organize analyses, create a Notion database called 'Analysis Gallery' with
  properties: Title (title), Date (date), Dataset (text), Confidence (select: A/B/C/D/F),
  Status (select: Draft/Final)."

### Step 3: Build Page Structure

#### Page Title
`{Analysis Title} — {Dataset} ({Date})`

#### Page Icon
Use the confidence grade as the icon:
- A: green circle
- B: yellow circle
- C: orange circle
- D/F: red circle
- No confidence artifact for this run (common for a quick brief): skip the icon and the
  confidence callout entirely

#### Content Structure

```
Callout block: Confidence badge
  "Confidence: {grade} ({score}/100) — {interpretation}"

H2: Executive Summary
  Paragraph: 3-5 sentence overview
  Bulleted list: Key findings (max 3)

H2: Finding 1 — {title}
  Callout block (gray): Data stamp
    "{row_count} rows | {date_range} | {primary_table} | {grade} ({score})"
  Paragraph: Insight and evidence
  Image block: Chart (if available)
  Toggle block: "Show methodology & SQL"
    Paragraph: Methodology details
    Code block (sql): Full SQL query
    Paragraph: Cross-verification result

H2: Finding 2 — {title}
  ... (repeat pattern)

H2: Recommendations
  Numbered list: Action items

H2: Data Quality & Limitations
  Paragraph: Validation summary
  Bulleted list: Caveats

Divider

H3: Provenance
  Toggle block: "Full provenance for F1"
    ... (full provenance block content)
  Toggle block: "Full provenance for F2"
    ...

H3: Analysis Receipt
  Paragraph: "Full audit trail available at: outputs/analysis_receipt_{DATASET}_{DATE}.md"
```

### Step 4: Toggle Block Detection

Before building the page, check if toggle blocks work:

1. Create a test page with one toggle block via the connector's create-pages capability
2. If it succeeds: use toggle blocks for provenance sections
3. If it fails or toggles aren't supported:
   - **Fallback:** Use H3 headings instead of toggle blocks
   - Provenance details go under H3 subheadings (always visible)
   - Add a note: "Toggle blocks not available — provenance shown inline"

### Step 5: Chart Image Hosting

Charts must be hosted at a URL Notion can embed. Charts go only to the user's
own Google Drive through the connector, private by default with just enough link
access for the embed. Never upload charts or data to public file hosts.

**Workflow:**
1. Check if the Google Drive tools are available
2. If yes: upload each chart to Drive, use the shareable link
3. If no: skip embedding; note in the page "Chart not embedded (Drive
   unavailable); saved locally at {path}"
4. Insert image blocks using the hosted URL

### Step 6: Create the Page

Use the connector's create-pages capability with the structured content.

Write the page content as **Notion-flavored Markdown** in the tool's content string, not as
block JSON. (Old Notion public-API integrations built pages from `heading_2` / `paragraph` /
`callout` block objects; current connectors take markdown instead. If the discovered tool's
description points at a markdown spec resource, read that spec first and follow it.)

Map the structure from Step 3 to markdown:
- `##` for section headings, `###` for subsections
- plain paragraphs for body text
- `-` bullets and `1.` numbered lists
- fenced code blocks tagged `sql` for SQL
- `---` for dividers
- callouts (data stamps, confidence badge) and toggles (provenance sections) use the
  Notion-flavored extensions defined in the connector's markdown spec; do not guess the syntax
  from memory. If the spec offers no toggle syntax, or the Step 4 test failed, use the H3
  fallback.

Connector boundary, honestly: the exact markdown extensions supported cannot be verified without
the live connector, which is why the spec-resource read and the Step 4 toggle test exist.

### Step 7: Self-Check (6 Points)

After creating the page, read it back and verify:

1. **Title correct** — page title matches expected format
2. **All findings present** — count H2 sections matches finding count
3. **Charts embedded** — image blocks present for each chart
4. **Data stamps present** — callout blocks with data stamp text
5. **Provenance sections exist** — toggle or H3 blocks for each finding
6. **No empty sections** — no heading followed immediately by another heading

If any check fails, attempt one fix iteration (max 1 retry).

### Step 8: Report

```
Analysis exported to Notion:
  URL: {page_url}
  Location: {Analysis Gallery / Standalone page}
  Findings: {N}
  Charts: {N} embedded
  Provenance: {toggle blocks / H3 sections}
  Self-check: {PASS / PASS with {N} fixes / {N} issues flagged}
```

---

## Rules

1. **Never duplicate content.** If an Analysis Gallery entry already exists for
   this dataset + date, ask before creating a duplicate.
2. **Data stamps on every finding.** Even if provenance toggle blocks fail,
   the callout data stamps must be present.
3. **Chart URLs must be accessible.** Verify the image URL works before embedding.
   If upload fails, skip the image and note: "Chart not embedded — upload failed."
4. **One fix iteration max.** If the self-check fails after one retry, report
   issues and let the user fix manually.
5. **Never expose secrets.** Database connection strings, passwords, and API keys
   must not appear in the Notion page content.

## Edge Cases

- **No Notion connector:** Cannot export. Suggest: "Configure the Notion integration first."
- **Toggle blocks unsupported:** Fall back to H3 headings (always visible)
- **No charts available:** Create page without images, note in report
- **Google Drive unavailable:** Skip chart embedding; note the local chart paths in the page
- **Large analysis (>10 findings):** Split into sections with a table of contents at top
- **Analysis Gallery has custom properties:** Map to known properties, skip unknown ones
