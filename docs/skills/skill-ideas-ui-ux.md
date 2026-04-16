# Frontend UI/UX Skill Ideas (Brainstorm List)

This is a non-authoritative brainstorming list of potential reusable Skills for frontend UI/UX design work. It is not a spec and does not indicate that any of these Skills exist yet.

Conventions:
- Skill IDs use dot-namespace + snake segments (example: `a11y.contrast_check`).
- Prefer atomic, deterministic, cross-project utilities. Anything needing network/subprocess/filesystem writes must be explicitly gated via `skill.yaml:security.access`.

## Design Systems & Tokens
- `design.tokens_validate` — Validate token schema, naming, and required roles (color/spacing/type).
- `design.tokens_lint` — Enforce conventions (no raw hex in semantic tokens, consistent casing, etc.).
- `design.tokens_merge` — Merge token sets with deterministic precedence rules.
- `design.tokens_diff` — Structured diff of two token versions (added/changed/removed).
- `design.tokens_to_css_vars` — Emit CSS variables from tokens (with prefixing rules).
- `design.tokens_to_scss_vars` — Emit SCSS variable maps from tokens.
- `design.tokens_to_tailwind` — Emit a Tailwind config snippet from tokens (colors, spacing, radii).
- `design.tokens_to_style_dictionary` — Emit Style Dictionary-compatible JSON (offline transform).
- `design.tokens_usage_scan` — Scan repo for hardcoded colors/sizes and report tokenization opportunities.
- `design.tokens_enforce_no_hex` — Fail if non-allowlisted hex colors appear in CSS/JS/TS.
- `design.theme_generate_variants` — Deterministically derive light/dark variants from a base palette (rule-based).
- `design.color_roles_validate` — Ensure required roles exist (bg/fg/primary/secondary/success/warn/error).

## Color & Contrast Utilities (WCAG)
- `a11y.contrast_ratio` — Compute contrast ratio for two colors (hex/rgb/hsl).
- `a11y.contrast_check` — Evaluate contrast against WCAG AA/AAA for text sizes.
- `a11y.palette_contrast_audit` — Audit token palette pairs (bg/fg combos) for pass/fail.
- `design.color_convert` — Convert colors between hex/rgb/hsl/lab with stable rounding rules.
- `design.color_blend` — Blend colors with alpha and output resulting color.
- `design.color_scale_generate` — Generate a deterministic scale (50–900) from a base color.
- `design.colorblind_simulate` — Simulate common color vision deficiencies for a palette (offline algorithmic).

## Typography & Layout
- `typography.scale_generate` — Generate a type scale (modular/steps) and emit CSS variables.
- `typography.fluid_type_clamp` — Generate `clamp()` rules from min/max sizes and breakpoints.
- `typography.line_height_suggest` — Deterministic line-height suggestions from font size categories.
- `typography.font_stack_validate` — Validate font stacks against allowlists and fallback order.
- `layout.spacing_scale_generate` — Generate spacing scale tokens (4px/8px/… or modular).
- `layout.grid_generate` — Generate CSS grid templates (columns/gutters/margins) for breakpoints.
- `layout.breakpoint_validate` — Validate breakpoint ordering, duplicates, and naming.
- `layout.container_query_map` — Emit container query rules for component-level responsiveness.
- `layout.z_index_registry_validate` — Validate a z-index registry (no collisions, documented layers).

## Component API & Consistency (React/TS-aware, but portable)
- `ui.component_inventory` — Index components, props, and usage sites into a JSON catalog.
- `ui.props_extract` — Extract prop names/types/defaults from TS types or PropTypes.
- `ui.props_validate` — Enforce prop naming rules (e.g., `onX` handlers, boolean prefix).
- `ui.component_name_lint` — Validate component naming conventions and file placement.
- `ui.design_system_usage_audit` — Detect direct imports of forbidden components/styles.
- `ui.css_classname_conventions` — Enforce BEM/utility naming rules if used.
- `ui.icon_usage_audit` — Detect non-standard icons or direct SVG embeds.
- `ui.deprecation_scan` — Detect usage of deprecated components/APIs and emit a migration report.

## Accessibility (A11y) Audits (Static + Runtime-gated)
- `a11y.html_semantics_audit` — Static audit of HTML for headings, landmarks, label associations.
- `a11y.aria_attributes_validate` — Validate ARIA attributes/roles against allowlists.
- `a11y.form_labels_audit` — Ensure inputs have labels/aria-label and correct `autocomplete`.
- `a11y.image_alt_audit` — Detect missing/empty alt text where required.
- `a11y.link_purpose_audit` — Flag ambiguous link text (“click here”) via allowlist rules.
- `a11y.focus_styles_audit` — Detect missing focus indicators in CSS (best-effort static analysis).
- `a11y.tabindex_audit` — Flag suspicious tabindex usage (`>0`, focus traps).
- `a11y.reduced_motion_audit` — Check for `prefers-reduced-motion` coverage (CSS/JS).
- `a11y.color_contrast_in_css` — Extract CSS colors and check common text/background combinations.
- `a11y.lighthouse_audit` — Run Lighthouse a11y checks (subprocess/browser-gated) and normalize results.
- `a11y.playwright_axe_audit` — Run axe-core audits via Playwright (subprocess/browser-gated).

