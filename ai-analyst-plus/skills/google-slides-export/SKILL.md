---
name: google-slides-export
description: >-
  Create properly formatted Google Slides through the Google Drive connector's Slides capabilities,
  preventing common errors (zero-weight outlines, short object IDs, oversized batches, text
  overflow) with a design system and pre-validated slide recipes. Apply on any Google Slides API
  call, when converting Marp decks, or when the user says "Google Slides", "export to slides",
  "create a presentation", "share as slides".
---

# Skill: Google Slides Export

Requires the Google Drive connector (with Google Slides access) enabled in Cowork.

## Purpose

Create properly formatted Google Slides presentations through the connector. Prevents API errors
and ensures every deck looks professional -- no text overflow, no overlapping elements,
consistent brand design.

## Connector Capabilities and Tool Discovery

Exact tool names differ by environment, so never hardcode them: discover the connector's actual
tools in-session (list the available tools and read each candidate's own schema before calling).
You need four capabilities:

1. **Create a presentation** -- creates the deck container and returns its presentation ID.
2. **Batch-update a presentation** -- applies a list of Google Slides API requests
   (`createSlide`, `createShape`, `insertText`, `updateShapeProperties`, `createImage`,
   `deleteObject`, ...) to a presentation ID. This is the workhorse call this skill's recipes feed.
3. **Read back a presentation or page** -- returns existing object IDs (needed before any
   `deleteObject`) and supports the post-build self-check.
4. **Upload a file to the user's Drive** -- used for chart images (see the Image Insertion
   Workflow); must return a file ID usable in a Drive URL.

If no available tool provides a capability, stop and tell the user to enable the Google Drive
connector (with Slides access); never fake the export or route the content elsewhere.

**The connector boundary, honestly:** the request bodies in this skill follow the public Google
Slides API `batchUpdate` format, which connectors pass through. Whether a given environment's
tools add wrapper parameters (or name things differently) cannot be verified from this file
without a live connector -- that is exactly why you discover the tools and read their schemas
in-session rather than trusting any tool name written here.

## When to Apply

Automatically whenever:
- A Slides batch-update call is about to be made through the connector
- A Google Slides deck is being designed or built

---

## Section A: Pre-Flight Checklist

Run this checklist BEFORE building any batch_update requests. Fix all violations first.

- [ ] **Object IDs >= 5 characters** -- every NEW object ID you create must be 5+ chars
     OK: `slide_2`, `hdr_bg`, `title_box`, `body_txt`
     BAD: `s2`, `t1`, `bg`, `p_t1`
     (Only applies to IDs you define; existing IDs from the API can be any length)
- [ ] **No zero-weight outlines** -- never set `outline.weight.magnitude = 0`
     BAD: `"weight": {"magnitude": 0, "unit": "PT"}` -> API error
     OK: Omit the `updateShapeProperties` outline block entirely (no border = default)
- [ ] **Slide creation uses `createSlide`** -- not `addSlide` (not a valid request type)
- [ ] **Batches <= 50 requests** -- split into batches of 50 and apply sequentially
     Each batch must complete before the next starts (do not parallelize)
- [ ] **`deleteObject` only for confirmed IDs** -- only delete element IDs returned by
     the connector's presentation/page read-back capability; never delete IDs you invented
- [ ] **Text boxes are generous** -- every text box that holds variable content must be
     at least 3000000 EMU wide and use `autoFit: AUTO_FIT`

---

## Section B: Design System

### Page Dimensions

```
Width:  9144000 EMU  (10 inches)
Height: 5143500 EMU  (5.625 inches)
1 inch = 914400 EMU
```

### Color Palette (Default Brand)

```
Dark navy:    {red: 0.118, green: 0.161, blue: 0.231}   -- header bars, full-bg dividers
Orange:       {red: 0.851, green: 0.467, blue: 0.024}   -- highlights, accent callouts
Accent green: {red: 0.02,  green: 0.588, blue: 0.412}   -- secondary metrics
Off-white:    {red: 0.969, green: 0.965, blue: 0.949}   -- slide background
White:        {red: 1.0,   green: 1.0,   blue: 1.0}     -- card backgrounds, text on dark
Dark text:    {red: 0.133, green: 0.133, blue: 0.133}   -- body text on light backgrounds
```

### Layout Zones

