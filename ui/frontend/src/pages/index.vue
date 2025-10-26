<script lang="ts" setup>
import type BackupsTable from "@/components/blocks/backups-table/BackupsTable.vue";
import EditBackupsDialog from "@/components/dialogs/edit-backups-dialog/EditBackupsDialog.vue";
import EditSettingsDialog from "@/components/dialogs/edit-settings-dialog/EditSettingsDialog.vue";
import { useDialog } from "@/components/dialogs/use-dialog/useDialog";

const openDialog = useDialog();
const backupsTableRef = ref<InstanceType<typeof BackupsTable> | null>(null);

const openEditSettingsDialog = async () => {
  await openDialog({
    component: EditSettingsDialog,
  });
};

const handleAddBackup = async () => {
  const result = await openDialog({
    component: EditBackupsDialog,
  });

  if (result) {
    await backupsTableRef.value?.getBackups();
  }
};
</script>

<template>
  <v-container class="w-100 h-100">
    <v-row>
      <v-col cols="12">
        <h1>Backups</h1>
      </v-col>
      <v-col class="d-flex align-center justify-end" cols="12">
        <v-btn prepend-icon="mdi-plus" @click="handleAddBackup">Add new</v-btn>
      </v-col>
      <v-col cols="12">
        <backups-table ref="backupsTableRef" />
      </v-col>
    </v-row>
  </v-container>
  <floating-button
    @click.stop="() => openEditSettingsDialog()"
    color="secondary"
    icon="mdi-cog"
  />
</template>
