<script setup lang="ts">
import { ref, provide, markRaw } from "vue";

interface DialogItem {
  id: string;
  component: any;
  props: Record<string, any>;
  isOpen: boolean;
  resolve: (value: any) => void;
}

const dialogs = ref<DialogItem[]>([]);
let dialogIdCounter = 0;

const openDialog = ({ component, props }: any) => {
  const id = `dialog-${++dialogIdCounter}`;

  return new Promise((resolve) => {
    const dialogItem: DialogItem = {
      id,
      component: markRaw(component), // markRaw to avoid making component reactive
      props: props || {},
      isOpen: true,
      resolve,
    };

    dialogs.value.push(dialogItem);
  });
};

const handleClose = (id: string) => {
  const index = dialogs.value.findIndex((d) => d.id === id);
  if (index !== -1) {
    const dialog = dialogs.value[index];
    if (dialog) {
      // Set isOpen to false first to prevent re-triggering
      dialog.isOpen = false;
      dialog.resolve(null);
      // Remove after a short delay to allow animation
      setTimeout(() => {
        const currentIndex = dialogs.value.findIndex((d) => d.id === id);
        if (currentIndex !== -1) {
          dialogs.value.splice(currentIndex, 1);
        }
      }, 200);
    }
  }
};

const handleResolve = (id: string, payload: any) => {
  const index = dialogs.value.findIndex((d) => d.id === id);
  if (index !== -1) {
    const dialog = dialogs.value[index];
    if (dialog) {
      // Set isOpen to false first to prevent re-triggering
      dialog.isOpen = false;
      dialog.resolve(payload);
      // Remove after a short delay to allow animation
      setTimeout(() => {
        const currentIndex = dialogs.value.findIndex((d) => d.id === id);
        if (currentIndex !== -1) {
          dialogs.value.splice(currentIndex, 1);
        }
      }, 200);
    }
  }
};

provide("openDialog", openDialog);
</script>

<template>
  <slot></slot>
  <v-dialog
    v-for="dialog in dialogs"
    :key="dialog.id"
    v-model="dialog.isOpen"
    :z-index="2000 + dialogs.indexOf(dialog)"
    @update:model-value="(value) => !value && handleClose(dialog.id)"
    :persistent="dialog.props.persistent ?? true"
  >
    <component
      :is="dialog.component"
      v-bind="dialog.props"
      @close="() => handleClose(dialog.id)"
      @resolve="(payload: any) => handleResolve(dialog.id, payload)"
    />
  </v-dialog>
</template>
