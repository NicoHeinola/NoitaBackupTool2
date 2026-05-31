import vuetify from 'eslint-config-vuetify';

const prettierPluginModule = await import('eslint-plugin-prettier');
const prettierPlugin = prettierPluginModule.default ?? prettierPluginModule;
const prettierConfigModule = await import('eslint-config-prettier/flat');
const prettierConfig = prettierConfigModule.default ?? prettierConfigModule;
const config = await vuetify();

export default [
  ...config,
  prettierConfig,
  {
    plugins: { prettier: prettierPlugin },
    rules: {
      'prettier/prettier': 'error',
      '@stylistic/quotes': ['error', 'single', { avoidEscape: true }],
      'vue/padding-line-between-tags': 'off',
      'antfu/top-level-function': 'off',
    },
  },
];
