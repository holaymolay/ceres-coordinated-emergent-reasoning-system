import {
  LayoutPatternId,
  UiAction,
  UiColumn,
  UiField,
  UiIntent,
  ValidatedUiIntent,
} from "../intent/intent-schema";

export type SpacingToken = "xs" | "sm" | "md" | "lg";
export type EmphasisToken = "primary" | "secondary" | "danger";
export type DensityToken = "compact" | "comfortable";

export interface TailwindTokenSet {
  spacing: Record<SpacingToken, string>;
  emphasis: Record<EmphasisToken, string>;
  density: Record<DensityToken, string>;
}

export interface TailwindComponentTokens {
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
    emphasis: Record<EmphasisToken, string>;
  };
  alert: {
    base: string;
  };
  cta: {
    base: string;
    actions: string;
  };
  modal: {
    container: string;
    content: string;
    actions: string;
  };
}

export interface TailwindAdapterTokens extends TailwindTokenSet {
  layouts: Record<LayoutPatternId, string>;
  components: TailwindComponentTokens;
}

export interface LayoutPattern {
  id: LayoutPatternId;
  description: string;
  slots: string[];
}

export type PatternResolver = (intent: UiIntent) => LayoutPatternId;

export interface ComponentMapping<RenderedNode> {
  field: (field: UiField, tokens: TailwindAdapterTokens) => RenderedNode;
  columnHeader: (column: UiColumn, tokens: TailwindAdapterTokens) => RenderedNode;
  action: (action: UiAction, tokens: TailwindAdapterTokens) => RenderedNode;
}

export interface TailwindAdapter<RenderedNode> {
  id: string;
  version: string;
  tokens: TailwindAdapterTokens;
  patterns: LayoutPattern[];
  resolvePattern: PatternResolver;
  componentMapping: ComponentMapping<RenderedNode>;
  render: (intent: ValidatedUiIntent) => RenderedNode;
}
