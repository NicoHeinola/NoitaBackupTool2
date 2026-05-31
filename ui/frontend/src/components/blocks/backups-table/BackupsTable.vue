<script lang="ts" setup>
import type Backup from '@/models/backup.model';
import EditBackupsDialog from '@/components/dialogs/edit-backups-dialog/EditBackupsDialog.vue';
import { useConfirm } from '@/components/dialogs/use-dialog/confirm/useConfirm';
import { useDialog } from '@/components/dialogs/use-dialog/useDialog';
import { BackupService } from '@/services/backup.service';
import { useBackupStore } from '@/stores/backup';
import { errorSnackbar } from '@/utils/errorSnackbar';
import { useSnackbar } from '../snackbar/useSnackbar';
import { headers } from './headers';

const props = withDefaults(
  defineProps<{
    filterFn?: (backup: Backup) => boolean;
  }>(),
  {
    filterFn: () => true,
  },
);

const backupStore = useBackupStore();

const backups = ref<Backup[]>([
  {
    id: '550e8400-e29b-41d4-a716-446655440000',
    name: 'Dummy Backup for testing (1)',
    description: 'This is a dummy backup used for testing purposes.',
    date: '2025-01-05',
  },
  {
    id: '660e8400-e29b-41d4-a716-446655440111',
    name: 'Dummy Backup for testing (2). Very long name to test UI behavior with long names',
    description:
      'Mauris sem leo, tempor et ultrices nec, facilisis ut dui. Curabitur pulvinar purus nec erat ullamcorper, eget laoreet nisi lacinia. Suspendisse sit amet justo at dolor pretium bibendum. In at rutrum magna, at sollicitudin ante. Duis fermentum lacus in arcu elementum efficitur. Nullam tincidunt tristique nibh, et tempor massa posuere eget. Phasellus lobortis eget nisi suscipit lobortis. Sed a pharetra tortor. Suspendisse placerat, erat sed faucibus hendrerit, tortor nibh laoreet eros, at posuere ipsum sapien quis nibh. Sed odio lorem, maximus non maximus ac, cursus sit amet enim. Mauris quis massa mollis, porta ante ut, consectetur lorem. Nullam lobortis arcu quis justo vestibulum hendrerit. Quisque consequat odio in ornare euismod. Etiam tincidunt fermentum odio a elementum. Sed sed scelerisque nisl. ',
    date: '2025-01-06',
  },
]);

const filteredBackups = computed(() =>
  backups.value.filter((backup) => props.filterFn!(backup)),
);

const openSnackbar = useSnackbar();
const openDialog = useDialog();
const openConfirm = useConfirm();

const isLoading = ref(false);

async function getBackups() {
  try {
    backups.value = await BackupService.getBackups();
  } catch (error) {
    console.error('Error fetching backups:', error);
    errorSnackbar(openSnackbar, error);
  }
}

async function handleEditBackup(backup?: Backup) {
  const result = await openDialog({
    component: EditBackupsDialog,
    props: {
      backup,
    },
  });

  if (result) {
    await getBackups();
  }

  return result;
}

async function handleDeleteBackup(backup: Backup) {
  const confirmed = await openConfirm({
    props: {
      title: 'Delete Backup',
      text: `Are you sure you want to delete "${backup.name}"?`,
    },
  });

  if (!confirmed) {
    return;
  }

  try {
    await BackupService.deleteBackup(backup.id!);
    openSnackbar({
      props: {
        text: 'Backup deleted successfully.',
        color: 'success',
      },
    });
    await getBackups();
  } catch (error) {
    console.error('Error deleting backup:', error);
    errorSnackbar(openSnackbar, error);
  }
}

async function handleLoadBackup(backup: Backup) {
  // Ask whether user wants to backup current save first.
  const confirmed = await openConfirm({
    props: {
      title: 'Backup current save?',
      text: `This will DELETE your current save and replace it with the backup "${backup.name}".
      \nDo you want to create a backup of your CURRENT SAVE first?`,
      cancelText: 'Just let me play',
      cancelColor: 'error',
      confirmText: 'Create backup first',
      persistent: false,
    },
  });

  // User closed dialog
  if (confirmed === null) {
    return;
  }

  try {
    if (confirmed) {
      // Reuse existing edit/create handler (no backup arg => create new)
      const created = await handleEditBackup();

      if (!created) {
        // User chose not to create backup after all - abort loading.
        return;
      }
    } else {
      // Make extra sure if user doesn't want to create a backup
      const proceed = await openConfirm({
        props: {
          title: 'Load without backup?',
          text: 'Just making sure – loading this backup will DELETE your current save file!',
        },
      });

      if (!proceed) {
        // User chose not to proceed - abort loading.
        return;
      }
    }

    // Load the selected backup
    await BackupService.loadBackup(backup.id!);

    backupStore.setLastSelectedBackupId(backup.id || null);

    openSnackbar({
      props: {
        text: "Backup '" + backup.name + "' loaded successfully.",
        color: 'success',
      },
    });
  } catch (error) {
    console.error('Error loading backup:', error);
    errorSnackbar(openSnackbar, error);
  }
}

