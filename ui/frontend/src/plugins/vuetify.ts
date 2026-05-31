/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Composables
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

// Styles
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        dark: true,
        colors: {
          primary: '#FFD700',
          secondary: '#9C27B0',
        },
      },
    },
  },
  defaults: {
    VBtn: {
      color: 'primary',
      variant: 'flat',
    },
    VTextField: {
      variant: 'outlined',
      color: 'primary',
      density: 'compact',
      hideDetails: 'auto',
    },
    VTextarea: {
      variant: 'outlined',
      color: 'primary',
      density: 'compact',
      hideDetails: 'auto',
    },
    VDialog: {
      width: '800',
    },
    VTooltip: {
      maxWidth: '400',
      location: 'bottom',
    },
  },
});
