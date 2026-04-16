import { createRoot } from "react-dom/client";
import { assertValidUiIntent } from "../intent/intent-schema";
import { tailwindAdapter } from "../adapter/tailwind-adapter";
import exampleIntent from "./example-intent.json";

// Reference flow: validate intent -> render via adapter (JSX remains inside adapter only).

const validatedIntent = assertValidUiIntent(exampleIntent);
const uiElement = tailwindAdapter.render(validatedIntent);

const mountNode = document.getElementById("root");
if (mountNode) {
  const root = createRoot(mountNode);
  root.render(uiElement);
}
