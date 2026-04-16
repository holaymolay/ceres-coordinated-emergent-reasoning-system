import { LayoutPatternId, UiIntent } from "../intent/intent-schema";
import { resolvePattern } from "../adapter/patterns";
import { CapabilityContext, compareCapability, DesignCapability, GovernanceError } from "./types";

const allowedCapabilities: DesignCapability[] = [
  "utility",
  "baseline",
  "expressive",
  "custom",
];

const patternMinCapability: Record<LayoutPatternId, DesignCapability> = {
  "single-column": "utility",
  "two-column": "baseline",
  "table-with-toolbar": "baseline",
  "modal-centered": "baseline",
  "alert-inline": "utility",
  "cta-inline": "utility",
};

const extractCapability = (intent: UiIntent): string | undefined => {
  const metadata = intent.metadata ?? {};
  if (typeof metadata !== "object" || metadata === null) {
    return undefined;
  }
  return (
    (metadata as Record<string, string>).designCapability ||
    (metadata as Record<string, string>).capability ||
    (metadata as Record<string, string>).design_capability
  );
};

// Enforcement boundary: capability must be valid and patterns must respect minimum levels.
export const validateCapability = (
  intent: UiIntent,
  override?: string,
): { context?: CapabilityContext; errors: GovernanceError[] } => {
  const errors: GovernanceError[] = [];
  const rawCapability = override ?? extractCapability(intent) ?? "baseline";
  if (!allowedCapabilities.includes(rawCapability as DesignCapability)) {
    errors.push({
      code: "CAPABILITY_INVALID",
      message: "Capability must be utility, baseline, expressive, or custom.",
      path: "metadata.designCapability",
    });
    return { errors };
  }

  const capability = rawCapability as DesignCapability;
  const pattern = resolvePattern(intent);
  const required = patternMinCapability[pattern];

  if (!required) {
    if (capability !== "custom") {
      errors.push({
        code: "PATTERN_UNKNOWN",
        message: `Pattern '${pattern}' is not registered for this capability.`,
        path: "layout.pattern",
      });
    }
    return { errors: errors.length ? errors : [], context: { capability, pattern } };
  }

  if (!compareCapability(capability, required)) {
    errors.push({
      code: "CAPABILITY_PATTERN_MISMATCH",
      message: `Pattern '${pattern}' requires capability '${required}'.`,
      path: "layout.pattern",
    });
  }

  return { context: { capability, pattern }, errors };
};

export const getDefaultPatternByType = (intent: UiIntent): LayoutPatternId => {
  switch (intent.type) {
    case "page.create":
      return "two-column";
    case "form.create":
      return "single-column";
    case "table.create":
      return "table-with-toolbar";
    case "modal.open":
      return "modal-centered";
    case "alert.show":
      return "alert-inline";
    case "cta.request":
      return "cta-inline";
    default:
      return "single-column";
  }
};
