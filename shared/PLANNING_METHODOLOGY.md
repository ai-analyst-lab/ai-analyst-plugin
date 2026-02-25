# Planning & Execution Methodology

**Purpose:** Standard methodology for planning and executing multi-phase builds in this monorepo. When starting a new project, read this file and follow the workflow.

---

## Phase 0: Scope & Persona Selection

Before planning, define:

1. **Project brief** — What are we building? What does success look like? What constraints exist?
2. **Reference examples** — Screenshots, existing implementations, competitor examples, user-provided inspiration
3. **Available assets** — Brand tokens (`shared/brand/tokens.json`), team photos, existing templates, shared infrastructure
4. **Personas** — Select 3-5 expert personas whose combined expertise covers the full scope

### Persona Selection Criteria

Each persona should:
- Have a distinct domain of expertise (no overlap)
- Be named with a role title that implies their perspective
- Have a clear "what they care about" that drives their plan
- Challenge at least one other persona's assumptions

Typical persona archetypes:
| Archetype | Cares About | Challenges |
|-----------|-------------|------------|
| **End User Advocate** | UX, conversion, psychology | Engineers over-building |
| **Technical Architect** | Automation, maintainability, pipeline design | Designers ignoring constraints |
| **Domain Specialist** | Craft quality, fidelity, industry standards | Shortcuts that sacrifice quality |
| **Growth/Marketing Strategist** | Distribution, engagement, metrics | Builders ignoring audience |
| **Pipeline/Ops Engineer** | Reproducibility, resumability, tracking | Perfect being enemy of done |

## Phase 1: Independent Plans (Round 1)

Launch all persona agents **in parallel**. Each receives:

```
You are [PERSONA_NAME], a [ROLE_DESCRIPTION].

Context: [PROJECT_BRIEF]
Reference: [EXAMPLES_AND_ASSETS]
Constraints: [BUDGET, TIMELINE, TECH_STACK]

Produce a detailed plan from YOUR perspective covering:
1. What needs to be built (your domain)
2. How it should be structured (files, agents, pipeline)
3. What the phases/waves should be
4. Dependencies on other domains
5. Risks and unknowns
6. What you'd push back on if another expert suggested shortcuts in your area

Format: Markdown with headers, tables, and specific file paths where possible.
```

**Output:** Each persona writes their plan to `working/plans/round1/[persona-slug].md`

## Phase 2: Debate & Critique

Launch a **single debate agent** that receives ALL Round 1 plans. Its job:

```
You are a senior technical moderator. You have received [N] independent plans from these experts:
[LIST PERSONAS AND THEIR ROLES]

Your job:
1. Read all plans carefully
2. Identify AGREEMENTS (things 2+ personas align on)
3. Identify CONFLICTS (where personas disagree or have incompatible approaches)
4. Identify GAPS (things nobody addressed)
5. For each conflict, state both sides fairly and recommend a resolution with reasoning
6. For each gap, flag it and suggest which persona should own it
7. Produce a DEBATE SUMMARY with:
   - Consensus items (proceed as-is)
   - Resolved conflicts (with winner and why)
   - Open questions (need user input)
   - Gap assignments

Format: Structured markdown. Be specific — quote from the plans.
```

**Output:** `working/plans/debate-summary.md`

## Phase 3: Revised Plans (Round 2)

Launch all persona agents again **in parallel**. Each receives:
- Their original Round 1 plan
- The full debate summary
- Instructions to revise

```
You are [PERSONA_NAME] again. Here is:
1. Your original plan: [ROUND_1_PLAN]
2. The debate summary from cross-review: [DEBATE_SUMMARY]

Revise your plan to:
- Accept consensus items
- Incorporate resolved conflicts (even if you "lost" — adapt gracefully)
- Address any gaps assigned to you
- Flag remaining disagreements you feel strongly about (max 2)

Produce your REVISED plan.
```

**Output:** Each persona writes to `working/plans/round2/[persona-slug].md`

## Phase 4: Alignment & Synthesis

Launch a **single synthesis agent** that receives ALL Round 2 plans + debate summary:

```
You are the chief architect synthesizing [N] revised expert plans into one unified master plan.

Input:
- Round 2 plans from all personas
- Debate summary (for context on resolved conflicts)
- Project brief and constraints

Produce the MASTER PLAN with these exact sections:

1. **Executive Summary** — What we're building, key decisions, scope
2. **Wave Structure** — Summary table: wave number, name, task count, dependencies
3. **Detailed Waves** — For each wave:
   - Goal
   - Parallelism notes
   - Task specs (ID, description, file paths, agent type, inputs, outputs, dependencies)
4. **Dependency Graph** — ASCII diagram
5. **Files Changed Summary** — Table: wave, file, change type, description
6. **Open Questions** — Anything needing user decision before execution
```

