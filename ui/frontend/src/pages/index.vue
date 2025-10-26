<script lang="ts" setup>
import EditSettingsDialog from "@/components/dialogs/edit-settings-dialog/EditSettingsDialog.vue";
import { useDialog } from "@/components/dialogs/use-dialog/useDialog";


const openDialog = useDialog();

let isDialogOpening = false;

const openEditSettingsDialog = async () => {
  console.log("Opening Edit Settings Dialog");
  if (isDialogOpening) return;

  isDialogOpening = true;

  await openDialog({
    component: EditSettingsDialog,
  });

  isDialogOpening = false;
};

</script>

<template>
  <v-container class="w-100 h-100">
    <v-row>
      <v-col cols="12">
        <h1>Backups</h1>
      </v-col>
      <v-col class="d-flex align-center justify-end" cols="12">
        <v-btn prepend-icon="mdi-plus">Add new</v-btn>
      </v-col>
      <v-col cols="12">
        <backups-table />
      </v-col>
    </v-row>
  </v-container>
  <floating-button @click="() => openEditSettingsDialog()" color="secondary" icon="mdi-cog" />
</template>
