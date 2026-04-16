import { z } from "zod";

export const uiEventTypes = [
  "form.submitted",
  "action.clicked",
  "modal.confirmed",
  "modal.cancelled",
  "table.rowSelected",
] as const;

export type UiEventType = (typeof uiEventTypes)[number];

export const UI_EVENT_SCHEMA_VERSION = "1.0.0";

export interface UiEventActor {
  userId?: string;
  roles?: string[];
}

export interface UiEvent {
  id: string;
  ts: string;
  uiSessionId: string;
  intentId: string;
  type: UiEventType;
  payload: Record<string, unknown>;
  idempotencyKey: string;
  schemaVersion: string;
  actor?: UiEventActor;
}

export const UiEventSchema = z.object({
  id: z.string().uuid(),
  ts: z.string().datetime(),
  uiSessionId: z.string().min(1),
  intentId: z.string().min(1),
  type: z.enum(uiEventTypes),
  payload: z.record(z.unknown()),
  idempotencyKey: z.string().min(1),
  schemaVersion: z.string().min(1),
  actor: z
    .object({
      userId: z.string().optional(),
      roles: z.array(z.string()).optional(),
    })
    .optional(),
});
