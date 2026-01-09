# Mobile Domain Boundary (CERES)

## Responsibility
CERES covers mobile planning, specification, and governed artifact production only. It defines mobile Concepts, Synchronizations, Skills, Plugins, and read-only UI views without introducing new execution authority.

## Out of Scope
- Building binaries or running build pipelines
- Running emulators or simulators
- Code signing or provisioning
- App store submission or deployment
- Device testing or CI orchestration

## Artifact Flow to External Pipelines
- Input: Objective Contract, Spec Elicitation Record, and Task Plan
- Output: Concept manifests, Synchronizations, and mobile-facing artifacts (plans, specs, component definitions)
- Downstream: External build and deployment tooling consumes CERES artifacts; CERES does not invoke those tools

## Mobile Concepts (Proposed)
Each Concept is represented by a manifest in `concepts/<concept>/manifest.yaml` and owns its files.

- `mobile-app-shell` — app bootstrap, entry points, shell-level structure
- `mobile-navigation` — navigation routes, stacks, and transitions
- `mobile-ui-components` — shared UI building blocks and visual primitives
- `mobile-state-management` — state shape, flows, and state-related constraints
- `mobile-platform-ios` — iOS platform-specific bindings and constraints
- `mobile-platform-android` — Android platform-specific bindings and constraints

## Synchronization Map
All dependencies are explicit and declared in `synchronizations/*.yaml`:

- `mobile-app-shell-to-mobile-navigation`
- `mobile-app-shell-to-mobile-state-management`
- `mobile-app-shell-to-mobile-ui-components`
- `mobile-navigation-to-mobile-state-management`
- `mobile-ui-components-to-mobile-platform-ios`
- `mobile-ui-components-to-mobile-platform-android`

## Mobile Skills (Proposed, Non-Authoritative)
Skills are read-only or pure transforms and must be single-Concept scoped:

- `generate-react-native-component` — transform spec to component scaffold
- `generate-swiftui-view` — transform spec to SwiftUI view scaffold
- `generate-kotlin-compose-screen` — transform spec to Compose screen scaffold
- `analyze-mobile-accessibility` — analyze accessibility risks and gaps
- `analyze-mobile-performance-risks` — analyze performance risk factors

## Mobile Plugins (Advisory Only)
Plugins observe and advise without blocking execution:

- `ios-hig-advisory` — heuristics against iOS HIG
- `android-navigation-warning` — navigation pattern warnings
- `store-policy-risk-hints` — non-blocking policy risk hints

## UI Integration (Read-Only)
Existing UI views may surface:
- Mobile plans and task breakdowns
- Platform-specific splits (iOS vs Android)
- Artifact previews (components, navigation maps)

UI remains read-only and artifact-driven.

## Explicit Prohibitions
- Running emulators
- Building binaries
- Signing apps
- Deploying to app stores
- Introducing mobile-specific execution authority

## Determinism and Governance Preservation
- Concept boundaries and Synchronizations are explicit and validated.
- Skills remain read-only or pure transforms.
- Plugins remain advisory and non-blocking.
- No new execution authority is introduced; governance and arbitration remain unchanged.
