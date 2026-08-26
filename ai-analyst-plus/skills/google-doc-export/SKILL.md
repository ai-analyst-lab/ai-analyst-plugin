---
name: google-doc-export
description: >-
  Create properly formatted Google Docs through the Google Docs/Drive connector, preventing
  text/image overlap, broken heading hierarchy, and inconsistent formatting. Use automatically
  whenever building a Google Doc or calling any Google Docs connector tool (create/append/format
  document, insert image, upload to Drive), or when the user wants to "create a Doc", export to
  Google Docs, or mentions Google Docs in any capacity.
---

# Skill: Google Doc Export

Requires the Google Docs connector enabled in Cowork.

**Tool discovery.** Exact tool names differ by environment; never hardcode them. Discover the
connector's actual tools in-session and read each tool's own schema before calling it. This skill
names capabilities (upload-file-to-Drive with Google Doc conversion, create document, append text,
write formatted content, insert image, upload image to Drive, read document); the discovered
tool's schema is the authority on names and parameters. If a needed capability has no tool, stop
and tell the user to enable the connector; never fake the export. What a given environment's
wrappers accept cannot be verified from this file without a live connector, which is exactly why
you discover and read schemas in-session.

## Purpose

Create properly formatted Google Docs through the connector. Prevents common issues:
text/image overlap, broken heading hierarchy, excessive whitespace, inconsistent
formatting.

---

## Section 0: Quick Decision Tree — START HERE

**Step 1: What type of document are you creating?**

- **Analysis report/writeup** → Use `.docx → Google Docs` workflow (Section A), building the `.docx` with python-docx per the Analysis Readout rules
- **Simple text-only doc** (meeting notes, memo) → Use direct connector calls (Section B)
- **Non-analysis document** (proposal, spec) → Use python-docx directly

**Step 2: Choose your approach based on document type:**

### ✅ Recommended: .docx → Google Docs Conversion (use for 90% of cases)

**When:** Any doc with charts, tables, or complex formatting (analysis reports, writeups)

**Why:** Most reliable. Avoids index calculation errors, handles images/tables automatically, always creates local backup.

**How:**
```python
# 1. Build the .docx locally with python-docx (see Section A Step 1)
# 2. Upload with the connector's upload-file-to-Drive capability, conversion flag on
<upload file to drive tool>(
    file_path="<path to report.docx>",
    convert_to_google_doc=True
)
# 3. Done! Returns Google Doc URL
```

**Capability needed:** upload a local file to the user's Drive with a convert-to-Google-Doc
option (typical shape: file path + conversion flag, returning a file ID and Doc URL). Discover
the exact tool and read its schema in-session.

### Alternative: Direct Connector Calls (simple text-only docs)

**When:** Quick text-only docs with no images/tables (meeting notes, simple memos)

**Capabilities to discover on the connector:**
- create a blank document (title → document ID)
- append text to a document
- write formatted content (headings + body blocks) to a document
- insert an image into a document (needs an image URL plus BOTH width and height)
- read a document's content back

**Note:** Do not assume richer editing tools exist (older docs reference things like
batch-update, paragraph-style updates, text modification, table insertion, structure
inspection, or text formatting tools); many connectors ship none of them. If the discovered
toolset lacks a capability, use the `.docx → Google Docs` workflow instead.

---

## Section A: Using the .docx → Google Docs Workflow (RECOMMENDED)

This is the easiest and most reliable approach for complex documents.

### Step 1: Generate .docx Locally

Build the `.docx` with python-docx (`pip install python-docx` if not present).

#### For analysis documents: follow the Analysis Readout build rules

**When:** Creating analysis reports, findings writeups, or any document following the Analysis Readout template (Context → Summary → Analysis → Next Steps → Resources).

Apply ALL of these mechanically when writing the python-docx code:
- Proper heading hierarchy (H1 → H2 → H3 → H4, no skipped levels, exactly one H1)
- Bold labels: when a paragraph starts with "The Insight:", "Why this matters for product:", "Bottom line:", "Key context:", "Data quality flag:", or "Sample size warning:", bold that label run
- Chart embedding at 6 inches wide (`doc.add_picture(path, width=Inches(6))`), each in its own paragraph, with an italic caption paragraph below it
- Figure numbering: caption every chart "Figure N: {description}", numbered in document order
- Data stamps (Section G) as a small italic paragraph below each finding heading
- Professional spacing per the Section Spacing Rules below
- The Analysis Readout template structure (Section B/C below)

