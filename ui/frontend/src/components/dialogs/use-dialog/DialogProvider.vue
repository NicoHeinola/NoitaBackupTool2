<script setup lang="ts">
import type { DialogApi } from './DialogApi';
import type { DialogOptions } from './DialogOptions';
import { markRaw, onUnmounted, provide, ref } from 'vue';
import { dialogApiKey } from './dialogApiKey';

interface DialogItem {
  id: number;
  component: any;
  props: Record<string, unknown>;
  isOpen: boolean;
  closeDelay: number;
  isClosing: boolean;
  resolve: (value: unknown) => void;
}

const dialogs = ref<DialogItem[]>([]);
const defaultCloseDelay = 220;
const pendingCloseTimeouts = new Set<number>();
let nextDialogId = 0;

function removeDialog(dialogId: number) {
  const dialogIndex = dialogs.value.findIndex(
    (dialog) => dialog.id === dialogId,
  );

  if (dialogIndex === -1) {
    return;
  }

  dialogs.value.splice(dialogIndex, 1);
}

function closeDialog(dialogId: number, value?: unknown) {
  const dialog = dialogs.value.find(
    (activeDialog) => activeDialog.id === dialogId,
  );

  if (dialog === undefined || dialog.isClosing) {
    return;
  }

  dialog.isClosing = true;
  dialog.isOpen = false;
  dialog.resolve(value);

  const timeoutId = window.setTimeout(() => {
    pendingCloseTimeouts.delete(timeoutId);
    removeDialog(dialogId);
  }, dialog.closeDelay);

  pendingCloseTimeouts.add(timeoutId);
}

function showDialog<
  Result = unknown,
  Props extends Record<string, unknown> = Record<string, never>,
>(options: DialogOptions<Props>): Promise<Result | undefined> {
  return new Promise((resolve) => {
    dialogs.value.push({
      id: nextDialogId++,
      component: markRaw(options.component),
      props: options.props ?? {},
      isOpen: true,
      closeDelay: options.closeDelay ?? defaultCloseDelay,
      isClosing: false,
      resolve: (value) => {
        resolve(value as Result | undefined);
      },
    });
  });
}

const dialogApi: DialogApi = {
  showDialog,
};

provide(dialogApiKey, dialogApi);

onUnmounted(() => {
  for (const timeoutId of pendingCloseTimeouts) {
    window.clearTimeout(timeoutId);
  }

  pendingCloseTimeouts.clear();
  dialogs.value = [];
});
</script>

<template>
  <slot />

  <v-dialog
    v-for="dialog in dialogs"
    :key="dialog.id"
    v-model="dialog.isOpen"
    :persistent="(dialog.props as any).persistent ?? true"
    :z-index="2000 + dialogs.indexOf(dialog)"
    @update:model-value="(value) => !value && closeDialog(dialog.id)"
  >
    <component
      :is="dialog.component"
      v-bind="dialog.props"
      @close="() => closeDialog(dialog.id)"
      @resolve="(payload: any) => closeDialog(dialog.id, payload)"
    />
  </v-dialog>
</template>
