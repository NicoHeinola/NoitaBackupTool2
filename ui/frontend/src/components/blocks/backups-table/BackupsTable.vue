<script lang="ts" setup>
import { BackupService } from "@/services/backup.service";
import { useSnackbar } from "../snackbar/useSnackbar";
import type Backup from "@/models/backup.model";
import { errorSnackbar } from "@/utils/errorSnackbar";
import { headers } from "./headers";

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
    description: "This is another test backup",
    date: "2025-01-06",
  }
]);

const openSnackbar = useSnackbar();

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

//onMounted(getBackups);
</script>

<template>
  Backups: {{ backups }}
  <v-data-table :headers="headers" :items="backups">
    <template #item.actions>
      <div class="d-flex ga-2 justify-end">
        <v-btn size="x-small" icon="mdi-pencil"></v-btn>
        <v-btn size="x-small" color="error" icon="mdi-delete"></v-btn>
      </div>
    </template>
  </v-data-table>
</template>
