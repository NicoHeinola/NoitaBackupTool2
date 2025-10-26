<script lang="ts" setup>
import { useSnackbar } from "@/components/blocks/snackbar/useSnackbar";
import { SettingService } from "@/services/setting.service";
import { errorSnackbar } from "@/utils/errorSnackbar";

const props = withDefaults(defineProps<{}>(), {});

const openSnackbar = useSnackbar();

const settings = ref<Record<string, any>>({
  "example-setting-1": "Some example value 1",
  "example-setting-2": "Other example value 2",
});

const emit = defineEmits<{
  (e: "resolve", payload: boolean): void;
  (e: "close"): void;
}>();

const loading = ref(false);

const getSettings = async () => {
  try {
    settings.value = await SettingService.getAllSettings();
    openSnackbar({
      props: {
        text: "Settings loaded successfully.",
        color: "success",
      },
    });
  } catch (error) {
    console.error("Error fetching settings:", error);
    errorSnackbar(openSnackbar, "Failed to load settings.", true);
  }
};

const save = async () => {
  loading.value = true;
  try {
    await SettingService.saveSettings(settings.value);
    openSnackbar({
      props: {
        text: "Settings saved successfully.",
        color: "success",
      },
    });
    emit("resolve", true);
  } catch (error) {
    console.error("Error saving settings:", error);
    errorSnackbar(openSnackbar, "Failed to save settings.", true);
  } finally {
    loading.value = false;
  }
};

onMounted(getSettings);
</script>

<template>
  <v-card>
    <v-card-title>Edit settings</v-card-title>
    <v-card-text>
      <edit-settings-form v-model="settings" />
    </v-card-text>
    <v-card-actions class="d-flex justify-end">
      <v-btn
        variant="outlined"
        color="error"
        :disabled="loading"
        @click="emit('resolve', false)"
      >
        Cancel
      </v-btn>
      <v-btn
        variant="elevated"
        color="success"
        :loading="loading"
        @click="save()"
        >OK</v-btn
      >
    </v-card-actions>
  </v-card>
</template>
