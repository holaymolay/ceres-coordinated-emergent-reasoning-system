import { validateUiIntent, UiIntent } from "../intent/intent-schema";
import { GovernanceError } from "./types";

const forbiddenPatterns: Array<{ code: string; label: string; regex: RegExp }> = [
  {
    code: "INTENT_MARKUP_DETECTED",
    label: "Markup",
    regex: /<\s*(div|button|form|input|select|textarea|table|svg)\b/i,
  },
  {
    code: "INTENT_STYLE_DETECTED",
    label: "ClassName",
    regex: /\bclassName\s*=/,
  },
  {
    code: "INTENT_STYLE_DETECTED",
    label: "Inline style",
    regex: /\bstyle\s*=\s*['"]/i,
  },
];

const tailwindPattern = /\b(bg|text|flex|grid|px|py|mx|my|mt|mb|ml|mr|pt|pb|pl|pr|w|h)-[a-z0-9-]+\b/i;
const classAttributePattern = /\bclass(Name)?\s*=/i;

const aestheticKeys = [
  "theme",
  "color",
  "colors",
  "font",
  "typography",
  "gradient",
  "shadow",
  "radius",
];

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const scanForForbidden = (raw: string): GovernanceError[] => {
  const errors = forbiddenPatterns.flatMap((pattern) => {
    if (!pattern.regex.test(raw)) {
      return [];
    }
    return [
      {
        code: pattern.code,
        message: `Forbidden markup or styling detected (${pattern.label}).`,
      },
    ];
  });
  if (classAttributePattern.test(raw) && tailwindPattern.test(raw)) {
    errors.push({
      code: "INTENT_TAILWIND_DETECTED",
      message: "Tailwind classes detected alongside class attributes.",
    });
  }
  return errors;
};

const scanForAestheticKeys = (intent: UiIntent): GovernanceError[] => {
  const metadata = intent.metadata ?? {};
  if (!isRecord(metadata)) {
    return [];
  }
  const violations = Object.keys(metadata).filter((key) =>
    aestheticKeys.includes(key.toLowerCase()),
  );
  if (violations.length === 0) {
    return [];
  }
  return [
    {
      code: "INTENT_AESTHETIC_DETECTED",
      message: `Aesthetic metadata keys detected: ${violations.join(", ")}.`,
      path: "metadata",
    },
  ];
};

export interface IntentValidationResult {
  intent?: UiIntent;
  errors: GovernanceError[];
}

// Enforcement boundary: reject any non-intent output and flag markup or styling tokens.
export const validateIntentOnly = (raw: string): IntentValidationResult => {
  const errors: GovernanceError[] = [];

  errors.push(...scanForForbidden(raw));

  let payload: unknown;
  try {
    payload = JSON.parse(raw);
  } catch (error) {
    return {
      errors: [
        {
          code: "INTENT_PARSE_ERROR",
          message: `Input must be valid JSON: ${(error as Error).message}`,
        },
      ],
    };
  }

  const schemaResult = validateUiIntent(payload);
  if (!schemaResult.ok) {
    schemaResult.errors.forEach((schemaError) => {
      errors.push({
        code: "INTENT_SCHEMA_INVALID",
        message: schemaError.message,
        path: schemaError.path,
      });
    });
    return { errors };
  }

  const intent = schemaResult.value as UiIntent;
  errors.push(...scanForAestheticKeys(intent));

  return { intent, errors };
};
