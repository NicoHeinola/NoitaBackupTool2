<script lang="ts" setup>
withDefaults(
  defineProps<{
    text: string;
    icon?: string;
  }>(),
  {
    icon: "mdi-information",
  }
);
</script>

<template>
  <v-tooltip>
    <template #activator="{ props }">
      <v-icon v-bind="props">
        {{ icon }}
      </v-icon>
    </template>
    <template #default>
      <span>{{ text }}</span>
    </template>
  </v-tooltip>
</template>
