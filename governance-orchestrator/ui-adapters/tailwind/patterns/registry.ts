import { TailwindPattern } from "./types";
import { formSingleColumn } from "./patterns/form.singleColumn";
import { formTwoColumn } from "./patterns/form.twoColumn";
import { tableStandard } from "./patterns/table.standard";
import { pageDashboard } from "./patterns/page.dashboard";

export const tailwindPatterns: TailwindPattern[] = [
  formSingleColumn,
  formTwoColumn,
  tableStandard,
  pageDashboard,
];
