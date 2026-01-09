# Modes / Settings / Profiles Validation Rules

## Illegal Combinations (hard fail)
- professional mode + execution_continuity=continuous in mode defaults
- professional profile override + execution_continuity=continuous
- session overrides setting execution_continuity=continuous when active mode is professional
- profile overrides that escalate beyond base mode permissions (no override may exceed base mode capabilities)

## Auto-Downgrade Rules
- professional mode defaults execution_continuity to manual unless explicitly set to auto-safe

## Required Confirmations (when relaxing control discipline)
- Changing execution_continuity from manual → auto-safe requires explicit confirmation
- Elevating autonomy_level above base mode default requires explicit confirmation
- Relaxing questioning_policy (e.g., structured-only → bounded-options) requires explicit confirmation

## Auto-Advance Predicate (execution_continuity=auto-safe)
- Auto-advance permitted only when:
  - all blocking gaps are resolved
  - no open ClarificationRequest
  - task has deterministic acceptance criteria
  - safety_level != maximal

## Enforceability
- Rules are machine-checkable against modes_settings_profiles.schema.yaml
- Validation must fail on any illegal combination or missing confirmation predicate
