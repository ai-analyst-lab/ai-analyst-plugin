---
name: eval
description: >-
  Advanced: needs a gold-case YAML you supply and a live data connection. Run the held-out gold
  suite live against the analyst and score it. Trigger on "/eval", "run the eval suite", "score
  the system", "run the train split", "check the test split", "what's our accuracy on the gold
  cases". Drives the analyst on each question (does not grade hand-supplied answers). Pairs with
  /reliability (stability, no key) and /context-compare (two configs).
---

# Skill: Eval (live gold-suite runner)

## Purpose
Run the analyst on every question in a held-out gold suite, then score the answers against the
blind gold: accuracy (the analyst's number vs the recomputed gold), query similarity (its SQL vs
the trusted query), and cost/latency. This is the system-level eval: the number that tells you
whether the context you are adding is paying off, and the number a model comparison turns on.

Two honest properties:
- **Blind by construction.** The analyst runs see the **question only**, never the gold SQL or
  value. The gold is read only at grading, after the answers are locked.
- **Real, not staged.** Each answer is produced by actually running the analyst now. Nothing is
  pre-filled.

## The gold-case file

The suite is a YAML file you author and keep in your working folder (for example
`gold-cases.yaml`). It never lives in shared context, because the analyst must not be able to see
it. Each case is a question you already know the right answer to, paired with the query you trust
and the value it returns:

```yaml
cases:
  - id: rev-2025-q4               # short unique id
    question: "What was total net revenue in Q4 2025?"
    split: train                  # train (the set you iterate on) or test (held out)
    gold_sql: "select sum(net_revenue) from orders where order_date between '2025-10-01' and '2025-12-31'"
    gold_value: 4823910.55        # what gold_sql returns; a reference point, recomputed at grading
    # tolerance: 0.01             # optional relative tolerance; default 0.005 (0.5%)
```

The easiest way to start: take five queries your team already trusts (month-end numbers you have
reported, dashboard tiles you have verified) and record each as a case with the exact SQL and the
value it produces. Mark three or four of them `train` and keep at least one as `test`. Grading
recomputes the gold by re-running `gold_sql` against the live connection at eval time, so the
suite does not rot as new data arrives; the stored `gold_value` is a sanity reference.

## Invocation
`/eval [train|test|all] [--slice N]`, default split `train`.
- `train`: the working set you iterate on (error-analyze, add context, watch accuracy climb).
  Default.
- `test`: the held-out set. Run this ONCE at the end as the honest generalization number. Never
  iterate against it.
- `--slice N`: run only the first N cases as a quick spot check. Omit for the full split.

Examples: `/eval train` · `/eval train --slice 3` · `/eval test`

## How to run it

### Step 0: preflight (fail loud)
Verify the live data connection before anything runs: execute a trivial probe query
(`select 1`) through the session's active warehouse connection. If the probe fails, stop and
surface the error clearly; there is NO fallback engine. Do not grade against any other engine
than the one the gold was written for.

### Step 1: get the questions (blind)
Ask for the gold file's path if you do not have it. Load the question set for the requested split
by reading ONLY each case's `question` and `split` fields. Do not read `gold_sql` or `gold_value`
at this stage, so you cannot leak the key. If `--slice N` was given, take the first N.

### Step 2: run the analyst once per question
Launch one **fresh sub-agent per question** with the Task/Agent tool (run them concurrently in
reasonable batches). Each sub-agent gets a fresh context and sees ONLY its question. Time each run
(wall-clock) for latency. Give each sub-agent exactly this brief:

> You are answering one analytics question against the active dataset. Load the normal session
> context first (knowledge-bootstrap: `.knowledge/active.yaml`, then the active dataset's `schema.md`,
> `quirks.md`, and manifest from the local datasets dir). For the metric dictionary and semantic
> context, first resolve the context dir: read `.knowledge/context-source.yaml`; if it exists and
> says `source: git`, clone or pull the repo it names into `.knowledge/.context-cache` (checkout
> the `ref`, default `main`) and use the dataset's directory inside that cache; otherwise use
> `.knowledge/datasets/{active}/`. Read `metrics/index.yaml`, `semantic/`, and the verified queries
> (`verified_queries.yaml`, at the dataset root or under `semantic/` in older layouts) from the
> RESOLVED dir, not from any other copy. Do not read `.knowledge/reliability/` history before
> answering. If the metric you're asked about is defined in the dictionary, use that definition
> exactly. If it is NOT defined, decide for yourself how best to define and measure it. Query the
> real warehouse through the session's active data connection. Answer the question: "<QUESTION>".
> Return ONLY this block:
> `analyst_value: <the single number you'd report, digits only>`
> `analyst_query: <the exact SQL you ran to get it, one line>`
> `definition_source: <"metric dictionary" if you used a defined metric, else "my own choice">`