```
Header bar:       x=0,       y=0,       w=9144000, h=686000
Title in header:  x=457200,  y=100000,  w=8229600, h=486000
Content start:    y=800000
Left margin:      x=457200   (0.5 inch)
Right edge:       x=8686800
Content width:    8229600    (9 inches usable)
Bottom safe zone: y <= 4800000 (leaves 0.37in gutter above slide bottom)
```

### Formatting Rules

1. **autoFit on all content text boxes** -- use `"contentAlignment": "TOP"` +
  `"autoFit": {"autoFitType": "AUTO_FIT"}` in `updateShapeProperties`. Never set a
  fixed height on a text box that holds variable text content.

2. **Minimum text box width: 3000000 EMU** (3.3 inches) for any box holding sentences.
  Narrow boxes (metric labels, short tags) may be smaller.

3. **Font size hierarchy:**

  | Role | Size | Weight |
  |------|------|--------|
  | Full-slide section title (dark bg) | 28-32pt | Bold |
  | Slide title (in header bar) | 20-24pt | Bold |
  | Insight headline (below header) | 14-16pt | Bold |
  | Body / bullet text | 11-13pt | Regular |
  | Metric value (KPI card) | 24-30pt | Bold |
  | Card label / footnote | 9-11pt | Regular |

4. **Maximum 5 content elements per slide** (not counting the header RECTANGLE and title
  TEXT_BOX). If you need more, split into two slides.

5. **Maximum 3 bullet points per text box.** Max 70 characters per bullet.
  If content is longer, split into two slides or use a two-column layout.

6. **Card pattern for KPI metrics:**
  - Create a white RECTANGLE as the card background
  - Layer a large metric value TEXT_BOX on top
  - Layer a smaller label TEXT_BOX below the value
  - Card objects must be created in order: background RECTANGLE first, then text boxes

7. **Paragraph spacing inside text boxes:**
  ```json
  "paragraphStyle": {
    "spaceAbove": {"magnitude": 4, "unit": "PT"},
    "spaceBelow": {"magnitude": 4, "unit": "PT"},
    "lineSpacing": 115
  }
  ```

8. **Never use spaces or tabs for visual alignment.** Use separate text boxes positioned
  at the correct x coordinate.

---

## Section C: Layout Library

Five pre-validated slide type recipes. Each specifies exact `createShape` / `createSlide`
requests. Always pick the closest matching type; fill in text content only.

**Object ID naming convention:** `{type}_{slidenum}_{role}`
Examples: `slide_2`, `hdr_2`, `ttl_2`, `hdl_2`, `bdy_2`, `cd1_2`, `cv1_2`, `cl1_2`

---

### Type 1 -- Title Slide

*Use for: deck opening slide*
Elements: 3

```
1. RECTANGLE (full-background, dark navy)
  objectId: "bg_{n}"
  size:      w=9144000, h=5143500
  position:  x=0, y=0
  fill:      dark navy

2. TEXT_BOX (main title)
  objectId: "ttl_{n}"
  size:      w=8229600, h=900000
  position:  x=457200, y=1700000
  text:      [DECK TITLE -- headline, not label]
  font:      28pt, white, bold
  autoFit:   AUTO_FIT

3. TEXT_BOX (subtitle / context)
  objectId: "sub_{n}"
  size:      w=8229600, h=500000
  position:  x=457200, y=2700000
  text:      [Scope | Date range | Author]
  font:      16pt, off-white, regular
  autoFit:   AUTO_FIT
```

---

### Type 2 -- Section Divider

*Use for: transitions between major sections*
Elements: 2

```
1. RECTANGLE (full-background, dark navy)
  objectId: "bg_{n}"
  size:      w=9144000, h=5143500
  position:  x=0, y=0
  fill:      dark navy

2. TEXT_BOX (section name)
  objectId: "sec_{n}"
  size:      w=8229600, h=700000
  position:  x=457200, y=1900000
  text:      [SECTION NAME]
  font:      28pt, white, bold, centered
  autoFit:   AUTO_FIT
```

---

### Type 3 -- Header + Bullets

*Use for: insight findings, recommendation lists, methodology, any text-heavy slide*
Elements: 4

