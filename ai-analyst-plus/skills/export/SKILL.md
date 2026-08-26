---
name: export
description: >-
  Export analysis results in different formats for different audiences: email summaries, Slack
  updates, decision briefs, Google Docs with charts, Word docs, slide decks, or CSVs. Trigger on
  "/export", "export this as...", "send this to...", "share this analysis", "create a Google Doc",
  "make a Word document", "I need this as a deck", "write an email summary", "draft a Slack
  update", "create a brief".
---

# Skill: Export

## Purpose
Export analysis results in different formats for different audiences. Converts
pipeline outputs into ready-to-share deliverables.

## Invocation
`/export slides` — create a Google Slides deck from the latest analysis (delegates to the google-slides-export skill through the Google Drive connector)
`/export email` — write an executive summary email (markdown)
`/export slack` — write a concise Slack update (markdown)
`/export brief` — write a 1-page decision brief (markdown)
`/export data` — export analysis data tables as CSV
`/export gdoc` — create a Google Doc with full Analysis Readout (charts, SQL, bookmarks)
`/export docx` — generate a local .docx Word document (no Google upload)
`/export notion` — export analysis to a Notion page (with charts, data stamps, provenance toggles)
`/export receipt` — generate full analysis receipt (Reproduce-level audit trail)
`/export all` — generate all text formats + data (does NOT include gdoc, notion, or receipt — use `/export gdoc`, `/export notion`, and `/export receipt` separately)

Tool names vary by connector version: discover the exact tool names from the connector's available tools in-session and read each schema before calling.

## Instructions

### Step 1: Find Source Material

**Primary source detection** (use exactly ONE of these, in order):
1. `outputs/narrative_*.md` — if exists, use the **most recent by date** (check filename date suffix)
2. `outputs/analysis_*.md` — if narrative absent, use **most recent analysis**
3. `working/pipeline_summary.md` — if no outputs/ files exist
4. `working/storyboard_*.md` — last resort if above are all missing

**How to choose when multiple files exist:** Sort by filename date (YYYYMMDD or YYYY-MM-DD suffix), use the latest. If no date in filename, use file modification time.

**Supporting materials** (collect when available, but NOT primary source):
- `outputs/charts/*.png` — chart images
- `outputs/validation_*.md` — confidence score
- `outputs/close_the_loop_*.md` — success tracking + action items
- `working/sql_queries/*.sql` — SQL queries

**If no outputs exist:**
- Check `working/` for partial results
- If nothing found: "No analysis results to export. Run an analysis first or use `/run-pipeline`."

**Critical:** Once you identify the primary source, read it COMPLETELY before generating any export. Do not assume you know the content — always verify what analysis you're exporting.

### Step 2: Generate Requested Format

**Format: slides**
- If a deck was already exported for this analysis, ask: "Deck found at {url or path}. Regenerate or keep as-is?"
- Otherwise delegate to the google-slides-export skill with the latest narrative + charts. That skill builds the deck through the Google Drive connector's Slides capabilities (create presentation + batch update; it discovers the exact tool names in-session).
- Output: a Google Slides presentation; record its URL to `outputs/slides_url_{DATE}.txt`. If the connector is unavailable, the google-slides-export skill stops and says so; do not fake a deck in another format unless the user asks for one.

**Format: email**
- Structure: Subject line + 3-paragraph body (context, key finding, recommendation)
- Tone: Executive-friendly, no jargon, action-oriented
- Include: 1-2 key numbers, the "so what", and a clear ask
- **Content source:** Use ONLY findings from the source narrative — do not calculate derived metrics (e.g., revenue impact) unless they appear in the source. Simplify technical findings, but never fabricate numbers.
- **Output file:** Write the email content to `outputs/email_summary_{DATE}.md` where {DATE} is today's date in YYYY-MM-DD format (e.g., `email_summary_2026-04-04.md`). This specific file path is important for consistent organization.