**Requirements:**
- Always save to the `outputs/` directory
- Use descriptive filename with date suffix: `report_[title]_[YYYYMMDD].docx`

#### For non-analysis documents (proposals, specs, design docs)

Use python-docx directly with a clean heading hierarchy; the readout template does not apply.

**Example:**
```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
# Add title
title = doc.add_heading('Document Title', level=1)
# Add content sections...
# Add charts
doc.add_picture('/path/to/chart.png', width=Inches(6))
# Save
doc.save('outputs/report_title_20260404.docx')
```

### Step 2: Upload with Conversion

**CRITICAL: The local .docx file IS your backup. Do not delete it.**

```python
result = <upload file to drive tool>(
    file_path=docx_path,
    convert_to_google_doc=True
)

# Returns: {"file_id": "...", "url": "https://docs.google.com/document/d/..."}
```
(Use the connector's upload-file-to-Drive tool discovered in-session; parameter names follow
its schema.)

### Step 3: Confirm Deliverables

You now have TWO deliverables (always provide both to the user):

1. **Live Google Doc** - `result["url"]`
   - Editable, shareable, lives in Google Drive
   - Charts embedded permanently (no expiration)

2. **Local backup** - `docx_path`
   - Archival copy in `/outputs/` directory
   - Useful for version control, offline access
   - REQUIRED: Always mention both the Google Doc URL AND the local file path in your response to the user

### Why This Works Better

Google's .docx converter handles:
- Image placement (no index calculation needed)
- Table creation (no manual cell population)
- Bold/italic/heading styles
- Spacing and layout

No risk of index invalidation, no image timing issues, no expiring image links.

---

## Section B: Direct Connector Calls (Simple Docs Only)

For simple text-only documents, you can call the connector's document tools directly
(discovered in-session; the shapes below are typical, the tool schemas are the authority).

### Create and Populate

```python
# 1. Create blank doc (create-document capability)
result = <create document tool>(title="Meeting Notes")
doc_id = result["document_id"]

# 2. Add formatted content (write-formatted-content capability)
content_blocks = [
    {"type": "heading1", "text": "Meeting Notes\n"},
    {"type": "body", "text": "Attendees: Alice, Bob\n\n"},
    {"type": "heading2", "text": "Discussion Points\n"},
    {"type": "body", "text": "We reviewed the Q1 results...\n"}
]

<write formatted content tool>(
    document_id=doc_id,
    content_blocks=json.dumps(content_blocks)
)
```

### Insert Images (if needed)

**Data handling:** chart images go only to the user's own Google Drive through
the connector, private by default. Never upload charts or data to public file
hosts; use the Drive file reference/URL from `upload_image_to_drive`.

```python
# 1. Upload image to Drive first (upload-image-to-Drive capability)
image_result = <upload image to drive tool>(
    file_path="<path to chart.png>"
)
image_url = image_result["url"]

# 2. Read doc to find insertion index (read-document capability)
doc_content = <read document tool>(document_id=doc_id)
# Find the index where you want the image

# 3. Insert image with BOTH width and height (insert-image capability)
<insert image tool>(
    document_id=doc_id,
    image_url=image_url,
    width_pts=400,
    height_pts=300  # REQUIRED - calculate from aspect ratio if needed
)
```

**Critical:** Always specify BOTH `width_pts` and `height_pts`. Omitting height causes API error.

---

## Section C: Document Structure Standards

### Standard Analysis Document Template

Use this structure for analysis reports:

- [ ] **Text inserted before images** — all text content must be in the doc
      before any image insertion. Images shift all indices.
- [ ] **Images in dedicated paragraphs** — every image gets its own paragraph.
      Never insert an image into a paragraph that already contains text.
- [ ] **Bottom-to-top image insertion** — insert the last section's image first,
      then work backwards. Prevents index invalidation.
- [ ] **Re-read structure after each image** — read the document back after
      every image insertion to get fresh indices.
- [ ] **Heading hierarchy is clean** — exactly one H1, H2 for sections, H3 for
      subsections. No skipped levels.
