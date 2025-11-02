<script lang="ts" setup>
import AppFooter from "./components/modules/app-footer/AppFooter.vue";
</script>

<template>
  <v-app>
    <snackbar-provider>
      <dialog-provider>
        <router-view />
        <app-footer />
      </dialog-provider>
    </snackbar-provider>
  </v-app>
</template>
