import { z } from "zod";

// DRAFT / SHADOW: UIP-0.2 schema is non-blocking and used for shadow validation only.
export const UI_INTENT_V02_SCHEMA_VERSION = "0.2.0";

const fieldKind = z.enum(["text", "select", "number", "date", "checkbox", "textarea"]);
const columnDataType = z.enum(["text", "number", "date", "status"]);
const actionIntent = z.enum(["submit", "confirm", "cancel", "navigate", "dismiss"]);
const alertSeverity = z.enum(["info", "warning", "error", "success"]);
const uiIntentType = z.enum([
  "page.create",
  "form.create",
  "table.create",
  "modal.open",
  "alert.show",
  "cta.request",
]);

export const UiIntentV02Schema = z
  .object({
    id: z.string().min(1),
    type: uiIntentType,
    schemaVersion: z.literal(UI_INTENT_V02_SCHEMA_VERSION),
    purpose: z.object({
      summary: z.string().min(1),
      userGoal: z.string().optional(),
    }),
    content: z
      .object({
        title: z.string().optional(),
        summary: z.string().optional(),
        body: z.string().optional(),
      })
      .optional(),
    payload: z.record(z.unknown()),
    components: z.object({
      fields: z
        .array(
          z.object({
            id: z.string().min(1),
            label: z.string().min(1),
            kind: fieldKind,
            required: z.boolean().optional(),
            options: z.array(z.string()).optional(),
            placeholder: z.string().optional(),
            helpText: z.string().optional(),
          })
        )
        .default([]),
      columns: z
        .array(
          z.object({
            id: z.string().min(1),
            label: z.string().min(1),
            dataType: columnDataType,
          })
        )
        .default([]),
      actions: z
        .array(
          z.object({
            id: z.string().min(1),
            label: z.string().min(1),
            intent: actionIntent,
          })
        )
        .default([]),
    }),
    hooks: z
      .object({
        submit: z.string().optional(),
        confirm: z.string().optional(),
        cancel: z.string().optional(),
      })
      .optional(),
    layout: z
      .object({
        pattern: z.string().optional(),
      })
      .optional(),
    metadata: z.record(z.string()).optional(),
    sections: z
      .array(
        z.object({
          id: z.string().min(1),
          title: z.string().optional(),
          description: z.string().optional(),
          componentIds: z.array(z.string()),
        })
      )
      .optional(),
    formId: z.string().optional(),
    fieldOrder: z.array(z.string()).optional(),
    tableId: z.string().optional(),
    rowKey: z.string().optional(),
    dataSourceId: z.string().optional(),
    modalId: z.string().optional(),
    severity: alertSeverity.optional(),
    ctaId: z.string().optional(),
  })
  .superRefine((intent, ctx) => {
    if (intent.type === "page.create" && (!intent.sections || intent.sections.length === 0)) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, message: "sections required" });
    }
    if (intent.type === "form.create" && !intent.formId) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, message: "formId required" });
    }
    if (intent.type === "table.create" && !intent.tableId) {
      ctx.addIssue({ code: z.ZodIssueCode.custom, message: "tableId required" });
    }
    if (intent.type === "modal.open") {
      if (!intent.content?.title || !intent.content?.body) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "modal content required" });
      }
    }
    if (intent.type === "alert.show") {
      if (!intent.severity) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "severity required" });
      }
      if (!intent.content?.body) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "alert body required" });
      }
    }
    if (intent.type === "cta.request") {
      if (!intent.content?.body) {
        ctx.addIssue({ code: z.ZodIssueCode.custom, message: "cta body required" });
      }
    }
  });
