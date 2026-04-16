import argparse
import difflib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


class SpecError(Exception):
    pass


class ValidationError(Exception):
    pass


@dataclass
class Section:
    section_id: str
    title: str
    heading_level: int
    required: bool
    source: str
    field: str
    render: str
    intro_key: str | None = None
    title_template: str | None = None


@dataclass
class ReadmeSection:
    title: str
    level: int
    lines: List[str]


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing YAML file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data


def load_sections(path: Path) -> List[Section]:
    data = load_yaml(path)
    raw_sections = data.get("sections")
    if not isinstance(raw_sections, list):
        raise ValueError("sections.yaml must contain a 'sections' list")
    sections: List[Section] = []
    for entry in raw_sections:
        if not isinstance(entry, dict):
            raise ValueError("Each section entry must be a mapping")
        sections.append(
            Section(
                section_id=entry.get("id", ""),
                title=entry.get("title", ""),
                heading_level=int(entry.get("heading_level", 2)),
                required=bool(entry.get("required", False)),
                source=entry.get("source", ""),
                field=entry.get("field", ""),
                render=entry.get("render", ""),
                intro_key=entry.get("intro_key"),
                title_template=entry.get("title_template"),
            )
        )
    return sections


def load_rules(path: Path) -> Dict[str, Any]:
    return load_yaml(path)


def load_tone_profiles(path: Path) -> Dict[str, Any]:
    data = load_yaml(path)
    profiles = data.get("profiles")
    if not isinstance(profiles, dict):
        raise ValueError("tone.yaml must contain a 'profiles' map")
    return profiles


def validate_spec(spec: Dict[str, Any]) -> None:
    required_fields = [
        "project_name",
        "one_sentence_value_prop",
        "audience",
        "problem_statement",
        "solution_summary",
        "outcomes",
        "quick_start",
        "repo_map",
        "non_goals",
        "constraints",
    ]
    errors: List[str] = []
    for field in required_fields:
        if field not in spec:
            errors.append(f"Missing required field: {field}")

    if errors:
        raise SpecError("Spec validation failed:\n- " + "\n- ".join(errors))

    if not isinstance(spec.get("project_name"), str):
        errors.append("project_name must be a string")
    if not isinstance(spec.get("one_sentence_value_prop"), str):
        errors.append("one_sentence_value_prop must be a string")
    if not isinstance(spec.get("problem_statement"), str):
        errors.append("problem_statement must be a string")
    if not isinstance(spec.get("solution_summary"), str):
        errors.append("solution_summary must be a string")

    audience = spec.get("audience")
    if not isinstance(audience, dict):
        errors.append("audience must be a mapping")
    else:
        include = audience.get("include")
        exclude = audience.get("exclude")
        if not isinstance(include, list) or not all(isinstance(item, str) for item in include):
            errors.append("audience.include must be a list of strings")
        if not isinstance(exclude, list) or not all(isinstance(item, str) for item in exclude):
            errors.append("audience.exclude must be a list of strings")

    for list_field in ["outcomes", "quick_start", "non_goals"]:
        value = spec.get(list_field)
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            errors.append(f"{list_field} must be a list of strings")

    repo_map = spec.get("repo_map")
    if not isinstance(repo_map, list):
        errors.append("repo_map must be a list of path/description entries")
    else:
        for entry in repo_map:
            if not isinstance(entry, dict):
                errors.append("repo_map entries must be mappings")
                break
            if not isinstance(entry.get("path"), str) or not isinstance(entry.get("description"), str):
                errors.append("repo_map entries require string path and description")
                break

    constraints = spec.get("constraints")
    if not isinstance(constraints, dict):
        errors.append("constraints must be a mapping")
    else:
        max_length = constraints.get("max_length")
        banned_terms = constraints.get("banned_terms")
        tone_profile = constraints.get("tone_profile")
        if not isinstance(max_length, int):
            errors.append("constraints.max_length must be an integer")
        if not isinstance(banned_terms, list) or not all(isinstance(term, str) for term in banned_terms):
            errors.append("constraints.banned_terms must be a list of strings")
        if not isinstance(tone_profile, str):
            errors.append("constraints.tone_profile must be a string")

    if errors:
        raise SpecError("Spec validation failed:\n- " + "\n- ".join(errors))




def section_heading(level: int, title: str) -> str:
    return f"{'#' * level} {title}".strip()