The undefined-metric cases are the ones that drift and fail at baseline; they flip to pass once
their definitions are added to the metric dictionary. That is the point of the exercise, so do not
hand the sub-agents definitions they don't have in the dictionary.

### Step 3: assemble the per-case results
Build one record per question:
`{"question", "analyst_value", "analyst_query", "latency_ms"}` (add `tokens`/`cost` per case only if
you can measure them honestly; otherwise capture run-level cost in Step 4).

### Step 4: grade against the blind gold + write the run record
Only NOW, after every analyst answer is locked, open the gold file. Grade deterministically by
writing and running a small Python script (never eyeball or estimate the numbers):

- **Accuracy (the suite metric).** For each case, recompute the gold value by running the case's
  `gold_sql` against the live connection (recomputing at eval time means the gold cannot rot).
  Parse the analyst's number (strip `$`, `%`, commas; expand `k`/`m`/`b` suffixes). Pass if it
  matches the recomputed gold within the case's relative tolerance (default 0.5%). Unit-aware
  pass: if the gold is a rate (0 < gold <= 1) and the analyst's value is about 100x it, re-check
  the analyst value divided by 100; count it as a pass but flag it `unit_adjusted`.
- **Query similarity.** Compare the analyst's SQL to the case's `gold_sql`, both normalized
  (lowercase, collapse whitespace, strip trailing semicolon): report `identical` or `changed`,
  plus a 0..1 Jaccard token-overlap similarity over the normalized SQL tokens. This measures text
  closeness, not semantic equivalence; say so if asked.
- **Aggregate.** `accuracy = passed/total`, `avg_query_similarity`, and total cost/latency when
  honestly captured (omit cost if you cannot measure it).

Write a self-describing run record `<run_id>.json` in a runs directory next to the gold suite,
carrying: timestamp, `split`, model, a one-line `changelog` (what changed since last run),
`context_state` (which metrics are currently defined in the resolved context dir's
`metrics/index.yaml`, the list that grows as you add definitions), the aggregate, and per-case
detail (question, gold value, analyst value, passed, unit_adjusted, analyst query, query_diff,
query_similarity, latency_ms).

### Step 5: report
Show the headline from the record: `accuracy = passed/total`, `avg_query_similarity`, and (when
present) `total_cost` / `cost_per_correct` / `avg_latency_ms`. Then do the **error analysis**
yourself: cluster the failures by mode (undefined-metric-drift, fan-out, wrong-filter,
wrong-grain, wrong-source), rank the modes by count, and record the clustering in the run
record. Then:
- Name the **context_state** (how many metrics are defined). The climb is this growing run over run.
- Show the ranked **failure modes**, then **diagnose** them; the diagnosis is the analyst's job,
  not the tool's: what does the dominant mode mean, and what is the fix? (Usually the definitional
  failures are missing definitions, so add them to the metric dictionary; a fan-out cluster
  usually means a join convention is needed.)
- For **train**: "this is your working number; the clustered failures show what to fix. Add the
  missing definitions, re-run, watch it climb."
- For **test**: "held-out number. If train climbed but this didn't, you overfit. Don't tune on this."
- Report the score as what this run produced, not a promised or expected figure. Accuracy depends
  on how much context has been defined, so numbers differ between setups.

## Model comparison
To compare engines or configurations, run `/eval train` in two sessions, one per configuration,
then put the two run records side by side with `/context-compare`. The cell that matters is
`cost_per_correct`. Run the comparison on **train** so the held-out test stays pristine.

## Notes
- The run record carries the `changelog` and `context_state`, so a sequence of `/eval` run records
  reads as a trend line over time: context grows, accuracy climbs.
- Blind discipline: never paste gold SQL or values into a sub-agent's context. If you need to debug
  a failure, read the run record's per-case detail (it shows gold next to analyst for the human),
  not the sub-agent.
