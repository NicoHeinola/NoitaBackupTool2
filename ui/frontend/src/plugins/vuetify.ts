/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
// @ts-ignore
import "@mdi/font/css/materialdesignicons.css";
// @ts-ignore
import "vuetify/styles";

// Composables
import { createVuetify } from "vuetify";

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: "dark",
    themes: {
      dark: {
        dark: true,
        colors: {
          primary: "#FFD700",
          secondary: "#9C27B0",
          accent: "#2196F3",
        },
      },
    },
  },
  defaults: {
    VBtn: {
      color: "primary",
      variant: "flat",
    },
    VTextField: {
      variant: "outlined",
      color: "primary",
      density: "compact",
    },
    VTextarea: {
      variant: "outlined",
      color: "primary",
      density: "compact",
    },
    VDialog: {
      width: "800",
    },
  },
});
