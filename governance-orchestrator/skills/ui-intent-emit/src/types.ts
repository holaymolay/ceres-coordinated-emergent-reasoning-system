export const UI_INTENT_SCHEMA_VERSION = "1.0.0" as const;

export type UiIntentType =
  | "page.create"
  | "form.create"
  | "table.create"
  | "modal.open"
  | "alert.show"
  | "cta.request";

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
  pattern?: string;
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
