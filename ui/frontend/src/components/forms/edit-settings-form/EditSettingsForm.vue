<script lang="ts" setup>
const settings = defineModel<Record<string, any>>({
  default: {},
});
</script>

<template>
  <v-form>
    <v-row>
      <v-col cols="12" v-for="(_, key) in settings" :key="key">
        <v-text-field hide-details :label="key" v-model="settings[key]" />
      </v-col>
    </v-row>
  </v-form>
</template>
