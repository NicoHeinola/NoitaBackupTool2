<script lang="ts" setup>
const settings = defineModel<Record<string, any>>({
  default: {},
});
</script>

<template>
  <v-form>
    <v-row>
      <v-col v-for="(_, key) in settings" :key="key" cols="12">
        <v-text-field v-model="settings[key]" :label="key" />
      </v-col>
    </v-row>
  </v-form>
</template>
