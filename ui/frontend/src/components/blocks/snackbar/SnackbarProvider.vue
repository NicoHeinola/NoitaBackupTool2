<script setup lang="ts">
import { ref, provide, nextTick } from "vue";

interface SnackbarItem {
  id: string;
  props: Record<string, any>;
  isOpen: boolean;
  resolve: (value: any) => void;
}

const snackbars = ref<SnackbarItem[]>([]);
let snackbarIdCounter = 0;

const openSnackbar = ({ props }: any) => {
  const id = `snackbar-${++snackbarIdCounter}`;

  return new Promise((resolve) => {
    const snackbarItem: SnackbarItem = {
      id,
      props: props || {},
      isOpen: true,
      resolve
    };

    snackbars.value.push(snackbarItem);

    // Auto-remove after timeout
    const timeout = snackbarItem.props.timeout || 5000;
    if (timeout > 0) {
      setTimeout(() => {
        handleClose(id);
      }, timeout);
    }
  });
};

const handleClose = (id: string) => {
  const index = snackbars.value.findIndex(s => s.id === id);
  if (index !== -1) {
    const snackbar = snackbars.value[index];
    if (snackbar) {
      // Set isOpen to false first to prevent re-triggering
      snackbar.isOpen = false;
      snackbar.resolve(null);
      // Remove after a short delay to allow animation
      setTimeout(() => {
        const currentIndex = snackbars.value.findIndex(s => s.id === id);
        if (currentIndex !== -1) {
          snackbars.value.splice(currentIndex, 1);
        }
      }, 200);
    }
  }
};

provide("openSnackbar", openSnackbar);
</script>

<template>
  <slot></slot>
  <v-snackbar v-for="(snackbar, index) in snackbars" :key="snackbar.id" v-model="snackbar.isOpen"
    v-bind="snackbar.props" :timeout="-1" :style="{ 'margin-bottom': `${index * 70}px` }">
    <template #actions>
      <v-btn :color="snackbar.props.actionColor || 'white'" text @click="handleClose(snackbar.id)">
        {{ snackbar.props.actionText || 'OK' }}
      </v-btn>
    </template>
  </v-snackbar>
</template>