**Format: slack**
- Structure: ONE focused update with bold headline + 3-5 bullet points
- Keep under 300 words, thread-friendly format
- Use emoji sparingly (checkmarks, arrows only)
- Include: key metric, direction, and recommended action
- Include a data stamp for each key finding (abbreviated format): `50K | Jan-Mar 2026 | EVENTS | B (82)`
- **Content source:** Extract directly from the source narrative — use exact numbers and findings. Do not reinterpret or add context not present in the source.
- Do not create multiple versions (Full/Short/Executive) — produce one concise update that works for team channels
- **Output file:** Write to `outputs/slack_update_{DATE}.md` where {DATE} is today's date in YYYY-MM-DD format (e.g., `slack_update_2026-04-04.md`)

**Format: brief**
- Structure: Title + Executive Summary (3 sentences) + Key Findings (numbered) +
  Recommendation + Next Steps + Appendix (data sources, methodology)
- 1 page target (~500 words)
- **Content source:** Extract all content from source narrative — do not add interpretation or derived metrics
- **Output file:** Write to `outputs/decision_brief_{DATE}.md` where {DATE} is today's date in YYYY-MM-DD format (e.g., `decision_brief_2026-04-04.md`)

**Format: data**
- Export all DataFrames from `working/` as CSVs to the `outputs/data/` directory
- Filename pattern: Use descriptive names based on what the data represents (e.g., `conversion_by_platform.csv`, `funnel_steps.csv`)
- Create `outputs/data/README.md` documenting each CSV file: columns, row count, use cases, data quality notes
- Do not create extra analysis variants or multiple versions — export only the source DataFrames that were actually used in the analysis
- **Output location:** All CSV files in `outputs/data/` directory plus `outputs/data/README.md` manifest

**Format: gdoc**

Creates a formatted Google Doc from the analysis with embedded charts, styled
headings, internal bookmark links, and SQL code blocks. Follows the Analysis
Readout template: Summary (30-second read) → Analysis (30-minute read) → Resources.

> **Formatting source of truth:** the `google-doc-export` skill owns Doc formatting
> standards (heading hierarchy, image placement, spacing). This path produces that same
> look by building a local `.docx` with python-docx (google-doc-export Section A) and
> uploading it with the connector's convert-to-Google-Doc flag — a distinct method from
> native in-Doc construction, not a restatement of it.

#### Step 0: Auth Check

Check whether Google Drive connector tools are available in this session:

1. Attempt `read_document` on any known document ID (lightweight probe).
2. **If auth works:** Proceed to Step 2a. Say nothing about auth.
3. **If MCP tools unavailable or auth expired:** Say "Connecting your Google
   account..." and run `authorize_google_docs`. Follow the browser OAuth flow.
4. **If auth still fails after one attempt:** Say "Google Docs connection failed.
   Generating a local Word document instead." Fall through to the `docx` format
   (generate .docx only, skip upload). Provide manual upload instructions:
   "You can upload `{docx_path}` to drive.google.com manually."

#### Step 2a: Re-export Detection

Check if `outputs/gdoc_export.yaml` exists:

```python
import hashlib, yaml, os

def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

yaml_path = "outputs/gdoc_export.yaml"
if os.path.isfile(yaml_path):
    with open(yaml_path) as f:
        state = yaml.safe_load(f)

    # Check if source has changed
    narrative_path = state.get("source_narrative")
    if narrative_path and os.path.isfile(narrative_path):
        current_hash = content_hash(open(narrative_path).read())
        if current_hash == state.get("source_hash"):
            # Source unchanged — ask user
            url = state.get("document_url", "")
            # Say: "Google Doc already exists at {url}. No analysis changes
            #        detected. Open it, or force re-create?"
            # If user says open: done. If force: continue to Step 2b.
```

#### Step 2b: Parse and Build .docx

Say: "Building document from analysis..." Then:

