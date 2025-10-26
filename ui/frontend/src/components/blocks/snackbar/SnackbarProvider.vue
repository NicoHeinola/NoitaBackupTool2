<script setup lang="ts">
import { ref, provide } from "vue";

const isOpen = ref(false);
const snackbarProps = ref<Record<string, any>>({});
let resolvePromise: ((value: any) => void) | null = null;

const openSnackbar = ({ props }: any) => {
  snackbarProps.value = props || {};
  isOpen.value = true;

  return new Promise((resolve) => {
    resolvePromise = resolve;
  });
};

const handleClose = () => {
  if (resolvePromise) resolvePromise(null);
  resolvePromise = null;
};

provide("openSnackbar", openSnackbar);
</script>

<template>
  <slot></slot>
  <v-snackbar color="success" v-model="isOpen" v-bind="snackbarProps" :timeout="5000" @update:model-value="handleClose">
    <template #actions>
      <v-btn color="white" text @click="isOpen = false">OK</v-btn>
    </template>
  </v-snackbar>
</template>
