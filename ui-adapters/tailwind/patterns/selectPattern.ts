import { UiIntent } from "../../../skills/ui-intent-emit/src/types";
import { TailwindPattern } from "./types";

export const selectPattern = (
  intent: UiIntent,
  patterns: TailwindPattern[]
): TailwindPattern | null => {
  const candidates = patterns.filter((pattern) => pattern.match(intent));
  if (candidates.length === 0) {
    return null;
  }

  const ranked = candidates
    .map((pattern) => ({ pattern, score: pattern.rank(intent) }))
    .sort((a, b) => {
      if (b.score !== a.score) {
        return b.score - a.score;
      }
      return a.pattern.patternId.localeCompare(b.pattern.patternId);
    });

  return ranked[0].pattern;
};
