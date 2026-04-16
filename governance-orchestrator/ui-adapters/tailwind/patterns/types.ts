import { UiIntent } from "../../../skills/ui-intent-emit/src/types";

export interface TailwindPatternTokens {
  layouts: Record<string, string>;
  components: {
    container: string;
    section: string;
    actionsRow: string;
    field: {
      wrapper: string;
      label: string;
      control: string;
      helper: string;
    };
    table: {
      wrapper: string;
      base: string;
      headerCell: string;
      bodyCell: string;
    };
    action: {
      base: string;
      emphasis: Record<string, string>;
    };
  };
}

export interface PatternRenderContext {
  tokens: TailwindPatternTokens;
}

export interface TailwindPattern {
  patternId: string;
  match: (intent: UiIntent) => boolean;
  rank: (intent: UiIntent) => number;
  render: (intent: UiIntent, ctx: PatternRenderContext) => JSX.Element;
}
