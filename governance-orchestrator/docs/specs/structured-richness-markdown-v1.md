# Structured Richness Markdown v1
Structured Richness Markdown v1 defines a strict house style for Markdown docs.
It optimizes for fast scanning, predictable structure, and low cognitive load.
The rules are enforceable by tooling and intended for long-lived maintenance.
Apply this spec to every Markdown document created or revised here.

## Document skeleton rules
- Exactly one H1, placed at the top.
- Sentence-case headings only.
- Heading depth limited to H3.
- A required purpose paragraph follows the H1 and spans 3 to 5 lines.
- Sections use H2; subsections use H3.
- Keep section titles specific and action-neutral.

## Paragraph and chunking rules
- One idea per paragraph; no mixed topics.
- Maximum 5 lines per paragraph.
- Insert a blank line between every paragraph and block element.
- Avoid long prose blocks; prefer short, scannable chunks.
- Do not use essay-style sections.

## Allowed rich elements
- Lists with 7 items or fewer.
- Code blocks with a language tag, placed before their explanation.
- Tables used only for comparisons.
- Callouts using NOTE, WARNING, TIP, or EXAMPLE labels.
- One callout per section; no stacked callouts.

## Emphasis rules
- Bold is for semantic emphasis only.
- Italics are rare and secondary.
- Never bold full sentences.
- Avoid emphasis for decoration or tone.

## Visual restraint rules
- No emojis.
- No raw HTML.
- No decorative formatting.
- At most one horizontal rule per document.

## Profiles and applicability
```yaml
---
doc_profile: rich-human
---
```
Use YAML frontmatter to select a profile for a document.
If no profile is declared, default to rich-human.
Valid profiles are rich-human, lean-reference, and strict-ci.
Profiles adjust enforcement without changing the core rules.

## Philosophy
Structured Richness keeps documentation dense with meaning but easy to scan.
It prioritizes comprehension speed, reduces re-reading, and supports maintenance.
The format is strict so tooling can enforce quality without subjective debates.

## Profiles Summary
| Profile | Intended use | Enforcement level | CI behavior |
| --- | --- | --- | --- |
| rich-human | Human-first docs and onboarding | Full rules + Vale | Enforced |
| lean-reference | Specs and reference docs | Structure only | Enforced |
| strict-ci | Public or core docs | Full rules + strict language | Enforced |
| internal-notes | Drafts and scratch notes | Relaxed structure | Skipped by default |
