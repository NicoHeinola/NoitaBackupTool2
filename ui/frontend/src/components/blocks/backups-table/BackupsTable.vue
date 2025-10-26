<script lang="ts" setup>
import { BackupService } from "@/services/backup.service";
import { useSnackbar } from "../snackbar/useSnackbar";
import type Backup from "@/models/backup.model";
import { errorSnackbar } from "@/utils/errorSnackbar";
import { headers } from "./headers";
import { useDialog } from "@/components/dialogs/use-dialog/useDialog";
import { useConfirm } from "@/components/dialogs/use-dialog/confirm/useConfirm";
import EditBackupsDialog from "@/components/dialogs/edit-backups-dialog/EditBackupsDialog.vue";

const backups = ref<Backup[]>([
  {
    id: "1",
    name: "Backup 1",
    description: "This is a test backup",
    date: "2025-01-05",
  },
  {
    id: "2",
    name: "Backup 2",
    description:
      "Mauris sem leo, tempor et ultrices nec, facilisis ut dui. Curabitur pulvinar purus nec erat ullamcorper, eget laoreet nisi lacinia. Suspendisse sit amet justo at dolor pretium bibendum. In at rutrum magna, at sollicitudin ante. Duis fermentum lacus in arcu elementum efficitur. Nullam tincidunt tristique nibh, et tempor massa posuere eget. Phasellus lobortis eget nisi suscipit lobortis. Sed a pharetra tortor. Suspendisse placerat, erat sed faucibus hendrerit, tortor nibh laoreet eros, at posuere ipsum sapien quis nibh. Sed odio lorem, maximus non maximus ac, cursus sit amet enim. Mauris quis massa mollis, porta ante ut, consectetur lorem. Nullam lobortis arcu quis justo vestibulum hendrerit. Quisque consequat odio in ornare euismod. Etiam tincidunt fermentum odio a elementum. Sed sed scelerisque nisl. ",
    date: "2025-01-06",
  },
]);

const openSnackbar = useSnackbar();
const openDialog = useDialog();
const openConfirm = useConfirm();

const loadingBackup = ref(false);

const getBackups = async () => {
  try {
    backups.value = await BackupService.getBackups();
    openSnackbar({
      props: {
        text: "Backups loaded successfully.",
        color: "success",
      },
    });
  } catch (error) {
    console.error("Error fetching backups:", error);
    errorSnackbar(openSnackbar, "Failed to load backups.", true);
  }
};

const handleEditBackup = async (backup?: Backup) => {
  const result = await openDialog({
    component: EditBackupsDialog,
    props: {
      backup,
    },
  });

  if (result) {
    await getBackups();
  }

  // Return whether the dialog resulted in a saved backup (true) or was cancelled (false/undefined)
  return result;
};

const handleDeleteBackup = async (backup: Backup) => {
  const confirmed = await openConfirm({
    props: {
      title: "Delete Backup",
      text: `Are you sure you want to delete "${backup.name}"? This action cannot be undone.`,
    },
  });

  if (confirmed) {
    try {
      await BackupService.deleteBackup(backup.id!);
      openSnackbar({
        props: {
          text: "Backup deleted successfully.",
          color: "success",
        },
      });
      await getBackups();
    } catch (error) {
      console.error("Error deleting backup:", error);
      errorSnackbar(openSnackbar, "Failed to delete backup.", true);
    }
  }
};

const handleLoadBackup = async (backup: Backup) => {
  // Ask whether user wants to backup current save first.
  const confirmed = await openConfirm({
    props: {
      title: "Backup current save?",
      text: `Create a backup of the current save before loading "${backup.name}"? Click OK to add a backup first, or Cancel to skip and load immediately.`,
      cancelText: "Load Without Backup",
      confirmText: "Backup Current Save",
    },
  });

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
          title: "Load without backup?",
          text: `Are you sure you want to load "${backup.name}" without creating a backup of the current save? This action cannot be undone.`,
        },
      });

      if (!proceed) {
        // User chose not to proceed - abort loading.
        return;
      }
    }

    // Load the selected backup
    await BackupService.loadBackup(backup.id!);

    openSnackbar({
      props: {
        text: "Backup '" + backup.name + "' loaded successfully.",
        color: "success",
      },
    });
  } catch (error) {
    console.error("Error loading backup:", error);
    errorSnackbar(openSnackbar, "Failed to load backup.", true);
  }
};

const handleLoadBackupWithLoadingState = async (backup: Backup) => {
  loadingBackup.value = true;
  try {
    await handleLoadBackup(backup);
  } finally {
    loadingBackup.value = false;
  }
};

onMounted(getBackups);

defineExpose({
  getBackups,
});
</script>

<template>
  <v-data-table multi-sort :headers="headers" :items="backups">
    <template #item.actions="{ item }">
      <div class="d-flex ga-2 justify-end">
        <v-btn
          size="x-small"
          icon="mdi-backup-restore"
          :title="'Load ' + item.name"
          :loading="loadingBackup"
          @click="handleLoadBackupWithLoadingState(item)"
        ></v-btn>
        <v-btn
          size="x-small"
          icon="mdi-pencil"
          @click="handleEditBackup(item)"
        ></v-btn>
        <v-btn
          size="x-small"
          color="error"
          icon="mdi-delete"
          @click="handleDeleteBackup(item)"
        ></v-btn>
      </div>
    </template>
  </v-data-table>
</template>
