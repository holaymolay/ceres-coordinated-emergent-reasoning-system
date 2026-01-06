# AGENTS (Canonical)
# This file is machine-readable YAML. It is the single source of truth for agent roles.

patterns:
  - planning
  - tool-use
  - reflection
  - self-correction
  - coordination
  - arbitration
  - security
  - observability
  - memory

agents:
  - name: Coordinator
    role: governance
    supports_patterns:
      - coordination
    allowed_phases:
      - planning
      - execution
      - reflection
      - correction
    side_effects: forbidden

  - name: Router
    role: governance
    supports_patterns:
      - coordination
    allowed_phases:
      - planning
      - execution
      - reflection
      - correction
    side_effects: forbidden

  - name: Planner
    role: planning
    supports_patterns:
      - planning
      - self-correction
    allowed_phases:
      - planning
      - correction
    side_effects: forbidden

  - name: Execution
    role: execution
    supports_patterns:
      - tool-use
      - self-correction
    allowed_phases:
      - execution
      - correction
    side_effects: allowed

  - name: Specialized
    role: execution
    supports_patterns:
      - tool-use
      - self-correction
    allowed_phases:
      - execution
      - correction
    side_effects: allowed

  - name: Critic
    role: critique
    supports_patterns:
      - reflection
    allowed_phases:
      - reflection
    side_effects: forbidden

  - name: Arbitration
    role: governance
    supports_patterns:
      - arbitration
    allowed_phases:
      - planning
      - execution
      - reflection
      - correction
    side_effects: forbidden

  - name: Security
    role: governance
    supports_patterns:
      - security
    allowed_phases:
      - planning
      - execution
      - reflection
      - correction
    side_effects: forbidden

  - name: Observability
    role: telemetry
    supports_patterns:
      - observability
    allowed_phases:
      - planning
      - execution
      - reflection
      - correction
    side_effects: allowed

  - name: Memory
    role: memory
    supports_patterns:
      - memory
    allowed_phases:
      - planning
      - execution
      - reflection
      - correction
    side_effects: allowed
