<script lang="ts" setup>
import type Backup from '@/models/backup.model';
import { useSnackbar } from '@/components/blocks/snackbar/useSnackbar';
import { BackupService } from '@/services/backup.service';
import { errorSnackbar } from '@/utils/errorSnackbar';
import { useConfirm } from '../use-dialog/confirm/useConfirm';
import { useSafetyStore } from '@/stores/safety';

const props = withDefaults(
  defineProps<{
    backup?: Backup;
    title?: string;
    saveButtonText?: string;
    handleSave?: boolean;
  }>(),
  {
    backup: undefined,
    title: undefined,
    saveButtonText: undefined,
    handleSave: true,
  },
);

const openSnackbar = useSnackbar();
const openConfirm = useConfirm();
const safetyStore = useSafetyStore();

const backupData = ref<Backup>({
  id: props.backup?.id,
  name: props.backup?.name || '',
  description: props.backup?.description || '',
  date: props.backup?.date,
});

const emit = defineEmits<{
  (e: 'resolve', payload: boolean | Backup): void;
  (e: 'close'): void;
}>();

const loading = ref(false);

const isEditMode = computed(() => !!props.backup?.id);

async function save() {
  // If saving is handled externally, just emit the data
  if (!props.handleSave) {
    emit('resolve', false);
    return;
  }

  await safetyStore.checkIsNoitaRunning();

  if (safetyStore.isNoitaRunning) {
    const confirmed = await openConfirm({
      props: {
        title: 'Noita is running!',
        text: `Are you sure you want to create a backup while Noita is running? It is recommended to close Noita before creating backups to avoid potential corruption.`,
      },
    });

    if (!confirmed) {
      emit('resolve', false);
      return;
    }
  }

  loading.value = true;
  try {
    await BackupService.saveBackup(backupData.value);
    openSnackbar({
      props: {
        text: isEditMode.value ? 'Backup updated successfully.' : 'Backup created successfully.',
        color: 'success',
      },
    });
    emit('resolve', true);
  } catch (error) {
    console.error('Error saving backup:', error);
    errorSnackbar(openSnackbar, error);
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <v-card>
    <v-card-title>
      {{ props.title ? props.title : isEditMode ? 'Edit Backup' : 'Add Backup' }}
    </v-card-title>
    <v-card-text>
      <edit-backups-form v-model="backupData" />
    </v-card-text>
    <v-card-actions class="d-flex justify-end">
      <v-btn color="error" :disabled="loading" variant="outlined" @click="emit('resolve', false)"> Cancel </v-btn>
      <v-btn color="success" :loading="loading" variant="elevated" @click="save()">
        {{ saveButtonText ? saveButtonText : isEditMode ? 'Update' : 'Create' }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>
