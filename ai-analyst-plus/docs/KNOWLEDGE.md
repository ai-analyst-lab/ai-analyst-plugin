# The .knowledge contract

The analyst keeps its memory in a `.knowledge/` folder inside your working folder. This page is
the canonical definition of that tree. Skills that add a new store must document it here in the
same change; a store that is not on this page is either brand new (add it) or a mistake (fix it).

```
.knowledge/
  active.yaml                  # which dataset is currently active (connect-data sets it; the
                               #   datasets skill's /switch-dataset rewrites it)
  setup-state.yaml             # optional setup progress marker (read by business and
                               #   knowledge-bootstrap; nothing requires it to exist)
  context-source.yaml          # optional: where semantic context lives (local vs a git repo);
                               #   read by the reliability and eval run briefs
  query-log.md                 # append-only log of live probe queries (data-map appends)
  datasets/{id}/               # one folder per dataset you have connected
    manifest.yaml              #   dataset_id, display_name, connection block (type + path +
                               #   files), created, last_profiled
    schema.md                  #   readable schema notes (connect-data writes, data-profiling
                               #   refreshes)
    quirks.md                  #   oddities found while profiling (gaps, dupes, weird codes)
    last_profile.md            #   the full deep-profile report (data-profiling owns)
    metrics/index.yaml         #   metric list for this dataset (id, name, category, direction,
                               #   validation_status, created, updated)
    metrics/{metric-id}.yaml   #   one full definition per metric (metric-spec's registration
                               #   schema: name, owner, definition.*, source.*, dimensions,
                               #   guardrails, typical_range, validation_status, last_validated,
                               #   limitations)
  corrections/                 # corrections you have given (log-correction's layout):
    log.yaml                   #   the entries (id CORR-NNN, date, severity, category, dataset,
                               #   tables, description, fix, sql_before/after, prevented_by)
    index.yaml                 #   counters + last_correction_id (analyst-core pre-flight reads
                               #   this first)
  learnings/index.md           # durable taught rules and observations that are not corrections,
                               #   as bullets under category headings
  analyses/                    # saved briefs and run records from past analyses
    index.yaml                 #   one entry per analysis (title, date, key findings) so future
                               #   sessions can surface recent work
  query-archaeology/curated/   # proven SQL store (archaeology reads; archaeology's writer
    index.yaml                 #   convention and notion-ingest write): counters
    cookbook/CK-{NNN}.yaml     #   curated query entries (id, title, sql, tables, tags, ...)
    tables/*.yaml              #   table cheatsheets
    joins/*.yaml               #   join patterns
  reliability/                 # reliability-check audit trail (reliability skill):
                               #   {timestamp}-{question}/runs.json + stats.json + report.md,
                               #   plus log.jsonl (append-only log of every check)
  comparisons/                 # context-compare run dirs (per-arm runs.json/stats.json, the
                               #   delta report, and the metrics backup staged during a run)
  global/                      # cross-dataset findings
    cross_dataset_observations.yaml   # written by compare-datasets
  organizations/{org}/         # business context (the business skill's corpus)
    manifest.yaml              #   company name, industry, description
    business/                  #   glossary/terms.yaml, products/index.yaml, metrics/index.yaml,
                               #   objectives/index.yaml, teams/index.yaml
    entity-index.yaml          #   OPTIONAL prebuilt alias index for pre-flight entity
                               #   disambiguation; the glossary files are the primary source
  user/                        # user-level context (knowledge-bootstrap creates)
    profile.md                 #   who the user is, preferences
    integrations.yaml          #   integration tokens/settings (e.g. Notion)
  references/                  # optional user-curated reference documents; skills bundle their
                               #   own references and do not require anything here
```

Who writes what:

- **connect-data** creates `datasets/{id}/` (manifest with its `connection` block, `schema.md`,
  `quirks.md`, empty `metrics/index.yaml`) and sets `active.yaml` when you connect data.
- **datasets** (`/switch-dataset`) rewrites `active.yaml` with confirmation.
- **data-profiling** writes `datasets/{id}/last_profile.md`, refreshes `schema.md`, appends
  quirks, and owns the manifest's `last_profiled` field (it sets it after every profile).
- **metric-spec** registers definitions into `datasets/{id}/metrics/`; **metrics** reads them.
- **log-correction** owns `corrections/log.yaml` + `corrections/index.yaml` and appends taught
  rules to `learnings/index.md`.
- **data-map** appends its live probes to `query-log.md`.
- **compare-datasets** writes `global/cross_dataset_observations.yaml`.
- **reliability** writes run dirs and `log.jsonl` under `reliability/`.
- **context-compare** writes its arms and delta under `comparisons/`.
- **archaeology** (writer convention, after a validated analysis) and **notion-ingest** write
  `query-archaeology/curated/`; archaeology's pre-flight retrieval reads it.
- **business** reads `organizations/{org}/`; the user (or an ingest like notion-ingest) writes it.
- **knowledge-bootstrap** creates the whole tree when it is missing, with your permission, and
  reads most of it at session start.
- **analyst-core**'s pre-flight reads `organizations/` (entity disambiguation),
  `corrections/index.yaml`, and `learnings/index.md` before any analysis.
- Every analysis skill READS the tree before writing queries: definitions first, corrections
  always, learnings for taught rules, quirks before trusting the data.

Rules:

1. If `.knowledge/` does not exist, offer to create it. Never silently skip memory.
2. Corrections are never deleted by skills. The user owns the folder and can edit anything.
3. Nothing outside the working folder is ever written. The memory travels with the folder.
4. A skill introducing a new store documents it on this page in the same change.
