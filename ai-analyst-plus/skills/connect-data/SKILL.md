---
name: connect-data
description: >-
  Guided wizard to connect a new dataset for analysis in Cowork: find CSV/Excel files, open local
  DuckDB, or point at a cloud warehouse via a connector, then profile the schema and register the
  dataset in .knowledge. Trigger on "/connect-data", "connect my data", "add a new dataset", "set
  up my data", "can you look at this file", "connect to Snowflake / BigQuery", or when an analysis
  request arrives and no dataset is registered yet.
---

# Skill: Connect Data

## Purpose
**This is an interactive setup wizard, not a documentation generator.** Guide the user through the actual connection process by executing each step: finding the data, testing that it reads, profiling the schema, and registering the dataset in the `.knowledge/` context store. Do not just explain what would happen. Make it happen.

## When to Use
- User says `/connect-data`, "connect my data", or "add a new dataset"
- A first analysis request arrives and no dataset is registered in `.knowledge/datasets/`
- The user drops new files into the working folder and wants to analyze them

## The three connection paths

### Path 1: Files in the working folder (first-class path)

CSV and Excel files in the mounted working folder are the primary way to connect data in Cowork. No configuration is needed: the files are already accessible.

1. **Find the files.** List the working folder for `.csv`, `.xlsx`, `.xls`, `.parquet`, and `.json` files (including subfolders like `data/`). Show what you found and ask the user to confirm which files belong to this dataset.
2. **If the user mentions files that are not there,** ask them to add the files to the working folder (or share them into the session) and re-run this step.
3. **Read each file with pandas** (`pd.read_csv` / `pd.read_excel`) and confirm it parses: row count, column names, obvious encoding or delimiter problems. Fix read options until every file loads cleanly.

Each file becomes one table, named after the file (without extension).

### Path 2: Local DuckDB files

A `.duckdb` file in the working folder works in the sandbox.

1. Ask for the path to the `.duckdb` file (relative to the working folder) and verify it exists.
2. Connect read-only with the `duckdb` package and run `SELECT 1` to confirm the file opens.
3. Enumerate tables with `SHOW TABLES` and confirm with the user.

### Path 3: Cloud warehouses via Cowork connectors (Snowflake, BigQuery, and similar)

Cloud warehouses connect through **Cowork connectors**, which the user sets up in **Customize** (not through anything this skill configures).

1. Ask whether the warehouse connector is already set up in Customize. If not, direct the user: open Customize, add the connector for their warehouse, and authenticate there. This skill cannot create or configure connectors, and no credentials are ever collected or stored here.
2. Once the connector is available, test it with a trivial query (for example `SELECT 1`), then enumerate the schemas and tables the user cares about.
3. For profiling and repeated analysis, offer to export the relevant tables (or filtered extracts) to CSV in the working folder so Path 1 tooling applies. Large tables should be extracted with an aggregating or sampling query, not pulled whole.

**Honest limitation:** a source that is only reachable inside a private network (a VPN-only Postgres, an on-prem database, an internal API) is not reachable from Cowork. Connecting to those is a job for the Claude Code version of this system, which runs on a machine inside the network. Say this plainly rather than attempting workarounds.

## Registration steps (all paths)

### Step 1: Create the dataset entry
1. **Generate a dataset_id from the display name** using lowercase letters with hyphens (NOT underscores).
   - Example: "Production Analytics" becomes `production-analytics`
   - Example: "GA4 Event Data" becomes `ga4-event-data`
2. Create `.knowledge/datasets/{id}/` in the working folder. If `.knowledge/` does not exist yet, offer to create it (it is the context store this system uses to remember your data).
3. Write `manifest.yaml` with: `dataset_id`, `display_name`, `connection` (type: `csv`, `excel`, `duckdb`, or `connector`, plus file paths or connector/table names), `created`, and `last_profiled: null`. Never store credentials or secrets in the manifest.
4. Create an empty `quirks.md` with section headers, and an empty `metrics/index.yaml`.

### Step 2: Profile the schema
1. For each table: column names, inferred types, row count, null rates, a few sample values, and detected date columns.
2. Write the result to `.knowledge/datasets/{id}/schema.md`.
3. Offer the deep profile: "Want me to deep-profile this dataset?" (runs the `data-profiling` skill). Profile before trusting any dataset.

### Step 3: Set active
1. Update `.knowledge/active.yaml` to point to the new dataset.
2. Confirm: "Connected! **{display_name}** is now your active dataset."
3. Show: table count, estimated row count, date range (if detected).
4. Suggest next steps: `/explore` to browse, `/metrics` to define metrics, or just ask a question.

## Rules
1. Never collect, echo, or store credentials. Warehouse auth lives in the Cowork connector, nowhere else.
2. Always test that the data actually reads before declaring success.
3. Always generate a `schema.md`; it is required for analysis.
4. Create the full `.knowledge/datasets/{id}/` tree even if profiling fails.
5. If a dataset with the same id already exists, ask before overwriting.

## Edge Cases
- **No data files found:** ask the user to add files to the working folder, or offer the connector path.
- **Excel with multiple sheets:** treat each sheet as a table (`{file}-{sheet}`), confirm with the user which sheets matter.
- **Connector not listed in Customize:** the warehouse may not have a Cowork connector yet; offer the CSV-export route (user exports from the warehouse UI into the working folder).
- **Private-network source:** state the limitation honestly and point to the Claude Code version; then offer the CSV-export route as the practical fallback.
- **Schema too large (>100 tables):** profile only the tables the user names, skip per-table details for the rest.
- **Dataset name collision:** append a number (for example `mydata-2`).
