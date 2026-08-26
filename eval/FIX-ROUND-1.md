# FIX-ROUND-1 (from round-1 eval: 40 scenarios, 12A/17B/11C, 0 fail)

Defects clustered by CLASS across runners (multiple independent runners converged on most).
Fix the class, not the instance. Applied by three fix tracks; verification: lint + reinstall +
round-2 re-run of all C scenarios plus any scenario whose skill a fix touched.

## Track 1: bundled-code fixes (BROKEN-SCRIPT class; every fix needs a passing repro test)

1.1 forecast/scripts/forecast_helpers.py: detect_seasonality cannot detect the last computable
    lag (annual cycle on monthly data invisible below ~26 points) — extend the peak scan to the
    final lag. seasonal_naive silently falls back to a hardcoded 7-period cycle — derive the
    period from detected seasonality or require it. Add a future-values path: forecast from a
    fitted exponential_smoothing model (holt-style continuation), since nothing currently
    produces future values yet the skill's MSE rule crowns that method.
1.2 causal scripts: rosenbaum_bounds ties bug (zero-diff pairs inflate the null expectation but
    not the statistic; p_upper=1.0 at gamma=1 contradicting a significant estimate) — drop ties
    per standard practice. propensity_match must return the propensity scores its own
    assumption-checker's check_common_support needs.
1.3 data-quality-check scripts: validate_date_range / check_temporal_coverage silently coerce
    int64 YYYYMMDD to nanosecond epochs and return ok=True over 1970-01-01 — parse YYYYMMDD
    ints properly and fail loudly on unparseable dtypes. Unify null severity to ONE table
    (structural_validator's >20% BLOCKER vs SKILL text 5-50% WARNING vs dq_extras >=50%):
    canonical = <5% ok, 5-20% WARNING, >20-50% SEVERE WARNING, >50% BLOCKER; both scripts and
    the skill text updated together.
1.4 data-profiling scripts: table enumeration must respect the manifest files: list instead of
    globbing every CSV in the folder (folder-grain table bleed). srm doc key mismatch:
    skill text says result["chi2"], script returns chi2_stat — fix the skill text.

## Track 2: skill-text integrity (WRONG-INSTRUCTION + MISSING-PIECE + CONTRADICTION classes)

2.1 Template-artifact sweep (5+ mangled substitution strings from earlier scripted edits):
    visualization-patterns savefig path and action-title code line, analyst-core rule 7 path,
    question-framing Step 5 filename, context-compare orphaned notes, reliability split step-3
    sentence and no-antecedent "that cache". Repair each into clean prose/code.
2.2 data-profiling SKILL Step 3 anomaly snippet: silent no-op as written (.reset_index inside a
    trailing comment; rename clobbers the first metric column; the .mean() sed artifact) —
    rewrite the snippet cleanly and make empty-scan loud.
2.3 Phantom-reference purge (grep-verified fixes, either implement small or remove the claim):
    /setup (business, knowledge-bootstrap) -> point at connect-data + knowledge-bootstrap;
    /switch-dataset (4 skills advertise, none implements) -> implement as a section of the
    datasets skill (read/write active.yaml with confirmation) and keep the references;
    /history + /archive-analysis phantoms -> remove or fold into patterns' own instructions;
    statistical-distributions-guide.md (distribution-profiler hard-depends) -> ship a compact
    distributions reference in the skill's reference/ dir and repoint;
    triangulation's cross-verification bonus keyed to a file nothing produces -> make the
    bonus explicitly optional with its unavailable-denominator defined (fixes the S31
    ambiguity: define max = 70 base, +5 repro, +10 cross-verification, grade on achieved/max);
    export's gdoc helpers imports (no helpers module ships) -> rewrite the gdoc path to
    python-docx instructions consistent with google-doc-export;
    "Descriptive Analytics agent" / "Data Explorer agent" -> name the real skills instead;
    deck-rescue's shared/themes CSS render command -> plain markdown/HTML output guidance;
    data-map's CLAUDE.md rule numbers + MotherDuck mentions -> self-contained phrasing;
    entity-index.yaml never created -> pre-flight documents glossary as primary, entity-index
    as optional; phantom yaml helpers (safe_read_yaml etc.) -> plain "read/write the YAML".
2.4 Memory-loop closure: add a learnings check to analyst-core's Session pre-flight (mirroring
    corrections); give archaeology a WRITER: after a validated analysis, curate the final SQL
    into query-archaeology/curated/ (CK-NNN format notion-ingest already uses) — one convention
    sentence in triangulation's after-validation step and archaeology's own skill.
2.5 KNOWLEDGE.md contract expanded to the REAL tree: organizations/, user/, references/,
    global/, query-archaeology/, reliability/, comparisons/, analyses/index.yaml,
    last_profile.md, query-log.md, setup-state.yaml; ownership rows (data-profiling owns
    last_profiled; log-correction's actual corrections layout); remove "only what is listed
    here" absolutism in favor of "this is the canonical tree; skills adding stores must
    document them here".
2.6 Small contradictions: metric-spec writes the fields metrics reads (owner, granularity,
    guardrails not thresholds, typical_range, validation_status, last_validated); business vs
    metrics deference sentence; brief vocabulary unified to VIABLE/MARGINAL/NOT_VIABLE (match
    the script); deck-rescue default theme aligned with its reference file; effort-estimate
    contradiction between analysis-design rules and feedback-synthesizer template resolved
    (estimates allowed in the synthesizer template only); export "slides" wording matches the
    Slides-API delegation; stakeholder matrix one-line mapping for data-adjacent engineers;
    visualization-patterns Default Theme text made consistent (amber focus, #F7F6F2 ground,
    one palette definition).

## Track 3: rewrites (the two C-scoring flows that need surgery, + API-shape class)

3.1 context-compare: complete the rename in the body (H1, /compare invocation, worked example)
    and REPLACE the aievals-adapter execution core with a self-contained manual procedure:
    stage the definition (copy metrics index entry aside / restore after), N runs per arm as
    fresh sub-sessions per the reliability brief, collect answers, compute both arms' stats
    with reliability's bundled reliability_stats.py (relative path documented), delta report
    format kept. No external repo, no adapter.
3.2 Export API shapes: google-slides-export and notion-export rewritten to
    capability-described connector instructions rather than hardcoded tool names from the
    author's machine ("use the Google Drive/Slides connector's create-presentation and
    batch-update capabilities; discover exact tool names in-session"), notion content as
    Notion-flavored markdown per the current MCP rather than old block-JSON. Keep the
    boundary honest: what cannot be verified without the connector is stated.

## Round 2 re-run set

All C scenarios: S09, S10, S11, S12, S13, S16, S20, S21, S23, S35, S36 (+S05 regression check
for context-compare hijack after its rewrite; +S25, S31 (B, fix-touched); +S02 spot check for
template-artifact fixes). Stop rule per EVAL-DESIGN.