## Interaction, Motion, and States
- `ui.state_matrix_generate` — Generate a component state matrix template (default/hover/focus/disabled/loading/error).
- `ui.state_coverage_audit` — Scan for missing state styles (e.g., no disabled styles).
- `motion.token_validate` — Validate motion tokens (durations/easings) and usage.
- `motion.prefers_reduced_motion_enforce` — Ensure animations are disabled/reduced when requested.
- `motion.css_keyframes_lint` — Lint keyframe naming, duplication, and infinite loops.

## Content, UX Copy, and Information Architecture (Deterministic checks)
- `ux.copy_readability` — Compute readability metrics (Flesch-Kincaid) for UI copy bundles.
- `ux.copy_banned_terms` — Enforce banned terms and preferred terminology glossary.
- `ux.copy_length_budget` — Check copy against length budgets (buttons, nav, toasts).
- `ux.i18n_length_expand` — Simulate length expansion (e.g., +30%) to flag layout risk.
- `ux.empty_state_lint` — Validate presence of empty/loading/error states in defined views.
- `ux.navigation_map_validate` — Validate nav structure JSON (no orphan routes, consistent naming).

## Responsive & Cross-Browser QA (Some browser-gated)
- `ui.breakpoint_screenshot_grid` — Capture screenshots across breakpoints (browser-gated) and emit manifest.
- `ui.visual_regression_diff` — Compare screenshots and emit deterministic diff metrics (pixel diff thresholding).
- `ui.layout_shift_audit` — Measure CLS from traces (browser-gated) and normalize output.
- `ui.font_loading_audit` — Detect FOIT/FOUT risks from CSS/font config.
- `ui.browser_support_check` — Check usage of unsupported CSS/JS features against a target matrix.

## Performance & Web Vitals (Mostly tooling-gated)
- `perf.lighthouse_run` — Run Lighthouse with a pinned config and normalize results.
- `perf.bundle_size_report` — Parse bundle analyzer outputs and produce a stable report.
- `perf.image_weight_audit` — Audit image sizes/format usage and flag heavy assets.
- `perf.font_subset_suggest` — Suggest subsetting based on declared character sets (static analysis).
- `perf.cache_headers_validate` — Validate static hosting headers config (if present) for assets.

## CSS & Styling Hygiene
- `css.unused_selectors` — Detect unused selectors (best-effort static; or tooling-gated with build).
- `css.duplicate_rules` — Detect duplicate declarations and opportunities to dedupe.
- `css.variables_audit` — Detect hardcoded values that should be tokens/CSS vars.
- `css.specificity_audit` — Flag overly specific selectors and `!important` usage.
- `css.media_query_audit` — Validate media query consistency and ordering.
- `css.theme_toggle_validate` — Validate theme class/data-attr behavior via static checks.

## Assets (SVG/Images) and UI Resources
- `asset.svg_optimize` — Optimize SVGs (SVGO; subprocess-gated) with deterministic config.
- `asset.svg_lint` — Validate SVG safety rules (no scripts, external refs) and naming conventions.
- `asset.icon_sprite_build` — Build an SVG sprite sheet deterministically from a directory.
- `asset.image_resize_batch` — Resize/compress images to presets (subprocess-gated) with manifest output.
- `asset.image_format_audit` — Flag non-optimal formats (png vs webp/avif) with thresholds.

## Storybook / Docs / Design QA Docs
- `docs.component_md_generate` — Generate component docs skeleton from extracted props.
- `docs.story_scaffold` — Scaffold Storybook stories for components (write-gated; template-driven).
- `docs.story_coverage_audit` — Detect components missing stories.
- `docs.changelog_ui_entry` — Generate UI-focused changelog snippets from explicit inputs.
- `docs.design_system_site_build` — Build a static design system site (tooling-gated) and emit artifact manifest.

## Forms, Validation, and Error UX
- `ux.form_accessibility_audit` — Check label/help/error patterns and ARIA associations.
- `ux.form_validation_copy_lint` — Enforce consistent validation messages and tone.
- `ux.input_type_audit` — Verify correct HTML input types and `autocomplete` attributes.
- `ux.error_toast_lint` — Validate toast/alert usage patterns and dedupe rules.

## i18n / Localization
- `i18n.extract_strings` — Extract translatable strings into locale files (write-gated).
- `i18n.validate_locales` — Validate locale keys across languages (missing/extra).
- `i18n.unused_keys_audit` — Detect unused translation keys.
- `i18n.pseudolocalize` — Deterministically pseudo-localize strings for UI testing.

## Optional Network-Gated / External Integrations (Requires Security Approval)
- `figma.tokens_pull` — Fetch tokens from Figma API (network + env read gated).
- `figma.assets_export` — Export icons/images from Figma (network + write gated).
- `jira.design_ticket_sync` — Sync design QA findings to Jira (network + env read gated).
- `vcs.github_pr_comment_design_qa` — Post summarized design QA results to a PR (network-gated).
