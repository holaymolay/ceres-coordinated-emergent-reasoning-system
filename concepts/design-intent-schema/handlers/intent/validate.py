#!/usr/bin/env python3
import re
from datetime import datetime
from typing import Any, Dict, List

SCHEMA_VERSION = "1.0.0"
ALLOWED_PAGE_GOALS = {"convert", "explain", "operate"}
ALLOWED_AUDIENCE = {"low", "medium", "expert"}
ALLOWED_INTERACTION_DENSITY = {"sparse", "moderate", "dense"}
ALLOWED_EXPRESSIVENESS = {"conservative", "expressive"}
ALLOWED_ACCESSIBILITY_FLOORS = {"wcag-2.1-aa", "wcag-2.2-aa", "section-508"}
MAX_BRAND_TRAITS = 5
INTENT_VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def error(path: str, message: str) -> Dict[str, str]:
    return {"path": path, "message": message}


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and len(value.strip()) > 0


def is_iso8601(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        if value.endswith("Z"):
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        else:
            datetime.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate_design_intent(intent: Any) -> List[Dict[str, str]]:
    errors: List[Dict[str, str]] = []

    if not isinstance(intent, dict):
        return [error("", "intent must be an object")]

    allowed_keys = {
        "schemaVersion",
        "intentId",
        "intentVersion",
        "createdAt",
        "page_goal",
        "audience_sophistication",
        "brand_traits",
        "interaction_density",
        "expressiveness_tolerance",
        "accessibility_floor",
    }
    extra_keys = set(intent.keys()) - allowed_keys
    if extra_keys:
        extras = ", ".join(sorted(extra_keys))
        errors.append(error("", f"unexpected fields: {extras}"))

    if intent.get("schemaVersion") != SCHEMA_VERSION:
        errors.append(error("schemaVersion", "schemaVersion must match the current schema version"))

    if not is_non_empty_string(intent.get("intentId")):
        errors.append(error("intentId", "intentId must be a non-empty string"))

    intent_version = intent.get("intentVersion")
    if not is_non_empty_string(intent_version) or not INTENT_VERSION_PATTERN.match(intent_version):
        errors.append(error("intentVersion", "intentVersion must be a semantic version (e.g., 1.0.0)"))

    if not is_iso8601(intent.get("createdAt")):
        errors.append(error("createdAt", "createdAt must be an ISO-8601 timestamp"))

    page_goal = intent.get("page_goal")
    if not is_non_empty_string(page_goal) or page_goal not in ALLOWED_PAGE_GOALS:
        errors.append(error("page_goal", "page_goal must be convert, explain, or operate"))

    audience = intent.get("audience_sophistication")
    if not is_non_empty_string(audience) or audience not in ALLOWED_AUDIENCE:
        errors.append(error("audience_sophistication", "audience_sophistication must be low, medium, or expert"))

    traits = intent.get("brand_traits")
    if not isinstance(traits, list):
        errors.append(error("brand_traits", "brand_traits must be an array"))
    else:
        if len(traits) == 0:
            errors.append(error("brand_traits", "brand_traits must include at least one value"))
        if len(traits) > MAX_BRAND_TRAITS:
            errors.append(error("brand_traits", f"brand_traits must not exceed {MAX_BRAND_TRAITS} entries"))
        normalized: List[str] = []
        for index, trait in enumerate(traits):
            if not is_non_empty_string(trait):
                errors.append(error(f"brand_traits[{index}]", "brand_traits values must be non-empty strings"))
            else:
                normalized.append(trait.strip())
        if len(set(normalized)) != len(normalized):
            errors.append(error("brand_traits", "brand_traits values must be unique"))

    density = intent.get("interaction_density")
    if not is_non_empty_string(density) or density not in ALLOWED_INTERACTION_DENSITY:
        errors.append(error("interaction_density", "interaction_density must be sparse, moderate, or dense"))

    expressiveness = intent.get("expressiveness_tolerance")
    if not is_non_empty_string(expressiveness) or expressiveness not in ALLOWED_EXPRESSIVENESS:
        errors.append(
            error("expressiveness_tolerance", "expressiveness_tolerance must be conservative or expressive")
        )

    accessibility = intent.get("accessibility_floor")
    if not is_non_empty_string(accessibility) or accessibility not in ALLOWED_ACCESSIBILITY_FLOORS:
        errors.append(
            error(
                "accessibility_floor",
                "accessibility_floor must be wcag-2.1-aa, wcag-2.2-aa, or section-508",
            )
        )

    return errors


def require_design_intent(intent: Any) -> Dict[str, Any]:
    errors = validate_design_intent(intent)
    if errors:
        message = "; ".join(f"{item['path']}: {item['message']}" for item in errors)
        raise ValueError(f"Design intent validation failed: {message}")
    return intent
