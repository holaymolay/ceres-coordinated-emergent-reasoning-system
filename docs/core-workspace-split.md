# CERES Core vs Workspace Split (Design)

Objective: Separate immutable governance (Core) from mutable execution (Workspace) without breaking existing repos.

## Proposed Structure (Repo + Directory Diagram)

```
ceres-core/                         (immutable, versioned)
  AGENTS.md
  CONSTITUTION.md
  PROMPTLOADER.md
  security.md
  access-manifest.md
  schemas/
  templates/
  scripts/                          (validators, preflight, enforcement)
  docs/

ceres-workspace/                    (mutable, project-specific)
  core/ -> git submodule (ceres-core @ vX.Y.Z)
  concepts/
  synchronizations/
  todo-inbox.md
  todo.md
  completed.md
  memory.md
  handover.md
  logs/
  runtime/
  project/
```

Notes:
- The current CERES hub can become the initial `ceres-core` repo.
- Workspace repos reference Core, they do not copy it.

## Inheritance Mechanism (Version-Pinned Core)

- Workspace includes Core as a git submodule at `core/`.
- A `core.lock` file in the Workspace records the Core tag/commit for auditability.
- All governance scripts are run from Core, for example:
  - `core/scripts/preflight.sh`
  - `core/scripts/validate-concept-graph.js`
- Workspace never overrides Core files; it only references them.

## Upgrade Semantics

- Core upgrades are opt-in only.
- Upgrade flow:
  1. Update the submodule pointer to a new Core tag/commit.
  2. Update `core.lock`.
  3. Review Core changelog and run preflight in Workspace.
- Breaking changes are handled by Core release notes and explicit upgrade steps.

## Rules

Allowed in Core:
- Governance doctrine (AGENTS, CONSTITUTION, PROMPTLOADER).
- Enforcement rules, validators, and schemas.
- Templates for canonical artifacts.
- Security and access policies.

Forbidden in Workspace:
- Modifying or shadowing Core governance documents.
- Copying Core scripts into Workspace and diverging them.
- Storing enforcement rules or schemas outside of `core/`.

## Migration Plan (Phased, Non-Destructive)

Phase 0 (now):
- Document the split and define Core vs Workspace boundaries.
- Add `core.lock` spec (no behavior change).

Phase 1:
- Extract a `ceres-core` repo from the current hub.
- Keep backward compatibility by leaving thin shims in the hub that call Core scripts.

Phase 2:
- Create a `ceres-workspace-template` that references Core via submodule.
- Update onboarding docs to point new projects at the Workspace template.

Phase 3:
- Deprecate the old monolithic layout with clear migration steps.
- Keep existing repos functional by maintaining shims during the transition window.

## Why This Split Increases Safety and Scalability

- Governance becomes stable and auditable; execution remains flexible.
- Workspaces can pin known-good Core versions and opt into upgrades.
- Cross-project consistency improves without forcing synchronized releases.
- Reduced risk of silent behavioral drift in governance logic.
