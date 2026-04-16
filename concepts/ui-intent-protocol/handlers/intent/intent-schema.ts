export const UI_INTENT_SCHEMA_VERSION = "1.0.0" as const;

export type UiIntentType =
  | "page.create"
  | "form.create"
  | "table.create"
  | "modal.open"
  | "alert.show"
  | "cta.request";

export type LayoutPatternId =
  | "single-column"
  | "two-column"
  | "table-with-toolbar"
  | "modal-centered"
  | "alert-inline"
  | "cta-inline";

export type FieldKind =
  | "text"
  | "select"
  | "number"
  | "date"
  | "checkbox"
  | "textarea";

export type ColumnDataType = "text" | "number" | "date" | "status";

export type ActionIntent = "submit" | "confirm" | "cancel" | "navigate" | "dismiss";

export type AlertSeverity = "info" | "warning" | "error" | "success";

export interface UiIntentPurpose {
  summary: string;
  userGoal?: string;
}

export interface UiIntentContent {
  title?: string;
  summary?: string;
  body?: string;
}

export interface InteractionHooks {
  submit?: string;
  confirm?: string;
  cancel?: string;
}

export interface UiIntentLayoutHint {
  pattern?: LayoutPatternId;
}

export interface UiField {
  id: string;
  label: string;
  kind: FieldKind;
  required?: boolean;
  options?: string[];
  placeholder?: string;
  helpText?: string;
}

export interface UiColumn {
  id: string;
  label: string;
  dataType: ColumnDataType;
}

export interface UiAction {
  id: string;
  label: string;
  intent: ActionIntent;
}

export interface UiIntentComponents {
  fields: UiField[];
  columns: UiColumn[];
  actions: UiAction[];
}

export interface PageSection {
  id: string;
  title?: string;
  description?: string;
  componentIds: string[];
}

export interface UiIntentBase {
  id: string;
  type: UiIntentType;
  schemaVersion: typeof UI_INTENT_SCHEMA_VERSION;
  purpose: UiIntentPurpose;
  components: UiIntentComponents;
  hooks?: InteractionHooks;
  layout?: UiIntentLayoutHint;
  content?: UiIntentContent;
  metadata?: Record<string, string>;
}

export interface PageCreateIntent extends UiIntentBase {
  type: "page.create";
  sections: PageSection[];
}

export interface FormCreateIntent extends UiIntentBase {
  type: "form.create";
  formId: string;
  fieldOrder?: string[];
}

export interface TableCreateIntent extends UiIntentBase {
  type: "table.create";
  tableId: string;
  rowKey?: string;
  dataSourceId?: string;
}

export interface ModalOpenIntent extends UiIntentBase {
  type: "modal.open";
  modalId?: string;
}

export interface AlertShowIntent extends UiIntentBase {
  type: "alert.show";
  severity: AlertSeverity;
}

export interface CtaRequestIntent extends UiIntentBase {
  type: "cta.request";
  ctaId?: string;
}

export type UiIntent =
  | PageCreateIntent
  | FormCreateIntent
  | TableCreateIntent
  | ModalOpenIntent
  | AlertShowIntent
  | CtaRequestIntent;

export type ValidatedUiIntent = UiIntent & { readonly __validated: true };

export interface ValidationError {
  path: string;
  message: string;
}

export interface ValidationResult {
  ok: boolean;
  errors: ValidationError[];
  value?: ValidatedUiIntent;
}

const allowedIntentTypes: UiIntentType[] = [
  "page.create",
  "form.create",
  "table.create",
  "modal.open",
  "alert.show",
  "cta.request",
];

const allowedSeverities: AlertSeverity[] = ["info", "warning", "error", "success"];

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);

const isNonEmptyString = (value: unknown): value is string =>
  typeof value === "string" && value.trim().length > 0;

const isStringArray = (value: unknown): value is string[] =>
  Array.isArray(value) && value.every((item) => typeof item === "string");

const pushError = (errors: ValidationError[], path: string, message: string) => {
  errors.push({ path, message });
};

