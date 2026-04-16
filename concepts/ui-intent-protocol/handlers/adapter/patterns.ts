import { LayoutPatternId, UiIntent } from "../intent/intent-schema";
import { LayoutPattern } from "./adapter-contract";

export const layoutPatterns: LayoutPattern[] = [
  {
    id: "single-column",
    description: "Single vertical flow for forms and simple pages",
    slots: ["header", "body", "actions"],
  },
  {
    id: "two-column",
    description: "Two-column layout for overview pages with side content",
    slots: ["left", "right"],
  },
  {
    id: "table-with-toolbar",
    description: "Table layout with header and actions area",
    slots: ["header", "table", "actions"],
  },
  {
    id: "modal-centered",
    description: "Centered modal surface with action row",
    slots: ["content", "actions"],
  },
  {
    id: "alert-inline",
    description: "Inline alert banner",
    slots: ["message", "actions"],
  },
  {
    id: "cta-inline",
    description: "Inline call-to-action block",
    slots: ["message", "actions"],
  },
];

export const resolvePattern = (intent: UiIntent): LayoutPatternId => {
  if (intent.layout?.pattern) {
    return intent.layout.pattern;
  }

  switch (intent.type) {
    case "page.create":
      return "two-column";
    case "form.create":
      return "single-column";
    case "table.create":
      return "table-with-toolbar";
    case "modal.open":
      return "modal-centered";
    case "alert.show":
      return "alert-inline";
    case "cta.request":
      return "cta-inline";
    default:
      return "single-column";
  }
};