```
1. RECTANGLE (header bar, dark navy)
  objectId: "hdr_{n}"
  size:      w=9144000, h=686000
  position:  x=0, y=0
  fill:      dark navy

2. TEXT_BOX (slide title, inside header)
  objectId: "ttl_{n}"
  size:      w=8229600, h=486000
  position:  x=457200, y=100000
  text:      [SLIDE TITLE -- max 60 chars]
  font:      20pt, white, bold

3. TEXT_BOX (insight headline)
  objectId: "hdl_{n}"
  size:      w=8229600, h=450000
  position:  x=457200, y=800000
  text:      [INSIGHT HEADLINE -- the "so what", max 100 chars]
  font:      14pt, dark navy, bold
  autoFit:   AUTO_FIT

4. TEXT_BOX (body bullets)
  objectId: "bdy_{n}"
  size:      w=8229600, h=3300000
  position:  x=457200, y=1350000
  text:      [bullet 1\nbullet 2\nbullet 3]  (max 3 bullets, 70 chars each)
  font:      12pt, dark text, regular
  autoFit:   AUTO_FIT
```

---

### Type 4 -- KPI Cards

*Use for: metric dashboards with 2-4 key numbers side by side*
Max 4 cards. Elements: header (2) + per card (3 each) = 5-14 total.

**Card x-positions by count:**

```
2 cards: card_w=3800000  x1=457200,  x2=4686800
3 cards: card_w=2500000  x1=457200,  x2=3214200,  x3=5971200
4 cards: card_w=1800000  x1=457200,  x2=2514200,  x3=4571200,  x4=6628200
```

Card height: 2000000 EMU. Card y-position: 900000.

```
1. RECTANGLE (header bar, dark navy)    -- objectId: "hdr_{n}"
2. TEXT_BOX (slide title in header)     -- objectId: "ttl_{n}"
  [same as Type 3 header elements]

Per card i (repeat for each metric):
3i. RECTANGLE (card background, white)
   objectId: "cd{i}_{n}"
   size:      w={card_w}, h=2000000
   position:  x={xi}, y=900000
   fill:      white, rounded corners (optional)

4i. TEXT_BOX (metric value)
   objectId: "cv{i}_{n}"
   size:      w={card_w - 200000}, h=900000
   position:  x={xi + 100000}, y=1050000
   text:      [METRIC VALUE -- e.g., "40.2M" or "39.4%"]
   font:      28pt, dark navy, bold, centered

5i. TEXT_BOX (metric label)
   objectId: "cl{i}_{n}"
   size:      w={card_w - 200000}, h=400000
   position:  x={xi + 100000}, y=2050000
   text:      [METRIC LABEL -- e.g., "Monthly Active Users"]
   font:      10pt, dark text, regular, centered
   autoFit:   AUTO_FIT
```

---

### Type 5 -- Two-Column

*Use for: side-by-side comparisons, before/after, two segments*
Elements: 4

```
1. RECTANGLE (header bar, dark navy)    -- objectId: "hdr_{n}"
2. TEXT_BOX (slide title in header)     -- objectId: "ttl_{n}"
  [same as Type 3 header elements]

3. TEXT_BOX (left column)
  objectId: "lcl_{n}"
  size:      w=3900000, h=3700000
  position:  x=457200, y=900000
  font:      12pt, dark text, regular
  autoFit:   AUTO_FIT

4. TEXT_BOX (right column)
  objectId: "rcl_{n}"
  size:      w=3900000, h=3700000
  position:  x=4786800, y=900000
  font:      12pt, dark text, regular
  autoFit:   AUTO_FIT
```

---

### Type 6 -- Chart Slide (Header + Text + Image)

*Use for: findings with an embedded chart image*
Elements: 5

```
1. RECTANGLE (header bar, dark navy)    -- objectId: "hdr_{n}"
2. TEXT_BOX (slide title in header)     -- objectId: "ttl_{n}"
  [same as Type 3 header elements]

3. TEXT_BOX (insight headline)
  objectId: "hdl_{n}"
  size:      w=4000000, h=450000
  position:  x=457200, y=800000
  text:      [INSIGHT HEADLINE -- the "so what", max 100 chars]
  font:      14pt, dark navy, bold
  autoFit:   AUTO_FIT

4. TEXT_BOX (body text, left side)
  objectId: "bdy_{n}"
  size:      w=4000000, h=3300000
  position:  x=457200, y=1350000
  text:      [3 bullets max, 70 chars each]
  font:      12pt, dark text, regular
  autoFit:   AUTO_FIT

5. IMAGE (chart, right side)
  objectId: "img_{n}"
  size:      w=4300000, h=3500000
  position:  x=4572000, y=1300000
  url:       [HTTPS URL -- see Image Insertion workflow below]
```

**Image Insertion Workflow (for Type 6 slides):**

Charts are local PNG files that must be reachable at an HTTPS URL before
insertion. The Google Slides API does NOT accept `data:image/...` data URIs.