- [ ] **No more than 2 consecutive empty paragraphs** anywhere in the document.
- [ ] **Drive file IDs used for images** (never public file-host URLs; those expire and put the user's data outside their control).
- [ ] **Image deduplication audit** — before inserting any image, inspect the doc
      structure and check for existing 2-char paragraphs (inline object + newline)
      at the target location. If an image already exists there, skip insertion.
- [ ] **Table spacing** — every table must have 1 empty paragraph before and after
      it. Text must never run directly into a table or start immediately after one.
- [ ] **No stub headings** — never insert a heading without body content beneath it.
      If data for a section doesn't exist, omit the heading entirely.
- [ ] **Both width AND height specified for images** — the image-insertion tool requires
      both dimensions. Omitting height causes an API error.

---

## Section B: Document Structure Template

### Standard Analysis Document

```
H1: [Document Title]
    [Subtitle — scope, date, author]

H2: Executive Summary
    [3-5 sentence overview]
    [Numbered key findings — max 3]
    [Bottom line statement]

H2: Section 1: [Topic]
    [Chart image — centered, 400pt wide]
    [The Insight: bold label + finding]
    [Supporting evidence paragraphs]
    [Why this matters for product: bold label + implication]

H2: Section 2: [Topic]
    ... (repeat pattern)

H2: Data Quality and Limitations
    [Outlier investigation]
    [Sample size notes]
    [Methodology caveats]

H2: Recommendations
    [Numbered list of actionable recommendations]
    [Each with a bold title + explanation paragraph]

H2: Appendix
    [Summary statistics tables]
```

### Section Spacing Rules

```
After H1:          2 empty paragraphs
After H2:          1 empty paragraph
Before chart:      1 empty paragraph
After chart:       1 empty paragraph
Before table:      1 empty paragraph
After table:       1 empty paragraph
Between sections:  2 empty paragraphs (includes the pre-H2 spacing)
Between paragraphs: 0 empty paragraphs (natural paragraph spacing)
After bullet list:  1 empty paragraph
```

---

### Spacing Rules

```
After H1:          2 empty paragraphs
After H2:          1 empty paragraph
Before chart:      1 empty paragraph
After chart:       1 empty paragraph
Before table:      1 empty paragraph
After table:       1 empty paragraph
Between sections:  2 empty paragraphs
Between paragraphs: 0 empty paragraphs (natural spacing)
After bullet list:  1 empty paragraph
```

### Bold Labels (apply these when building the .docx)

These phrases should always be bold when they appear at the start of a paragraph:
- "The Insight:"
- "Why this matters for product:"
- "Bottom line:"
- "Key context:"
- "Data quality flag:"
- "Sample size warning:"

---

## Section D: Image Sizing Reference

```
Standard chart:     width=400, height=300  (4:3 ratio)
Wide chart:         width=500, height=280  (16:9 ratio)
Square chart:       width=350, height=350  (1:1 ratio)
Small inline:       width=250, height=200  (for side notes)
```

Always specify both width and height. If only one dimension is known,
calculate the other from the image's aspect ratio.

---

## Section E: Common Pitfalls

| Pitfall | What happens | Prevention |
|---------|-------------|------------|
| Use a public file-host URL | Link expires and the chart leaves the user's Drive | Upload to the user's Drive via the connector, or use .docx embed |
| Omit height in insert_image | API error: "height must be greater than 0" | Always specify both width AND height |
| Assume a tool name instead of discovering it | Tool not found error | Discover the connector's tools in-session (Section F capabilities) |
| No local backup | Doc only exists in Google's cloud | Use .docx → Google Docs conversion |
| Complex doc via API calls | Index errors, image placement failures | Use .docx conversion instead |
| Too many empty paragraphs | Excessive whitespace, unprofessional | Max 2 consecutive empty paragraphs |
| Stub headings with no body | Orphaned headings confuse readers | Only insert headings that have content beneath |

---

## Section F: Quick Reference - Connector Capabilities

Discover the exact tool for each capability in-session; the shapes below are the typical
contract, and each tool's own schema is the authority on names and parameters.

```python
# Document operations
create document        (title) → {"document_id": ...}
read document          (document_id) → content
append text            (document_id, text) → status
write formatted content(document_id, content_blocks) → status

# Image operations
insert image           (document_id, image_url, width_pts, height_pts) → status
upload image to Drive  (file_path, file_name) → {"file_id": ..., "url": ...}

# File operations (RECOMMENDED for complex docs)
upload file to Drive   (file_path, convert_to_google_doc) → {"file_id": ..., "url": ...}
```

**Capabilities you should NOT count on existing** (older docs reference them; many connectors
ship no such tools): document batch-update, paragraph-style updates, in-place text
modification/formatting, table insertion, and document-structure inspection/debugging.

If you need these features, use the .docx → Google Docs workflow (Section A).

---

## Section G: Citation Pattern & Provenance Appendix

When creating analysis documents with findings, embed provenance data at three levels:

### Level 1: Data Stamps (Always Present)

Every finding paragraph must include a data stamp inline, immediately after the finding title or key claim:

```
**Finding 1: Mobile converts at half the rate of desktop**
[50K rows | Jan-Mar 2026 | EVENTS | Confidence: B (82/100)]
```

Build the data stamp yourself in this exact format:
`[{rows} rows | {date range} | {PRIMARY_TABLE} | Confidence: {grade} ({score}/100)]`
- Abbreviate the row count (50,000 → `50K`; 1,200,000 → `1.2M`)
- When no confidence score is available, drop that segment: `[50K rows | Jan-Mar 2026 | EVENTS]`

In the `.docx` workflow, render data stamps as a small italic paragraph below each finding heading. In direct connector mode, insert as body text with 9pt font and muted gray color.

### Level 2: Citation Links + Provenance Appendix

For Tier 2+ analyses, add citation markers and a provenance appendix.

**Two-pass approach:**

**Pass 1 — Build content:**
1. For each finding, insert a citation marker `[F1]` after the data stamp
2. At the end of the document (before any existing Appendix), add:
   ```
   H2: Provenance Appendix

   H3: F1: Mobile converts at half the rate
   **Data:** [50K rows | Jan-Mar 2026 | EVENTS | Confidence: B (82/100)]
   **Methodology:** segmented comparison, COUNT by device
   **SQL:**
   ```sql
   SELECT device, COUNT(*) FROM events GROUP BY device
   ```
   **Cross-verification:** Type B: Parts-to-whole — Verified (PASS, diff 0.2%)

   H3: F2: ...
   ```

**Pass 2 — Link citations (`.docx` workflow only):**
When building the `.docx`, create:
- Bookmark anchors on each `H3` in the Provenance Appendix (named `F1`, `F2`, etc.)
- Hyperlinks from `[F1]` markers in the body to the corresponding bookmark

python-docx has no high-level bookmark API: insert the `w:bookmarkStart`/`w:bookmarkEnd`
elements on the appendix headings and wrap each `[F1]` marker in a `w:hyperlink` element
with `w:anchor="F1"` via the paragraph's XML.

For direct connector mode, citation links are not possible (the API doesn't support internal bookmarks). Use the `[F1]` text markers without hyperlinks; the reader can scroll to the appendix.

### Level 3: Full Receipt Link

For Tier 3 analyses, add a link to the analysis receipt at the bottom of the document:

```
H2: Analysis Receipt
Full audit trail with all queries, methodology, and reproducibility data:
→ outputs/analysis_receipt_{DATASET}_{DATE}.md
```

### Building Provenance Blocks

Assemble the provenance blocks yourself, one per finding, from the analysis run's own
artifacts:
- The finding's data stamp (format above), from the query result's row count, date range,
  and primary table
- **Methodology:** one line naming the analytical approach (e.g. "segmented comparison,
  COUNT by device")
- **SQL:** the exact query that produced the finding, if available
- **Cross-verification:** the check type and verdict from the validation step, if available
  (e.g. "Type B: Parts-to-whole — Verified (PASS, diff 0.2%)")
- The connection type and database, from the active dataset manifest

Render each block as the appendix entry format shown in Pass 1 above.

### Checklist for Citation-Enabled Documents

- [ ] Every finding has a data stamp (even without citation links)
- [ ] Citation markers `[F1]`, `[F2]` appear after each data stamp (Tier 2+)
- [ ] Provenance Appendix section exists with one H3 per finding (Tier 2+)
- [ ] Each appendix entry has: data stamp, methodology, SQL (if available), cross-verification (if available)
- [ ] Bookmark links resolve correctly in `.docx` output (Tier 2+)
- [ ] Receipt link present at document end (Tier 3 only)
