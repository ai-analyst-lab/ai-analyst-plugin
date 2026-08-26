# R4 ledger rows (runner 4: S14, S15, S16, S40)

| Scenario | Capability | Round | Grade | Verdict | Defect classes | Evidence |
|----------|-----------|-------|-------|---------|----------------|----------|
| S14 | Memory: correction sticks across sessions | 1 | B | PASS | MISSING-PIECE (x2, minor), AMBIGUOUS (minor) | eval/results/S14.md |
| S15 | Memory: taught rule honored next session | 1 | B | PASS | AMBIGUOUS (learnings retrieval skill-conditional) | eval/results/S15.md |
| S16 | Memory: saved SQL reused via archaeology | 1 | C | PARTIAL | MISSING-PIECE (no local writer for archaeology store; phantom archive-analysis skill), AMBIGUOUS (analyses/ format undefined) | eval/results/S16.md |
| S40 | Meta: pre-flight resolves org shorthand | 1 | B | PASS | MISSING-PIECE (entity-index.yaml never created), CONTRADICTION (KNOWLEDGE.md omits organizations/), AMBIGUOUS ({org} resolution unstated in analyst-core) | eval/results/S40.md |
