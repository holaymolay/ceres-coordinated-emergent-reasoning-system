import { UiIntent } from "../intent/intent-schema";
import { CapabilityContext, DesignCapability, GovernanceError } from "./types";
import { getDefaultPatternByType } from "./capability-validation";

const PRIMARY_INTENTS = new Set(["submit", "confirm"]);
const MAX_FIELDS_PER_GROUP = 18;
const MAX_COLUMNS_PER_TABLE = 12;

const isBaselineCapability = (capability: DesignCapability): boolean =>
  capability === "utility" || capability === "baseline";

// Enforcement boundary: apply baseline constitution checks without stylistic inference.
export const validateConstitution = (
  intent: UiIntent,
  context: CapabilityContext,
): GovernanceError[] => {
  const errors: GovernanceError[] = [];

  const primaryActions = intent.components.actions.filter((action) =>
    PRIMARY_INTENTS.has(action.intent),
  );
  if (primaryActions.length > 1) {
    errors.push({
      code: "CONSTITUTION_PRIMARY_ACTIONS",
      message: "Only one primary action is allowed per intent.",
      path: "components.actions",
    });
  }

  if (intent.type === "form.create" && intent.components.fields.length > MAX_FIELDS_PER_GROUP) {
    errors.push({
      code: "CONSTITUTION_DENSITY_FIELDS",
      message: `Form fields exceed readable density (${MAX_FIELDS_PER_GROUP}).`,
      path: "components.fields",
    });
  }

  if (intent.type === "table.create" && intent.components.columns.length > MAX_COLUMNS_PER_TABLE) {
    errors.push({
      code: "CONSTITUTION_DENSITY_COLUMNS",
      message: `Table columns exceed readable density (${MAX_COLUMNS_PER_TABLE}).`,
      path: "components.columns",
    });
  }

  if (isBaselineCapability(context.capability) && intent.layout?.pattern) {
    const defaultPattern = getDefaultPatternByType(intent);
    if (intent.layout.pattern !== defaultPattern) {
      errors.push({
        code: "CONSTITUTION_PATTERN_OVERRIDE",
        message: "Baseline capability requires the default pattern for this intent.",
        path: "layout.pattern",
      });
    }
  }

  return errors;
};