export const validateUiIntent = (intent: unknown): ValidationResult => {
  const errors: ValidationError[] = [];

  if (!isRecord(intent)) {
    return { ok: false, errors: [{ path: "", message: "Intent must be an object" }] };
  }

  if (intent.schemaVersion !== UI_INTENT_SCHEMA_VERSION) {
    pushError(errors, "schemaVersion", "Unsupported or missing schemaVersion");
  }

  if (!isNonEmptyString(intent.id)) {
    pushError(errors, "id", "id must be a non-empty string");
  }

  if (!isNonEmptyString(intent.type) || !allowedIntentTypes.includes(intent.type as UiIntentType)) {
    pushError(errors, "type", "type must be a supported intent type");
  }

  if (!isRecord(intent.purpose) || !isNonEmptyString(intent.purpose.summary)) {
    pushError(errors, "purpose.summary", "purpose.summary must be a non-empty string");
  }

  if (!isRecord(intent.components)) {
    pushError(errors, "components", "components must be an object with fields, columns, and actions");
  } else {
    if (!Array.isArray(intent.components.fields)) {
      pushError(errors, "components.fields", "fields must be an array");
    }
    if (!Array.isArray(intent.components.columns)) {
      pushError(errors, "components.columns", "columns must be an array");
    }
    if (!Array.isArray(intent.components.actions)) {
      pushError(errors, "components.actions", "actions must be an array");
    }
  }

  const type = intent.type as UiIntentType | undefined;

  if (type === "page.create") {
    if (!Array.isArray(intent.sections) || intent.sections.length === 0) {
      pushError(errors, "sections", "sections must be a non-empty array");
    }
  }

  if (type === "form.create") {
    if (!isNonEmptyString(intent.formId)) {
      pushError(errors, "formId", "formId must be a non-empty string");
    }
    if (isRecord(intent.components) && Array.isArray(intent.components.fields)) {
      if (intent.components.fields.length === 0) {
        pushError(errors, "components.fields", "form intents must include at least one field");
      }
    }
  }

  if (type === "table.create") {
    if (!isNonEmptyString(intent.tableId)) {
      pushError(errors, "tableId", "tableId must be a non-empty string");
    }
    if (isRecord(intent.components) && Array.isArray(intent.components.columns)) {
      if (intent.components.columns.length === 0) {
        pushError(errors, "components.columns", "table intents must include at least one column");
      }
    }
  }

  if (type === "modal.open") {
    if (!isRecord(intent.content) || !isNonEmptyString(intent.content.title)) {
      pushError(errors, "content.title", "modal intents require content.title");
    }
    if (!isRecord(intent.content) || !isNonEmptyString(intent.content.body)) {
      pushError(errors, "content.body", "modal intents require content.body");
    }
  }

  if (type === "alert.show") {
    if (!isNonEmptyString(intent.severity) || !allowedSeverities.includes(intent.severity as AlertSeverity)) {
      pushError(errors, "severity", "severity must be info, warning, error, or success");
    }
    if (!isRecord(intent.content) || !isNonEmptyString(intent.content.body)) {
      pushError(errors, "content.body", "alert intents require content.body");
    }
  }

  if (type === "cta.request") {
    if (!isRecord(intent.content) || !isNonEmptyString(intent.content.body)) {
      pushError(errors, "content.body", "cta intents require content.body");
    }
    if (isRecord(intent.components) && Array.isArray(intent.components.actions)) {
      if (intent.components.actions.length === 0) {
        pushError(errors, "components.actions", "cta intents must include at least one action");
      }
    }
  }

  if (errors.length > 0) {
    return { ok: false, errors };
  }

  return { ok: true, errors: [], value: intent as ValidatedUiIntent };
};

export const assertValidUiIntent = (intent: unknown): ValidatedUiIntent => {
  const result = validateUiIntent(intent);
  if (!result.ok || !result.value) {
    const message = result.errors.map((error) => `${error.path}: ${error.message}`).join("; ");
    throw new Error(`UI intent validation failed: ${message}`);
  }
  return result.value;
};

export const isUiIntent = (intent: unknown): intent is UiIntent => validateUiIntent(intent).ok;

export const collectComponentIds = (components: UiIntentComponents): string[] => {
  const fieldIds = components.fields.map((field) => field.id);
  const columnIds = components.columns.map((column) => column.id);
  const actionIds = components.actions.map((action) => action.id);
  return [...fieldIds, ...columnIds, ...actionIds];
};

export const normalizeFieldOrder = (intent: FormCreateIntent): string[] => {
  if (intent.fieldOrder && intent.fieldOrder.length > 0) {
    return intent.fieldOrder;
  }
  return intent.components.fields.map((field) => field.id);
};

export const normalizeTableColumns = (intent: TableCreateIntent): string[] => {
  return intent.components.columns.map((column) => column.id);
};

export const normalizeSectionComponentIds = (section: PageSection): string[] => {
  if (!isStringArray(section.componentIds)) {
    return [];
  }
  return section.componentIds;
};
