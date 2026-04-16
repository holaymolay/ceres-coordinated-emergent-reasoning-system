import js from '@eslint/js';
import globals from 'globals';

export default [
  {
    ignores: ['node_modules/**', 'coverage/**', 'ai_workflow_revisions/**', 'runs/**/*.jsonl', 'scripts/markdownlint/**']
  },
  {
    files: ['scripts/validate-patterns.js', 'tests/**/*.js'],
    languageOptions: {
      sourceType: 'module',
      ecmaVersion: 'latest',
      globals: {
        ...globals.node,
        URL: 'readonly'
      }
    },
    rules: {
      ...js.configs.recommended.rules,
      'no-console': 'off',
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }]
    }
  }
];