1. **Parse the pipeline outputs yourself** (no helper module ships for this):
   read the Step 1 primary source completely, collect the chart PNGs from
   `outputs/charts/`, the confidence grade from the most recent
   `outputs/validation_*.md` (the badge such as "A (94/100)"), and any SQL from
   `working/sql_queries/*.sql`. Extract the title, findings, and
   recommendations from the narrative.
2. **Build the .docx with python-docx** (`pip install python-docx` if absent),
   following the google-doc-export skill's Section A rules exactly: Analysis
   Readout structure (Summary 30-second read, then Analysis, then Resources),
   proper heading hierarchy with exactly one H1, charts inserted at their
   findings with widths set in Inches, data stamps as small italic paragraphs,
   SQL in monospace blocks.
3. Save to `outputs/report_{slug}_{YYYYMMDD}.docx` and keep that path as
   `docx_path`.

**Confidence gate:** If the parsed confidence grade is D or F, pause and ask:
"This analysis has low confidence (grade {grade}). The document will include a
prominent caveat. Create anyway?" If the user says no, abort. If yes, continue.

#### Step 2c: Upload to Google Drive

```python
# Say: "Uploading to Google Drive..."

result = the Google Drive connector's upload file to drive capability(
    file_path=docx_path,
    convert_to_google_doc=True
)
# result: {"file_id": "...", "url": "...", "name": "..."}
```

If upload fails: fall back to .docx. Say: "Drive upload failed. Your analysis
is saved locally at `{docx_path}`."

#### Step 2d: Write State

```python
import hashlib, yaml
from datetime import datetime

def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

state_path = "outputs/gdoc_export.yaml"

# Read existing state for version history
existing = {}
if os.path.isfile(state_path):
    with open(state_path) as f:
        existing = yaml.safe_load(f) or {}

version = existing.get("version", 0) + 1
history = existing.get("versions", [])
if existing.get("document_id"):
    history.append({
        "version": existing.get("version"),
        "document_id": existing.get("document_id"),
        "document_url": existing.get("document_url"),
        "created_at": existing.get("created_at"),
    })

narrative_path = "<the Step 1 primary source path>"
state = {
    "document_id": result["file_id"],
    "document_url": result["url"],
    "title": "<the parsed analysis title>",
    "created_at": datetime.now().isoformat(),
    "source_narrative": narrative_path,
    "source_hash": content_hash(open(narrative_path).read()) if narrative_path else None,
    "local_docx": docx_path,
    "charts_embedded": 0,  # set to the number of chart PNGs actually inserted in Step 2b
    "version": version,
    "versions": history,
}

with open(state_path, "w") as f:
    yaml.dump(state, f, default_flow_style=False)
```

#### Step 2e: Post-Upload Verification

After upload, do a quick read-back check:

```python
doc_text = the Google Drive connector's read document capability(document_id=result["file_id"])
```

Quick checks:
- Does the text contain the analysis title?
- Does the text contain "Summary" and "Analysis" headings?
- Does `[Chart:` appear? (indicates missing chart placeholders made it in)
- Is the document length reasonable (> 500 chars)?

If any check fails, append a note to the report: "Note: some formatting may not
have survived conversion. Review the document for any issues."

#### Step 3: Report to User

Say:
```
Your analysis is ready:
  Google Doc: {url}
  Local backup: {docx_path}

  Sections: {N findings} findings + recommendations
  Charts: {N} embedded
  Version: {version}

The .docx file is saved locally as a backup. You can share the Google Doc
link with your team.
```

If this was a re-export, also mention: "This is version {N}. Previous versions
are tracked in `outputs/gdoc_export.yaml`."

**Format: docx**

Same as `gdoc` Steps 2a-2b only (parse + build .docx). Skip auth, upload, and
state tracking. Report the .docx path to the user.

Say: "Word document saved at `{docx_path}`. You can upload it to Google Drive
manually or share it directly."

**Format: notion**

