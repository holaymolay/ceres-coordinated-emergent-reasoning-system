import {
  UI_INTENT_SCHEMA_VERSION,
  AlertShowIntent,
  CtaRequestIntent,
  FormCreateIntent,
  ModalOpenIntent,
  PageCreateIntent,
  TableCreateIntent,
  UiIntent,
} from "./intent-schema";

export const pageCreateExample: PageCreateIntent = {
  id: "intent-page-create-001",
  type: "page.create",
  schemaVersion: UI_INTENT_SCHEMA_VERSION,
  purpose: {
    summary: "Introduce the onboarding flow",
    userGoal: "Understand the next step",
  },
  content: {
    title: "Welcome",
    summary: "Start the setup flow",
  },
  components: {
    fields: [],
    columns: [],
    actions: [{ id: "cta-start", label: "Start onboarding", intent: "navigate" }],
  },
  sections: [{ id: "hero", title: "Getting started", componentIds: ["cta-start"] }],
};

export const formCreateExample: FormCreateIntent = {
  id: "intent-form-create-001",
  type: "form.create",
  schemaVersion: UI_INTENT_SCHEMA_VERSION,
  purpose: {
    summary: "Collect basic profile information",
    userGoal: "Create a profile",
  },
  content: {
    title: "Create profile",
    summary: "Enter the essentials",
  },
  formId: "profile-create",
  components: {
    fields: [
      { id: "first_name", label: "First name", kind: "text", required: true },
      { id: "role", label: "Role", kind: "select", options: ["Designer", "Engineer"] },
    ],
    columns: [],
    actions: [
      { id: "submit", label: "Create profile", intent: "submit" },
      { id: "cancel", label: "Cancel", intent: "cancel" },
    ],
  },
  hooks: {
    submit: "profile.create",
    cancel: "profile.cancel",
  },
};

export const tableCreateExample: TableCreateIntent = {
  id: "intent-table-create-001",
  type: "table.create",
  schemaVersion: UI_INTENT_SCHEMA_VERSION,
  purpose: {
    summary: "Review recent activity",
    userGoal: "Scan the latest updates",
  },
  content: {
    title: "Recent activity",
  },
  tableId: "activity-table",
  rowKey: "activity_id",
  components: {
    fields: [],
    columns: [
      { id: "timestamp", label: "Timestamp", dataType: "date" },
      { id: "activity", label: "Activity", dataType: "text" },
      { id: "status", label: "Status", dataType: "status" },
    ],
    actions: [],
  },
};

export const modalOpenExample: ModalOpenIntent = {
  id: "intent-modal-open-001",
  type: "modal.open",
  schemaVersion: UI_INTENT_SCHEMA_VERSION,
  purpose: {
    summary: "Confirm a destructive action",
    userGoal: "Avoid accidental deletion",
  },
  content: {
    title: "Delete profile",
    body: "This action cannot be undone.",
  },
  components: {
    fields: [],
    columns: [],
    actions: [
      { id: "confirm", label: "Delete", intent: "confirm" },
      { id: "cancel", label: "Cancel", intent: "cancel" },
    ],
  },
  hooks: {
    confirm: "profile.delete",
    cancel: "profile.delete.cancel",
  },
};

export const alertShowExample: AlertShowIntent = {
  id: "intent-alert-show-001",
  type: "alert.show",
  schemaVersion: UI_INTENT_SCHEMA_VERSION,
  purpose: {
    summary: "Notify the user of a failure",
    userGoal: "Understand what went wrong",
  },
  content: {
    body: "We could not save your changes. Please retry.",
  },
  severity: "error",
  components: {
    fields: [],
    columns: [],
    actions: [],
  },
};

export const ctaRequestExample: CtaRequestIntent = {
  id: "intent-cta-request-001",
  type: "cta.request",
  schemaVersion: UI_INTENT_SCHEMA_VERSION,
  purpose: {
    summary: "Prompt the user to upgrade",
    userGoal: "Unlock premium features",
  },
  content: {
    body: "Upgrade to unlock team analytics.",
  },
  components: {
    fields: [],
    columns: [],
    actions: [{ id: "upgrade", label: "Upgrade now", intent: "navigate" }],
  },
};

export const exampleIntents: UiIntent[] = [
  pageCreateExample,
  formCreateExample,
  tableCreateExample,
  modalOpenExample,
  alertShowExample,
  ctaRequestExample,
];