**Output:** `[PROJECT]_MASTER_PLAN.md` at the appropriate location

## Phase 5: Build Status Tracker

After the master plan is approved, create the BUILD_STATUS.yaml:

```yaml
project: [PROJECT_NAME]
master_plan: [PATH_TO_MASTER_PLAN]
protocol: shared/PLANNING_METHODOLOGY.md
current_wave: 0
total_waves: [N]
created: YYYY-MM-DD

tasks:
  - id: W0.1
    wave: 0
    description: "[Task description]"
    status: not_started       # not_started | in_progress | completed | failed
    depends_on: []            # Task IDs that must complete first
    output_files: []          # Files created/modified by this task
    agent_type: builder       # builder | reviewer | orchestrator
    parallel_group: "W0-A"   # Tasks in same group can run simultaneously
    session: null             # Session number when completed
    notes: ""

session_log:
  - session: 1
    date: "YYYY-MM-DD"
    wave: 0
    tasks_completed: []
    tasks_failed: []
    notes: ""
```

### Status Values
| Status | Meaning |
|--------|---------|
| `not_started` | Not yet begun |
| `in_progress` | Currently being worked on |
| `completed` | Finished successfully |
| `failed` | Attempted but did not complete |

### Dependency Rules
A task is READY when:
- Status is `not_started`
- ALL tasks in `depends_on` have status `completed`
- Its wave's prerequisites are met

## Phase 6: Execution

### Session Start Protocol
1. Read BUILD_STATUS.yaml
2. Read the master plan (skim — focus on current wave)
3. Identify READY tasks (not_started + all deps completed)
4. Group into parallel batches (max 3 concurrent)
5. Announce: "Session N. Wave X. Tasks: [list]. Launching [N] builders."

### Execution Loop
```
1. Find READY tasks
2. Group into parallel batches (respect same-file conflicts)
3. Launch builder agents in parallel
4. Collect results
5. Update tracker: completed or failed with notes
6. If batch done → launch review agent
7. If review finds issues → fix → re-review
8. Repeat from 1
9. Wave complete → announce, checkpoint with user
```

### Tracker Update Rules
- **Before launching builder:** Set status to `in_progress`
- **After success:** Set to `completed`, record output_files and session
- **After failure:** Set to `failed`, record error in notes
- **After review issues:** Set affected tasks back to `in_progress`
- **At session end:** Update all statuses, write session_log entry
- **NEVER skip tracker updates** — this is ground truth for cross-session continuity

### Context Management (Crash Recovery)
- **Context getting long:** Update tracker immediately, then let compaction happen
- **Session ending:** Write session_log entry with final state
- **Resuming after crash:** Read tracker. Any `in_progress` tasks need re-checking
- **After compaction:** Re-read tracker + master plan. Tracker is single source of truth

### Quality Gates
Before progressing to next wave:
1. All tasks in current wave are `completed`
2. Review agent has passed the wave
3. No `failed` tasks remain (fixed or explicitly deferred)
4. User informed and approves

### Same-File Conflict Prevention
NEVER run parallel builders on the same output file. If multiple tasks edit the same file, they MUST run sequentially regardless of what the dependency graph says.

---

## Quick Reference: Agent Types

| Agent | Purpose | Parallelism | Prompt Pattern |
|-------|---------|-------------|----------------|
| **Builder** | Create/edit one file per spec | Up to 3 concurrent | Task ID + spec + deps + pattern reference |
| **Reviewer** | Verify batch of outputs | 1 per wave | File list + checklist |
| **Orchestrator** | Read tracker, launch agents, update tracker | 1 (main context) | Never delegated |
| **Persona** | Expert planning from one perspective | All personas parallel | Brief + role + constraints |
| **Debate Moderator** | Cross-review and resolve conflicts | 1 | All plans + conflict resolution rules |
| **Synthesizer** | Merge plans into master plan | 1 | All revised plans + debate summary |

## Quick Reference: File Naming

| File | Location | Purpose |
|------|----------|---------|
| `[PROJECT]_MASTER_PLAN.md` | Project directory | Authoritative build plan |
| `BUILD_STATUS.yaml` | Project directory | Execution tracker (ground truth) |
| `PLANNING_METHODOLOGY.md` | `shared/` (this file) | How to plan (reference) |
| `working/plans/round1/*.md` | Project directory | Round 1 persona plans |
| `working/plans/round2/*.md` | Project directory | Round 2 revised plans |
| `working/plans/debate-summary.md` | Project directory | Debate moderator output |
