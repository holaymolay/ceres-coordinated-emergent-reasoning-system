# Modes / Settings / Profiles Interaction Flow (CLI/Chat)

## Entry Point
- Command: `/settings`
- Shows active `interaction_mode`, active profile (if any), and effective precedence order.

## Main Menu
1. View current mode/profile
2. Change mode (guided | standard | professional)
3. Manage profiles
4. Adjust session overrides
5. Exit

## Mode Change Flow
- Prompt: select mode (guided | standard | professional)
- If changing to professional and `execution_continuity` is not manual/auto-safe, prompt to reset to manual.
- Require confirmation when relaxing control (e.g., increasing autonomy_level, relaxing questioning_policy).

## Profiles Menu
1. List profiles (name, base_mode)
2. Activate profile
3. Save current as profile (name, base_mode, overrides)
4. Update profile overrides (within base_mode permissions)
5. Delete profile
6. Back

### Activate Profile
- Input: profile name
- Display: profile details (base_mode, overrides, resolved settings)
- Confirmation required if activation relaxes control discipline.

### Save Current as Profile
- Inputs: profile name, base_mode
- Derived: overrides = current session_overrides relative to base_mode
- Validation: overrides cannot exceed base_mode permissions.

### Update Profile
- Inputs: profile name, override fields
- Validation: override scope must remain within base_mode permissions.
- Confirmation required on any relaxation.

### Delete Profile
- Input: profile name
- Confirmation required.

## Session Overrides
- Allow setting session-only overrides (within schema constraints).
- Validation: respect precedence `system_defaults -> mode_defaults -> profile_overrides -> session_overrides`.
- Require confirmation on relaxation.

## Status Display (always)
- Active mode
- Active profile
- Effective settings (resolved after precedence)
- Warnings when confirmations are required or when auto-safe predicate is not met.

## Confirmation Prompts (when relaxing control)
- Changing execution_continuity from manual → auto-safe
- Elevating autonomy_level above base_mode default
- Relaxing questioning_policy (e.g., structured-only → bounded-options)

## Non-Goals
- No state mutation logic described
- No execution logic
- No UX beyond text interaction
