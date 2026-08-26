---
name: reliability
description: >-
  Check whether an AI analysis answer is STABLE by running the same question several independent
  times and measuring what holds versus what drifts. Trigger on "/reliability", "run this a few
  times", "is this answer stable / reliable", "check reliability of <question>", "does it give the
  same answer again", "run it N times and compare". The cheapest eval and the only one needing no
  answer key: stability, not correctness.
---

# Skill: Reliability check

## Purpose
Run one analytics question several **independent** times and report whether the answer
is stable (every run agrees) or drifting (runs disagree because the question is
under-defined). Stability is necessary, not sufficient: a wrong query is perfectly
stable. This check needs no ground truth.

## Invocation
`/reliability "<the question>" [N]` — default N = 5.
Example: `/reliability "What's our retention rate?"`

## How to run it

### Step 1 — fire N independent runs
Launch **N sub-agents in parallel** with the Task/Agent tool (N defaults to 5). They must
be genuinely independent: each gets a fresh context and sees ONLY the question, never the
other runs' answers. Give each sub-agent exactly this brief:

> You are answering one analytics question against the active dataset. Load the normal
> session context first (knowledge-bootstrap: read `.knowledge/active.yaml`, then the active
> dataset's `schema.md`, `quirks.md`, and manifest from the local datasets dir). For the
> metric dictionary and semantic context, first resolve the context dir: read
> `.knowledge/context-source.yaml`; if it exists and says `source: git`, clone or pull the
> repo it names into `.knowledge/.context-cache` (checkout the `ref`, default `main`) and use
> the dataset's directory inside that cache; otherwise use `.knowledge/datasets/{active}/`.
> Read `metrics/index.yaml` and `semantic/` from the RESOLVED dir, not from any other copy.
> Do not read `.knowledge/reliability/` history before answering. If
> the metric you're asked about is defined in the dictionary, use that definition exactly.
> If it is not, decide for yourself how best to define and measure it. Query the real data
> through the session's active data connection (the mounted files or the connected warehouse).
> Answer the question: "<QUESTION>". Then return ONLY this block:
> `headline: <the single number you'd report>`
> `measured: <one line: numerator, denominator, grain, window, any filter>`
> `definition_source: <"metric dictionary" if you used a defined metric, else "my own choice">`

Do not let the runs share state. Run them concurrently.

### Step 2 — record the runs (tracked + auditable)
Write the N results to a timestamped run directory so every check leaves an audit trail:
`.knowledge/reliability/<UTC-timestamp>-<question-slug>/runs.json`, shaped as
`{"question": "<the question>", "runs": [{"run":1,"headline":"...","measured":"...","definition_source":"..."}, ...]}`.

### Step 3 — compute the statistics (deterministic, not estimated)
Run the script bundled with this skill, using its path inside this skill's own directory:
`python3 <this skill's dir>/scripts/reliability_stats.py <the run directory from Step 2>`

**If the skill install path cannot be resolved** (some sandboxed environments): read the script file(s) from this skill, write a copy into a `scripts/` folder inside the working folder, and run from there. The scripts are self-contained.

The script computes the numbers
deterministically (never let the model estimate them): distinct values, min/max/range,
mean, stdev, CV, the agreement count + agreement rate, how many runs used the metric
dictionary, and the STABLE/DRIFT verdict. It writes `stats.json` + `report.md` in the run
dir and appends one line to `.knowledge/reliability/log.jsonl` (the audit log of every
reliability check over time, so results can be tracked).

### Step 4 — report (short, on-screen)
Show the `report.md` it produced: the `Run | headline | what it measured | source` table,
the verdict, and the computed stats (distinct values, agreement rate, CV, range). Frame it:
- **STABLE** — "Same answer every run. Lean on it being consistent. Stable is not correct
  though, a wrong query is perfectly stable too, so this says it's settled, not that it's
  the reading you meant."
- **DRIFT** — "N distinct readings. Each run quietly chose a different definition. The
  spread is the check telling you to go define this before you trust any single number."

Tell the user where it was saved (the run dir + `.knowledge/reliability/log.jsonl`). Then
the honest footnotes: N is illustrative (size it to the precision you need); this check
needs no answer key (it measures stability, not correctness); nearly free as long as the
runs are genuinely independent (some tools cache answers, and then it sees nothing).

## Notes
- The active data connection is whatever the session is configured for (mounted files or a
  connected warehouse); the sub-agents just use that same connection.
- The fix for drift is not a smarter model, it's context: define the metric once in the
  dictionary (the `/metric-spec` skill, or just tell the analyst the definition and ask it
  to save it), then run `/reliability` again and the runs converge on the meaning you set.
- One exception: when you are running a *comparison* (with-and-without, the `/context-compare` skill),
  do NOT save the definition permanently with `/metric-spec`. The comparison stages the
  definition temporarily (copies the metrics index entry aside for the with-definition runs,
  then restores the original when the comparison is done). Save into the dictionary only when
  you want the definition to be permanent, not for a comparison.
