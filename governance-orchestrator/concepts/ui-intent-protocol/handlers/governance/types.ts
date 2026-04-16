import { LayoutPatternId } from "../intent/intent-schema";

export type DesignCapability = "utility" | "baseline" | "expressive" | "custom";

export interface GovernanceError {
  code: string;
  message: string;
  path?: string;
}

export interface CapabilityContext {
  capability: DesignCapability;
  pattern: LayoutPatternId;
}

export const CAPABILITY_ORDER: DesignCapability[] = [
  "utility",
  "baseline",
  "expressive",
  "custom",
];

export const compareCapability = (current: DesignCapability, required: DesignCapability): boolean => {
  return CAPABILITY_ORDER.indexOf(current) >= CAPABILITY_ORDER.indexOf(required);
};
