<script lang="ts" setup>
import type BackupsTable from "@/components/blocks/backups-table/BackupsTable.vue";
import TooltipIcon from "@/components/blocks/tooltip-icon/TooltipIcon.vue";
import EditBackupsDialog from "@/components/dialogs/edit-backups-dialog/EditBackupsDialog.vue";
import EditSettingsDialog from "@/components/dialogs/edit-settings-dialog/EditSettingsDialog.vue";
import { useDialog } from "@/components/dialogs/use-dialog/useDialog";
import type Backup from "@/models/backup.model";

const openDialog = useDialog();
const backupsTableRef = ref<InstanceType<typeof BackupsTable> | null>(null);

const searchFilter = ref<string>("");

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

const filterBackup = (backup: Backup): boolean => {
  const filter = searchFilter.value.toLowerCase();
  return (
    !!backup.name?.toLowerCase().includes(filter) ||
    !!backup.description?.toLowerCase().includes(filter) ||
    !!backup.date?.toLowerCase().includes(filter)
  );
};
</script>

<template>
  <v-container class="w-100 h-100">
    <v-row>
      <v-col cols="12">
        <h1>Backups</h1>
      </v-col>
      <v-col class="d-flex align-center justify-end ga-2" cols="12">
        <tooltip-icon text="This will copy and zip your current save file." />
        <v-btn prepend-icon="mdi-plus" @click="handleAddBackup">
          Backup current save
        </v-btn>
      </v-col>
      <v-col cols="12">
        <v-text-field
          v-model="searchFilter"
          label="Search for backups"
        ></v-text-field>
      </v-col>
      <v-col cols="12">
        <backups-table ref="backupsTableRef" :filter-fn="filterBackup" />
      </v-col>
    </v-row>
  </v-container>
  <floating-button
    @click.stop="() => openEditSettingsDialog()"
    color="secondary"
    icon="mdi-cog"
  />
</template>
