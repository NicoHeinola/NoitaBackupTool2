<script lang="ts" setup>
import AppBackground from "./components/modules/app-background/AppBackground.vue";
import AppFooter from "./components/modules/app-footer/AppFooter.vue";
</script>

<template>
  <v-app>
    <snackbar-provider>
      <dialog-provider>
        <router-view style="z-index: 5" />
        <app-footer />
        <app-background />
      </dialog-provider>
    </snackbar-provider>
  </v-app>
</template>
