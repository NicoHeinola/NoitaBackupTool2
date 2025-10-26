<script lang="ts" setup>
const props = withDefaults(
  defineProps<{
    title?: string;
    text?: string;
  }>(),
  {
    title: "Are you sure?",
    text: "This action cannot be undone.",
  }
);

const emit = defineEmits<{
  (e: "resolve", payload: boolean): void;
}>();
</script>

<template>
  <v-card>
    <v-card-title v-if="title">{{ title }} </v-card-title>
    <v-card-text>
      {{ text }}
    </v-card-text>
    <v-card-actions class="d-flex justify-end">
      <v-btn variant="outlined" color="error" @click="emit('resolve', false)">Cancel</v-btn>
      <v-btn variant="elevated" color="success" @click="emit('resolve', true)">OK</v-btn>
    </v-card-actions>
  </v-card>
</template>
