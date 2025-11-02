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
      text: `Are you sure you want to delete "${backup.name}"?`,
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
      text: `This will DELETE your current save and replace it with the backup "${backup.name}".
      \nDo you want to create a backup of your CURRENT SAVE first?`,
      cancelText: "Just let me play",
      cancelColor: "success",
      confirmText: "Create backup first",
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
          title: "Load without backup?",
          text: `Just making sure – loading this backup will DELETE your current save file!`,
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
          icon="mdi-pencil"
          @click="handleEditBackup(item)"
        ></v-btn>
        <v-menu>
          <template #activator="{ props }">
            <v-btn
              size="x-small"
              icon="mdi-dots-vertical"
              variant="outlined"
              v-bind="props"
            ></v-btn>
          </template>
          <v-list>
            <v-list-item @click="handleLoadBackupWithLoadingState(item)">
              <template #prepend>
                <v-icon>mdi-backup-restore</v-icon>
              </template>
              <v-list-item-title
                v-tooltip="'Play on this backup instead of current save?'"
              >
                Play on this backup
              </v-list-item-title>
            </v-list-item>
            <v-list-item @click="handleDeleteBackup(item)" class="text-error">
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
