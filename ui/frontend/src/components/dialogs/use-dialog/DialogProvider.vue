<script setup lang="ts">
import { ref, provide, markRaw } from "vue";

const isOpen = ref(false);
const dialogComponent = ref<any>(null);
const dialogProps = ref<Record<string, any>>({});
let resolvePromise: ((value: any) => void) | null = null;

const openDialog = ({ component, props }: any) => {
  dialogComponent.value = markRaw(component); // markRaw to avoid making component reactive
  dialogProps.value = props || {};
  isOpen.value = true;

  return new Promise((resolve) => {
    resolvePromise = resolve;
  });
};

const handleClose = () => {
  isOpen.value = false;
  if (resolvePromise) resolvePromise(null);
  resolvePromise = null;
};

const handleResolve = (payload: any) => {
  isOpen.value = false;
  if (resolvePromise) resolvePromise(payload);
  resolvePromise = null;
};

provide("openDialog", openDialog);
</script>

<template>
  <slot></slot>
  <v-dialog v-model="isOpen">
    <component :is="dialogComponent" v-bind="dialogProps" @close="handleClose" @resolve="handleResolve" />
  </v-dialog>
</template>