async function handleDuplicateBackup(backup: Backup) {
  const result = await openDialog({
    component: EditBackupsDialog,
    props: {
      backup,
      title: 'Duplicate Backup',
      saveButtonText: 'Duplicate',
      handleSave: false,
    },
  });

  if (!result) {
    return;
  }

  try {
    await BackupService.duplicateBackup(backup.id!, result);
    openSnackbar({
      props: {
        text: 'Backup duplicated successfully.',
        color: 'success',
      },
    });
    await getBackups();
  } catch (error) {
    console.error('Error duplicating backup:', error);
    errorSnackbar(openSnackbar, error);
  }
}

async function handleReplaceBackup(backup: Backup) {
  const confirmed = await openConfirm({
    props: {
      title: 'Overwrite Backup',
      text: `This will overwrite "${backup.name}" with your current save file.\nAre you sure you want to proceed?`,
    },
  });

  if (!confirmed) {
    return;
  }

  try {
    await BackupService.replaceBackup(backup.id!);
    openSnackbar({
      props: {
        text: 'Backup replaced with current save successfully.',
        color: 'success',
      },
    });
    await getBackups();
  } catch (error) {
    console.error('Error replacing backup:', error);
    errorSnackbar(openSnackbar, error);
  }
}

async function handleFnWithLoading(
  fn: (...data: any[]) => any,
  ...data: any[]
) {
  isLoading.value = true;

  try {
    await fn(...data);
  } catch {
  } finally {
    isLoading.value = false;
  }
}

function getShortenedText(text: string, maxLength: number) {
  if (text.length <= maxLength) {
    return text;
  }
  return text.slice(0, maxLength) + '...';
}

onMounted(getBackups);

defineExpose({
  getBackups,
});
</script>

<template>
  <v-data-table
    :headers="headers"
    :items="filteredBackups"
    :items-per-page="9"
    :items-per-page-options="[9, 30, 50, 100, -1]"
    :loading="isLoading"
    multi-sort
    :row-props="
      (item: any) => ({
        class:
          item.item.id === backupStore.lastSelectedBackupId
            ? 'selected-row'
            : ``,
        style: { cursor: 'pointer' },
      })
    "
  >
    <template #item.id="{ item }">
      <span class="d-block text-truncate" style="max-width: 50px">
        {{ item.id }}
        <v-tooltip activator="parent"> {{ item.id }} </v-tooltip>
      </span>
    </template>
    <template #item.description="{ item }">
      <span>
        {{ getShortenedText(item.description || '', 150) }}
        <v-tooltip activator="parent"> {{ item.description }} </v-tooltip>
      </span>
    </template>
    <template #item.actions="{ item }">
      <div class="d-flex ga-2 justify-end">
        <v-btn
          v-tooltip="'Play on this backup instead of current save?'"
          icon="mdi-backup-restore"
          :loading="isLoading"
          size="x-small"
          @click="handleFnWithLoading(handleLoadBackup, item)"
        />
        <v-menu>
          <template #activator="{ props: activatorProps }">
            <v-btn
              icon="mdi-dots-vertical"
              size="x-small"
              variant="outlined"
              v-bind="activatorProps"
            />
          </template>
          <v-list>
            <v-list-item @click="handleFnWithLoading(handleEditBackup, item)">
              <template #prepend>
                <v-icon>mdi-pencil</v-icon>
              </template>
              <v-list-item-title
                v-tooltip="'Edit the information of this backup'"
              >
                Edit
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              @click="handleFnWithLoading(handleDuplicateBackup, item)"
            >
              <template #prepend>
                <v-icon>mdi-content-copy</v-icon>
              </template>
              <v-list-item-title v-tooltip="'Makes a copy of this backup.'">
                Duplicate
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              @click="handleFnWithLoading(handleReplaceBackup, item)"
            >
              <template #prepend>
                <v-icon>mdi-file-replace</v-icon>
              </template>
              <v-list-item-title
                v-tooltip="'Overwrite this backup with the current save.'"
              >
                Replace
              </v-list-item-title>
            </v-list-item>
            <v-list-item
              class="text-error"
              @click="handleFnWithLoading(handleDeleteBackup, item)"
            >
              <template #prepend>
                <v-icon>mdi-delete</v-icon>
              </template>
              <v-list-item-title>Delete</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </template>
  </v-data-table>
</template>

<style scoped>
:deep(.selected-row) {
  background-color: #9b27b02a;
}
</style>
