# Skill: /architect

Run the multi-persona planning methodology to produce a master plan for a new project or feature.

## Parameters

- **brief** (required): What are we building? Can be a sentence, a paragraph, or "read [file]" to pull from an existing doc.
- **--personas** (optional): Override persona count. Default: 5.
- **--skip-debate** (optional): Skip Phase 2 debate and go straight to synthesis. Faster but lower quality.
- **--output-dir** (optional): Where to write plans. Default: auto-detect from project context.

## Trigger Phrases

- `/architect Build a centered-person thumbnail template`
- `/architect "Add YouTube upload to the podcast pipeline"`
- `/architect read evals-course/BUILD_PLAN.md`
- `architect a new email drip sequence for cohort 4`

## Methodology

This skill implements `shared/PLANNING_METHODOLOGY.md`. The full workflow:

```
Phase 0  Scope & Persona Selection     → define brief, pick 3-5 expert personas
Phase 1  Independent Plans (Round 1)   → all personas plan in parallel
Phase 2  Debate & Critique             → single moderator resolves conflicts
Phase 3  Revised Plans (Round 2)       → personas revise in parallel
Phase 4  Alignment & Synthesis         → single architect produces master plan
Phase 5  Build Status Tracker          → CREATE BUILD_STATUS.yaml
```

## Execution

### 1. Parse the brief

If the user provided a file path or "read [file]", read that file as the project brief.
Otherwise, use the text they provided directly.

If the brief is too vague (under 20 words, no clear deliverable), ask one clarifying question before proceeding.

### 2. Determine output directory

Look for context clues:
- If the brief mentions a specific project (podcast, analytics, evals, etc.), use that project's directory
- If a `working/plans/` directory already exists nearby, use it
- Otherwise, create `working/plans/` in the most relevant project directory
- If truly ambiguous, ask the user

Set:
- `PLANS_DIR`: `{project}/working/plans/`
- `MASTER_PLAN_PATH`: `{project}/MASTER_PLAN.md` (or `{PROJECT_NAME}_MASTER_PLAN.md`)

### 3. Phase 0: Scope & Persona Selection

Read `shared/PLANNING_METHODOLOGY.md` for the full methodology reference.

Based on the brief, select 3-5 personas. Use the archetype table from the methodology as a starting point, but customize roles to the specific project. For example:
- A thumbnail project might need: CTR Optimizer, Frontend Renderer, Brand Compositor, Pipeline Architect
- A course project might need: Curriculum Designer, Student Advocate, Technical Author, Platform Specialist

Present the personas to the user:

```
Project: [brief summary]
Output: {MASTER_PLAN_PATH}

Personas:
1. [Name] — [Role]. Cares about: [focus]. Will challenge: [what].
2. ...

Proceed with these personas? (a) Yes (b) Swap one out (c) Add/remove
```

Wait for approval before launching Phase 1.

### 4. Phase 1: Independent Plans (Round 1)

Launch all persona agents **in parallel** using the Task tool. Each persona gets:
- The project brief
- Their role description and perspective
- Any reference files or examples mentioned in the brief
- Instructions to write their plan to `{PLANS_DIR}/round1/{persona-slug}.md`

Each persona produces:
1. What needs to be built (their domain)
2. How it should be structured
3. Phases/waves
4. Dependencies on other domains
5. Risks and unknowns
6. What they'd push back on

Wait for all personas to complete.

### 5. Phase 2: Debate & Critique

If `--skip-debate`: skip to Phase 4.

Launch a **single debate agent** that receives all Round 1 plans. It identifies:
- Agreements (2+ personas align)
- Conflicts (incompatible approaches)
- Gaps (nobody addressed)
- Resolutions with reasoning

Output: `{PLANS_DIR}/debate-summary.md`

### 6. Phase 3: Revised Plans (Round 2)

Launch all persona agents again **in parallel**. Each receives:
- Their Round 1 plan
- The debate summary
- Instructions to revise and write to `{PLANS_DIR}/round2/{persona-slug}.md`

### 7. Phase 4: Synthesis

Launch a **single synthesis agent** that receives all Round 2 plans + debate summary.

Produces the master plan with sections:
1. Executive Summary
2. Wave Structure (summary table)
3. Detailed Waves (task specs with IDs, files, deps)
4. Dependency Graph
5. Files Changed Summary
6. Open Questions

Output: `{MASTER_PLAN_PATH}`

### 8. Phase 5: Build Status Tracker

After user approves the master plan, generate `BUILD_STATUS.yaml` following the schema in `shared/PLANNING_METHODOLOGY.md`.

### 9. Report

```
=== PLANNING COMPLETE ===

Master Plan:    {MASTER_PLAN_PATH}
Build Tracker:  {project}/BUILD_STATUS.yaml
Persona Plans:  {PLANS_DIR}/round1/ (5 files)
Revised Plans:  {PLANS_DIR}/round2/ (5 files)
Debate Summary: {PLANS_DIR}/debate-summary.md

Waves: [N]
Tasks: [N]
Ready to execute: "produce wave 0" or read the master plan first
```

## Shortcuts

- `/architect --quick [brief]`: Use 3 personas, skip debate (Phases 0-1-4 only). Faster for smaller projects.
- `/architect --resume`: Re-read existing plans in `working/plans/` and pick up where we left off.
