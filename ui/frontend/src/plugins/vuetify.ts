/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import "@mdi/font/css/materialdesignicons.css";
import "vuetify/styles";

// Composables
import { createVuetify } from "vuetify";

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme: "noita",
    themes: {
      noita: {
        dark: true,
        colors: {
          // Primary: Golden/amber magic glow
          primary: "#E6B800",
          "primary-darken-1": "#B8941A",
          "primary-lighten-1": "#F5D142",

          // Secondary: Mystical purple/violet
          secondary: "#8A2BE2",
          "secondary-darken-1": "#6B1FA8",
          "secondary-lighten-1": "#A555E8",

          // Accent: Magical green (like toxic/acid magic)
          accent: "#32CD32",

          // Status colors with magical theme
          error: "#FF4444",
          warning: "#FF8C00",
          info: "#4FC3F7",
          success: "#66BB6A",

          // Dark mystical backgrounds
          background: "#0D0D0D",
          surface: "#1A1A1A",
          "surface-variant": "#2D2D2D",
          "surface-bright": "#3A3A3A",

          // Text colors
          "on-background": "#E0E0E0",
          "on-surface": "#E0E0E0",
          "on-primary": "#000000",
          "on-secondary": "#FFFFFF",

          // Additional magical colors
          "deep-purple": "#4A148C",
          amber: "#FFC107",
          lime: "#8BC34A",
          cyan: "#00BCD4",
        },
      },
      // Keep the original dark theme as an alternative
      dark: {
        dark: true,
        colors: {
          primary: "#FFD600",
          secondary: "#00CAFF",
          error: "#FF1744",
          success: "#00C853",
          surface: "#121212",
          background: "#0A0A0A",
        },
      },
    },
  },
  defaults: {
    VBtn: {
      variant: "elevated",
      color: "primary",
      style: "box-shadow: 0 4px 8px rgba(230, 184, 0, 0.3);",
    },
    VDialog: {
      width: 800,
      scrim: "rgba(0,0,0,0.9)",
      style: "border: 1px solid rgba(138, 43, 226, 0.3);",
    },
    VTooltip: {
      location: "bottom",
      style: "background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%);",
    },
    VCard: {
      style:
        "background: linear-gradient(135deg, #1A1A1A 0%, #2D2D2D 100%); border: 1px solid rgba(138, 43, 226, 0.2);",
    },
    VTextarea: {
      variant: "outlined",
      color: "secondary",
      density: "compact",
    },
    VTextField: {
      variant: "outlined",
      color: "secondary",
      density: "compact",
    },
    VSelect: {
      variant: "outlined",
      color: "secondary",
      density: "compact",
    },
    VFileInput: {
      variant: "outlined",
      color: "secondary",
      density: "compact",
    },
    VAutocomplete: {
      variant: "outlined",
      color: "secondary",
      density: "compact",
    },
    VAppBar: {
      style:
        "background: linear-gradient(90deg, #0D0D0D 0%, #1A1A1A 50%, #0D0D0D 100%);",
    },
    VNavigationDrawer: {
      style: "background: linear-gradient(180deg, #0D0D0D 0%, #1A1A1A 100%);",
    },
  },
});