def get_tone_profile(spec: Dict[str, Any], profiles: Dict[str, Any]) -> Dict[str, Any]:
    tone_profile = spec.get("constraints", {}).get("tone_profile")
    if tone_profile not in profiles:
        raise SpecError(f"Unknown tone_profile: {tone_profile}")
    profile = profiles[tone_profile]
    if not isinstance(profile, dict):
        raise SpecError(f"tone_profile '{tone_profile}' must map to a profile object")
    return profile


def get_section_intro(section: Section, tone_profile: Dict[str, Any]) -> str | None:
    if not section.intro_key:
        return None
    intros = tone_profile.get("section_intros", {})
    if not isinstance(intros, dict):
        return None
    intro = intros.get(section.intro_key)
    if isinstance(intro, str) and intro:
        return intro
    return None


def render_readme(
    spec: Dict[str, Any],
    sections: List[Section],
    rules: Dict[str, Any],
    tone_profiles: Dict[str, Any],
    repo_root: Path,
) -> str:
    validate_spec(spec)
    tone_profile = get_tone_profile(spec, tone_profiles)
    repo_map_rules = rules.get("validation", {}).get("repo_map_table", {})
    exists_values = repo_map_rules.get("exists_values", {"true": "yes", "false": "no"})
    exists_true = exists_values.get("true", "yes")
    exists_false = exists_values.get("false", "no")

    lines: List[str] = []

    for section in sections:
        rendered = []
        if section.render == "title":
            title = section.title_template or "{project_name}"
            rendered.append(section_heading(section.heading_level, title.format(**spec)))
        else:
            rendered.append(section_heading(section.heading_level, section.title))
            rendered.append("")
            intro = get_section_intro(section, tone_profile)
            if intro:
                rendered.append(intro)
                rendered.append("")

            if section.render == "paragraph":
                rendered.append(str(spec.get(section.field, "")).strip())
            elif section.render == "audience":
                audience = spec.get(section.field, {})
                include_label = rules.get("validation", {}).get("audience_labels", {}).get("include", "Include")
                exclude_label = rules.get("validation", {}).get("audience_labels", {}).get("exclude", "Exclude")
                rendered.append(f"**{include_label}**")
                for item in audience.get("include", []):
                    rendered.append(f"- {item}")
                rendered.append("")
                rendered.append(f"**{exclude_label}**")
                for item in audience.get("exclude", []):
                    rendered.append(f"- {item}")
            elif section.render == "list":
                for item in spec.get(section.field, []):
                    rendered.append(f"- {item}")
            elif section.render == "ordered_list":
                for index, item in enumerate(spec.get(section.field, []), start=1):
                    rendered.append(f"{index}. {item}")
            elif section.render == "repo_map_table":
                rendered.append("| Path | Description | Exists |")
                rendered.append("| --- | --- | --- |")
                for entry in spec.get(section.field, []):
                    path = entry.get("path", "")
                    description = entry.get("description", "")
                    exists = (repo_root / path).exists()
                    exists_value = exists_true if exists else exists_false
                    rendered.append(f"| {path} | {description} | {exists_value} |")
            elif section.render == "constraints_list":
                constraints = spec.get(section.field, {})
                labels = rules.get("validation", {}).get("constraints", {}).get("labels", {})
                max_label = labels.get("max_length", "Max length")
                banned_label = labels.get("banned_terms", "Banned terms")
                tone_label = labels.get("tone_profile", "Tone profile")
                max_length = constraints.get("max_length")
                banned_terms = constraints.get("banned_terms", [])
                tone_profile_name = constraints.get("tone_profile")
                banned_text = ", ".join(banned_terms) if banned_terms else "None"
                rendered.append(f"- {max_label}: {max_length} chars")
                rendered.append(f"- {banned_label}: {banned_text}")
                rendered.append(f"- {tone_label}: {tone_profile_name}")
            else:
                raise SpecError(f"Unknown render type: {section.render}")

        if lines:
            lines.append("")
        lines.extend(rendered)

    output = "\n".join(lines).strip() + "\n"
    max_length = spec.get("constraints", {}).get("max_length")
    if isinstance(max_length, int) and len(output) > max_length:
        raise SpecError(f"Generated README length {len(output)} exceeds max_length {max_length}")

    return output


def parse_readme_sections(text: str) -> List[ReadmeSection]:
    sections: List[ReadmeSection] = []
    current: ReadmeSection | None = None
    for line in text.splitlines():
        if line.startswith("#"):
            if current is not None:
                sections.append(current)
            stripped = line.lstrip("#")
            level = len(line) - len(stripped)
            title = stripped.strip()
            current = ReadmeSection(title=title, level=level, lines=[])
        elif current is not None:
            current.lines.append(line)
    if current is not None:
        sections.append(current)
    return sections


