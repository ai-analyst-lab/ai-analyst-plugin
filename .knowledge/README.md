# .knowledge/ -- Persistent Memory Layer

The `.knowledge/` directory is the AI Analyst's long-term memory. It stores
everything learned across sessions: dataset schemas, business context, user
corrections, reusable query patterns, and analysis history. Skills and agents
read from it at session start and write to it at analysis end.

---

## Directory Map

```
.knowledge/
├── active.yaml                 — pointer to the current dataset
├── setup-state.yaml            — onboarding interview progress tracker
├── datasets/                   — per-dataset brain (schema, metrics, quirks)
│   ├── .gitignore              — ignores profiling results and data files
│   └── _metric_schema.yaml     — shared metric entry format definition
├── corrections/                — analyst mistake log with fixes
│   ├── index.yaml              — summary counts by severity and category
│   ├── log.yaml                — append-only corrections list
│   └── log.template.yaml       — template for new entries
├── learnings/                  — accumulated insights by category
│   └── index.md                — categorized learnings (data, query, business)
├── query-archaeology/          — reusable SQL patterns and table cheatsheets
│   ├── raw/                    — unprocessed query snippets from analyses
│   ├── curated/                — reviewed patterns, organized by type
│   │   ├── cookbook/            — reusable SQL recipes (CK-nnn)
│   │   ├── tables/             — per-table cheatsheets
│   │   ├── joins/              — validated join patterns
│   │   └── index.yaml          — curated entry counts
│   └── schemas/                — JSON schemas for entry validation
├── analyses/                   — analysis archive and recurring patterns
│   ├── index.yaml              — completed analysis index
│   ├── _schema.yaml            — analysis entry format definition
│   └── _patterns.yaml          — recurring patterns across analyses
├── organizations/              — business context per org
│   └── _example/               — template org (committed)
│       ├── manifest.yaml       — org identity and industry
│       └── business/           — glossary, metrics, objectives, products, teams
├── user/                       — user profile and preferences
│   └── integrations.yaml       — export channels and communication prefs
└── global/                     — cross-dataset observations
    └── cross_dataset_observations.yaml
```

---

## Subsystem Details

### 1. Datasets (`datasets/`)
Per-dataset "brain": `manifest.yaml`, `schema.md`, `quirks.md`, and optional
`metrics/` folder. Populated by `/connect-data` and Data Profiling skill.
Profiling output (`last_profile.md`) is gitignored; schemas are committed.

### 2. Corrections (`corrections/`)
Analyst mistake log with severity, category, SQL before/after, and prevention
rule. Populated by `/log-correction`. Read by agents as pre-flight check.

### 3. Learnings (`learnings/`)
Insights in six categories: data patterns, query techniques, business context,
stakeholder preferences, visualization insights, methodology notes. Populated
during analyses. Template (`index.md`) committed; content gitignored.

### 4. Query Archaeology (`query-archaeology/`)
Reusable SQL extracted from analyses. Raw queries in `raw/`, curated into
`cookbook/`, `tables/`, and `joins/`. Populated by Archive Analysis skill.
JSON schemas in `schemas/` committed; curated entries gitignored.

### 5. Analyses (`analyses/`)
Archive of completed runs. `index.yaml` tracks question, findings, confidence
grade, and output paths. `_patterns.yaml` records recurring patterns (populated
after 3+ analyses). Schema files committed; archive entries gitignored.

### 6. Organizations (`organizations/`)
Business context per org: glossary, KPIs, products, teams, objectives. Populated
during `/setup` Phase 3. `_example/` committed as template; real orgs gitignored.

### 7. User (`user/`) and Global (`global/`)
`user/` stores profile (`profile.md`) and export preferences (`integrations.yaml`).
`global/` holds cross-dataset observations from Compare Datasets skill.
Templates committed; user-generated content gitignored.

## Gitignore Policy

**Committed** (shipped with the repo):
- Schema definitions: `_schema.yaml`, `_patterns.yaml`, `_metric_schema.yaml`
- Templates: `log.template.yaml`, `index.md`, `index.yaml` stubs
- Example org: `organizations/_example/`
- Structural markers: `.gitkeep` files, `.gitignore` files
- JSON schemas: `query-archaeology/schemas/`
- Config templates: `user/integrations.yaml`, `setup-state.yaml`, `active.yaml`

**Gitignored** (user-generated, session artifacts):
- Dataset brains created by `/connect-data` (except committed examples)
- Profiling results (`*/last_profile.md`)
- Corrections log entries
- Learnings content
- Curated query patterns
- Analysis archive entries
- Real organization business data
- User profile (`user/profile.md`)
- Cross-dataset observations

---

## Bootstrap Flow

At session start, the Knowledge Bootstrap skill runs this sequence:

1. Read `active.yaml` to find the active dataset
2. Load `datasets/{active}/manifest.yaml`, `schema.md`, and `quirks.md`
3. Load `user/profile.md` for communication preferences
4. Load `corrections/index.yaml` to surface recent mistake patterns
5. Load `organizations/{org}/` for business context if configured
6. Check `setup-state.yaml` to determine onboarding status

If no active dataset is set, the First-Run Welcome skill takes over to guide
onboarding.
