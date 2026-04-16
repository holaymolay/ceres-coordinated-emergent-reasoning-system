"use strict";

module.exports = [
  {
    names: ["structured-richness-heading-depth-h4", "SR002"],
    description: "Headings must not exceed H4.",
    tags: ["headings"],
    function: function SR002(params, onError) {
      params.tokens
        .filter((token) => token.type === "heading_open")
        .forEach((token) => {
          const level = Number(token.tag.slice(1));
          if (level > 4) {
            onError({
              lineNumber: token.lineNumber,
              detail: `Found H${level}; max is H4.`
            });
          }
        });
    }
  }
];
