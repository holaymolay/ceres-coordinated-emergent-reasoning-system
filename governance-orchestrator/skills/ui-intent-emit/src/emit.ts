import { UiIntentSchema, UiIntentInput, UiIntentOutput } from "./schema";

export const emitUiIntent = (input: UiIntentInput): UiIntentOutput => {
  return UiIntentSchema.parse(input) as UiIntentOutput;
};

export const validateUiIntent = (input: UiIntentInput) => {
  return UiIntentSchema.safeParse(input);
};
