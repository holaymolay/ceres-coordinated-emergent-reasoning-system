import { z } from "zod";

// DRAFT / SHADOW: UIP-0.2 schema is non-blocking and used for shadow validation only.
export const UI_EVENT_V02_SCHEMA_VERSION = "0.2.0";

export const uiEventV02Types = [
  "form.submitted",
  "action.clicked",
  "modal.confirmed",
  "modal.cancelled",
  "table.rowSelected",
] as const;

export type UiEventV02Type = (typeof uiEventV02Types)[number];

export const UiEventV02Schema = z.object({
  id: z.string().uuid(),
  ts: z.string().datetime(),
  uiSessionId: z.string().min(1),
  intentId: z.string().min(1),
  type: z.enum(uiEventV02Types),
  payload: z.record(z.unknown()),
  idempotencyKey: z.string().min(1),
  schemaVersion: z.literal(UI_EVENT_V02_SCHEMA_VERSION),
  actor: z
    .object({
      userId: z.string().optional(),
      roles: z.array(z.string()).optional(),
    })
    .optional(),
});
