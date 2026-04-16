"use strict";

module.exports = [
  {
    names: ["structured-richness-heading-depth", "SR001"],
    description: "Headings must not exceed H3.",
    tags: ["headings"],
    function: function SR001(params, onError) {
      params.tokens
        .filter((token) => token.type === "heading_open")
        .forEach((token) => {
          const level = Number(token.tag.slice(1));
          if (level > 3) {
            onError({
              lineNumber: token.lineNumber,
              detail: `Found H${level}; max is H3.`
            });
          }
        });
    }
  }
];