**Data handling:** charts go only to the user's own Google Drive through the
connector. Never upload charts or data to public file hosts. The files stay in
the user's Drive under their control, private by default; the upload tool sets
just enough link access for the Slides API to fetch the image.

1. **Upload each chart PNG to the user's Drive** using the connector's image/file upload
  capability (discover the exact tool in-session; it takes a local file path plus a file
  name and returns the Drive file ID and a URL):

  ```
  <drive upload tool>(
    file_path="<path to chart.png>",
    file_name="chart_name.png"
  )
  # Returns: {"file_id": "...", "url": "..."}
  ```

  Upload all charts in one pass and print the filename -> file_id map so later
  steps can reference charts by name. Before uploading, check Drive for an
  existing file with the same name uploaded in the last 24 hours and reuse its
  ID instead of creating a duplicate. Optionally create a
  "{dataset_name} - Charts" folder first for organization.

2. **Insert into slides via `createImage`, using the Drive direct-download URL**
  (`https://drive.google.com/uc?id={file_id}&export=download`):

  ```json
  {"createImage": {
    "objectId": "img_{n}",
    "url": "https://drive.google.com/uc?id={file_id}&export=download",
    "elementProperties": {
      "pageObjectId": "slide_{n}",
      "size": {"width": {"magnitude": 4300000, "unit": "EMU"},
               "height": {"magnitude": 3500000, "unit": "EMU"}},
      "transform": {"scaleX": 1, "scaleY": 1,
                     "translateX": 4572000, "translateY": 1300000, "unit": "EMU"}
    }
  }}
  ```

3. **Delete the placeholder frame (if one exists):**

  ```json
  {"deleteObject": {"objectId": "cpf_{n}"}}
  ```

  The chart already lives permanently in the user's Drive; no extra save step
  is needed, and the deck keeps working because the image URL points at the
  Drive file.

**Important API constraints:**
- BAD: `data:image/png;base64,...` -> returns 403 Forbidden
- BAD: `http://localhost:...` -> the connector cannot access local URLs
- BAD: public temporary file hosts -> links expire and the user's data leaves their control
- OK: the user's own Drive file via `https://drive.google.com/uc?id={ID}&export=download`
- All 5 `createImage` + `deleteObject` requests can go in a single batch

---

## Section D-1: Data Stamp & Speaker Notes Provenance

### Data Stamp Text Box

For finding slides (Type 3 and Type 6), add a data stamp text box at the bottom-right
corner. This provides at-a-glance provenance for every claim.

```
TEXT_BOX (data stamp)
  objectId: "dst_{n}"
  size:      w=4000000, h=250000
  position:  x=4686800, y=4800000
  text:      [abbreviated stamp: "50K | Jan-Mar 2026 | EVENTS | B (82)"]
  font:      8pt, {red: 0.6, green: 0.6, blue: 0.6}, regular
  alignment: RIGHT
  autoFit:   AUTO_FIT
```

**When to include:** Any slide presenting a specific data finding (insight headline + evidence).
**When to skip:** Title slides, section dividers, KPI dashboards, recommendation lists, appendix.

Build the abbreviated data stamp text yourself in this exact format:
`{row_count} | {date_range} | {primary_table} | {grade} ({score})`
- Abbreviate the row count (50,000 → `50K`; 1,200,000 → `1.2M`)
- When no confidence score is available, drop the final segment: `50K | Jan-Mar 2026 | EVENTS`

### Speaker Notes Provenance Format

For finding slides, speaker notes should contain full provenance so the presenter
can answer "where does this number come from?" questions:

```
Data: [145K rows | Jan-Mar 2026 | ORDERS | Confidence: B (82/100)]
Methodology: segmented comparison, SUM by segment
SQL: SELECT segment, SUM(revenue) FROM orders GROUP BY segment
Verification: Type B: Parts-to-whole — Verified (PASS, diff 0.2%)
```

Insert via `insertText` on the slide's notes page object.

---

## Section D: Reference Decks

To verify design decisions, use decks previously created by this pipeline as visual
references. Add your own reference deck IDs here after creating decks you're happy with.

Visual patterns to follow:
- Card-based layouts: colored RECTANGLE backgrounds with text boxes layered on top
- Section dividers: full dark-navy background with large centered text only
- Minimal element count: 2-4 elements on dividers, 5-10 on content slides
- Flow diagrams: CURVED_LEFT_ARROW shapes for process flows (not table data)
- Round rectangles (ROUND_RECTANGLE) as alternative card containers