Creates a Notion page from the analysis with charts, data stamps, and provenance toggle
blocks. Follows the Notion Export skill (`the notion-export skill`).

#### Step 0: Notion Auth Check
Check whether Notion connector tools are available in this session. If not: tell the user the Notion connector is not enabled and point them to Customize > Connectors.

#### Generation
Use the notion-export skill with:
- `NARRATIVE`: latest narrative
- `CHART_FILES`: chart PNGs from `outputs/charts/`
- `DATASET`: active dataset
- `PROVENANCE_BLOCKS`: from cross-verification (if available)
- `ANALYSIS_RECEIPT`: receipt path (if Tier 3)

The agent handles Analysis Gallery detection, chart hosting, toggle blocks, and self-check.

Output: `outputs/notion_url_{{DATASET}}_{{DATE}}.txt`

Say: "Analysis exported to Notion: {url}. {N} findings with charts and provenance."

**Format: receipt**

Generates a full analysis receipt — the Reproduce-level audit trail. Contains every
query, methodology decision, cross-verification result, and confidence factor breakdown.

#### Prerequisites
- Query log must exist (`working/query_log_*.jsonl`)
- Validation report must exist (`outputs/validation_*.md`)
- If neither exists: "Cannot generate receipt. Run a full analysis first."

#### Tier 3 Pre-Export Gate
If the analysis was run at Tier 3, the receipt is generated automatically at step 18.5.
Check if `outputs/analysis_receipt_*.md` already exists:
- If exists and source unchanged: "Receipt already generated at {path}. Open it, or force re-create?"
- If exists but source changed: Regenerate

#### Generation
Invoke the `receipt-generator` agent with:
- `QUERY_LOG`: most recent query log JSONL
- `VALIDATION_REPORT`: most recent validation report
- `CROSS_VERIFICATION_REPORT`: cross-verification YAML (if available)
- `PIPELINE_STATE`: pipeline state JSON (if available)

Output: `outputs/analysis_receipt_{{DATASET_NAME}}_{{DATE}}.md`

Say: "Analysis receipt generated at `{path}`. Contains {N} findings, {N} queries, and full validation breakdown."

**Format: all**
- Run email + slack + brief + data sequentially
- Skip slides if already exists
- Does NOT include gdoc or receipt (external resource creation must be explicit)
- After completion, suggest: "Want to also create a Google Doc? Run `/export gdoc`. Need a full audit trail? Run `/export receipt`."

### Step 3: Post-Export
- List all exported files with paths
- Suggest: "Copy the email to your clipboard?" or "Want to adjust the tone?"
- For gdoc/docx: suggest sharing or other export formats

## Rules
1. Never fabricate findings — only use data from actual analysis outputs
2. Always cite the source analysis date and dataset
3. Adapt detail level to format (email = high-level, brief = medium, data = raw)
4. Apply Stakeholder Communication skill for all text outputs
5. If the analysis had confidence scores, include them in brief format
6. The `gdoc`, `notion`, and `receipt` formats create external resources or audit trails — never include them in `/export all`
7. Always generate the .docx before attempting Google upload (local fallback)
8. If `outputs/gdoc_export.yaml` shows unchanged source, offer to open existing doc

## Edge Cases
- **Partial analysis:** Export what's available, note gaps: "Note: validation step was not completed."
- **Multiple analyses in outputs/:** Use the most recent by date, or ask user which one
- **Charts missing:** Text formats still work, note: "Charts not available for this export."
- **User requests unknown format:** List available formats and ask to choose
- **gdoc with no Google auth:** Fall back to docx format automatically
- **gdoc re-export, source unchanged:** Offer to open existing doc or force re-create
- **gdoc re-export, source changed:** Create new doc, preserve version history
- **Confidence D/F on gdoc:** Warn user before creating doc (only checkpoint in gdoc flow)
- **Offline / no network:** Generate .docx only. Say: "Saved as Word doc. Upload to Drive when you're back online."