def normalize_lines(lines: List[str]) -> List[str]:
    return [line.rstrip() for line in lines if line.strip() != ""]


def extract_bullets(lines: List[str]) -> List[str]:
    items = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def extract_ordered(lines: List[str]) -> List[str]:
    items = []
    for line in lines:
        match = re.match(r"^(\d+)\.\s+(.*)$", line.strip())
        if match:
            items.append(match.group(2).strip())
    return items


def parse_repo_table(lines: List[str]) -> List[List[str]]:
    rows = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        parts = [part.strip() for part in stripped.strip("|").split("|")]
        if len(parts) < 2:
            continue
        if all(part.replace("-", "") == "" for part in parts):
            continue
        rows.append(parts)
    return rows


def validate_readme(
    readme_text: str,
    spec: Dict[str, Any],
    sections: List[Section],
    rules: Dict[str, Any],
    tone_profiles: Dict[str, Any],
    repo_root: Path,
) -> List[str]:
    errors: List[str] = []
    validate_spec(spec)
    tone_profile = get_tone_profile(spec, tone_profiles)

    max_length = spec.get("constraints", {}).get("max_length")
    if isinstance(max_length, int) and len(readme_text) > max_length:
        errors.append(f"README length {len(readme_text)} exceeds max_length {max_length}")

    banned_terms = list(spec.get("constraints", {}).get("banned_terms", []))
    banned_terms += tone_profile.get("disallowed_terms", [])

    term_rules = rules.get("validation", {}).get("term_matching", {})
    case_sensitive = bool(term_rules.get("case_sensitive", False))
    whole_word = bool(term_rules.get("whole_word", False))

    labels = rules.get("validation", {}).get("constraints", {}).get("labels", {})
    banned_label = labels.get("banned_terms", "Banned terms")
    sanitized_text = re.sub(
        rf"^\s*-?\s*{re.escape(banned_label)}:.*$",
        "",
        readme_text,
        flags=re.MULTILINE,
    )
    haystack = sanitized_text if case_sensitive else sanitized_text.lower()
    for term in banned_terms:
        needle = term if case_sensitive else term.lower()
        if not needle:
            continue
        if whole_word:
            pattern = rf"\b{re.escape(needle)}\b"
            if re.search(pattern, haystack):
                errors.append(f"Banned term present: {term}")
        else:
            if needle in haystack:
                errors.append(f"Banned term present: {term}")

    readme_sections = parse_readme_sections(readme_text)
    if not readme_sections:
        errors.append("README contains no headings")
        return errors

    title_section = readme_sections[0]
    title_spec = sections[0]
    expected_title = (title_spec.title_template or "{project_name}").format(**spec)
    if rules.get("validation", {}).get("require_h1", True):
        if title_section.level != rules.get("validation", {}).get("heading_levels", {}).get("title", 1):
            errors.append("README title heading level is incorrect")
    if title_section.title != expected_title:
        errors.append(f"README title does not match project_name: {title_section.title}")

    expected_titles = []
    for section in sections[1:]:
        expected_titles.append(section.title)

    actual_titles = [section.title for section in readme_sections[1:]]
    if rules.get("validation", {}).get("section_order_strict", False):
        if actual_titles != expected_titles:
            errors.append("Section order or titles do not match sections.yaml")

    title_to_section = {section.title: section for section in readme_sections}

    for section in sections[1:]:
        if section.required and section.title not in title_to_section:
            errors.append(f"Missing required section: {section.title}")
            continue
        readme_section = title_to_section.get(section.title)
        if not readme_section:
            continue
        content_lines = normalize_lines(readme_section.lines)
        content_text = "\n".join(content_lines)

        if readme_section.level != section.heading_level:
            errors.append(f"Section heading level mismatch for {section.title}")

        if section.render == "paragraph":
            expected_text = str(spec.get(section.field, "")).strip()
            if expected_text not in content_text:
                errors.append(f"Section '{section.title}' does not include expected paragraph")
        elif section.render == "audience":
            labels = rules.get("validation", {}).get("audience_labels", {})
            include_label = labels.get("include", "Include")
            exclude_label = labels.get("exclude", "Exclude")
            if include_label not in content_text:
                errors.append("Audience section missing Include label")
            if exclude_label not in content_text:
                errors.append("Audience section missing Exclude label")
            for item in spec.get(section.field, {}).get("include", []):
                if item not in content_text:
                    errors.append(f"Audience include item missing: {item}")
            for item in spec.get(section.field, {}).get("exclude", []):
                if item not in content_text:
                    errors.append(f"Audience exclude item missing: {item}")
        elif section.render == "list":
            expected_items = spec.get(section.field, [])
            items = extract_bullets(content_lines)
            if items != expected_items:
                errors.append(f"List items mismatch in section {section.title}")
        elif section.render == "ordered_list":
            expected_items = spec.get(section.field, [])
            items = extract_ordered(content_lines)
            if items != expected_items:
                errors.append(f"Ordered list items mismatch in section {section.title}")
        elif section.render == "repo_map_table":
            rows = parse_repo_table(content_lines)
            if rows:
                header = rows[0]
                columns = rules.get("validation", {}).get("repo_map_table", {}).get("columns", [])
                if header != columns:
                    errors.append("Repository Map table header mismatch")
                body_rows = rows[1:]
            else:
                body_rows = []
            expected = spec.get(section.field, [])
            repo_map_rules = rules.get("validation", {}).get("repo_map_table", {})
            exists_values = repo_map_rules.get("exists_values", {"true": "yes", "false": "no"})
            exists_true = exists_values.get("true", "yes")
            exists_false = exists_values.get("false", "no")
            if len(body_rows) != len(expected):
                errors.append("Repository Map table row count mismatch")
            for row, entry in zip(body_rows, expected):
                if len(row) < 2:
                    errors.append("Repository Map table row malformed")
                    continue
                path = entry.get("path", "")
                description = entry.get("description", "")
                exists = (repo_root / path).exists()
                expected_exists = exists_true if exists else exists_false
                row_path = row[0]
                row_description = row[1]
                row_exists = row[2] if len(row) > 2 else ""
                if row_path != path or row_description != description or row_exists != expected_exists:
                    errors.append(f"Repository Map row mismatch for {path}")
        elif section.render == "constraints_list":
            constraints = spec.get(section.field, {})
            labels = rules.get("validation", {}).get("constraints", {}).get("labels", {})
            max_label = labels.get("max_length", "Max length")
            banned_label = labels.get("banned_terms", "Banned terms")
            tone_label = labels.get("tone_profile", "Tone profile")
            max_length = constraints.get("max_length")
            banned_terms = constraints.get("banned_terms", [])
            tone_profile_name = constraints.get("tone_profile")
            banned_text = ", ".join(banned_terms) if banned_terms else "None"
            expected_lines = [
                f"{max_label}: {max_length} chars",
                f"{banned_label}: {banned_text}",
                f"{tone_label}: {tone_profile_name}",
            ]
            for expected_line in expected_lines:
                if expected_line not in content_text:
                    errors.append(f"Constraints missing line: {expected_line}")
        else:
            errors.append(f"Unsupported render type in validation: {section.render}")

    metadata_rules = rules.get("validation", {}).get("metadata", {})
    if metadata_rules.get("repo_map_paths_must_exist", False):
        ignore = set(metadata_rules.get("metadata_ignore", []))
        for entry in spec.get("repo_map", []):
            path = entry.get("path", "")
            top_level = path.rstrip("/").split("/")[0] if path else ""
            if top_level in ignore:
                continue
            if path and not (repo_root / path).exists():
                errors.append(f"Repo map path does not exist: {path}")

    return errors


