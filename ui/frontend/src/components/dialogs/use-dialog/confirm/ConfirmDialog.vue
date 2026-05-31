<script lang="ts" setup>
const props = withDefaults(
  defineProps<{
    title?: string;
    text?: string;
    cancelText?: string;
    cancelColor?: string;
    confirmText?: string;
    confirmColor?: string;
  }>(),
  {
    title: 'Are you sure?',
    text: 'This action cannot be undone.',
    cancelText: 'Cancel',
    confirmText: 'OK',
    cancelColor: 'error',
    confirmColor: 'success',
  },
);

const splitText = computed(() => {
  return props.text?.split('\n') || [];
});

const emit = defineEmits<{
  (e: 'resolve', payload: boolean): void;
}>();
</script>

<template>
  <v-card>
    <v-card-title v-if="title">{{ title }} </v-card-title>
    <v-card-text>
      <p v-for="(line, index) in splitText" :key="index">{{ line }}</p>
    </v-card-text>
    <v-card-actions class="d-flex justify-end">
      <v-btn
        :color="cancelColor"
        variant="outlined"
        @click="emit('resolve', false)"
      >
        {{ cancelText }}
      </v-btn>
      <v-btn
        :color="confirmColor"
        variant="elevated"
        @click="emit('resolve', true)"
      >
        {{ confirmText }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
