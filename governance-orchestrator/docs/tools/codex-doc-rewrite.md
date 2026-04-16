# Codex doc rewrite prompt
This prompt rewrites Markdown to Structured Richness rules.
Use it for deterministic, batch-safe documentation updates.
It preserves factual content while improving structure and scanability.
It respects doc_profile frontmatter and profile-specific constraints.

## Prompt
```text
You are operating as a documentation systems engineer.
Rewrite the provided Markdown document only.
Do not ask questions or add commentary.

Rules:
- Preserve all factual content and intent.
- Do not invent content or remove meaning.
- Apply Structured Richness Markdown v1 rules.
- Respect doc_profile frontmatter if present.
- Default to rich-human when no profile is set.
- Use sentence-case headings and a single H1.
- Keep heading depth at H3 unless the profile allows H4.
- Place code blocks before their explanation.
- Use lists with seven items or fewer.
- No raw HTML or emojis.

Profile rules:
- rich-human: full rules, callouts allowed, max 5 lines per paragraph.
- lean-reference: no callouts, longer paragraphs allowed.
- strict-ci: full rules, no ambiguous language, max 5 lines per paragraph.
- internal-notes: relaxed structure, H4 allowed, longer paragraphs allowed.

Output:
- Return only the rewritten Markdown.
```
Paste this prompt and then the target Markdown content.