def semantic_diff(actual_text: str, expected_text: str) -> str:
    actual_sections = {section.title: section for section in parse_readme_sections(actual_text)}
    expected_sections = {section.title: section for section in parse_readme_sections(expected_text)}

    output: List[str] = ["README Semantic Diff"]

    missing = [title for title in expected_sections if title not in actual_sections]
    extra = [title for title in actual_sections if title not in expected_sections]

    for title in missing:
        output.append(f"- Missing section: {title}")
    for title in extra:
        output.append(f"- Extra section: {title}")

    for title in expected_sections:
        if title not in actual_sections:
            continue
        actual_lines = normalize_lines(actual_sections[title].lines)
        expected_lines = normalize_lines(expected_sections[title].lines)
        if actual_lines != expected_lines:
            output.append(f"- Modified section: {title}")
            diff = difflib.unified_diff(
                actual_lines,
                expected_lines,
                fromfile="actual",
                tofile="expected",
                lineterm="",
            )
            diff_lines = [line for line in diff if line.strip()]
            if diff_lines:
                output.extend(diff_lines)
            else:
                output.append("  (content differs)")

    return "\n".join(output) + "\n"


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", default="README_SPEC.yaml")
    parser.add_argument("--sections", default="spec/sections.yaml")
    parser.add_argument("--rules", default="spec/rules.yaml")
    parser.add_argument("--tone", default="spec/tone.yaml")
    parser.add_argument("--repo-root", default=".")
    return parser
