import { useDialog } from "../useDialog";
import ConfirmDialog from "./ConfirmDialog.vue";

export const useConfirm = () => {
  const openDialog = useDialog();
  return (options: any) =>
    openDialog({
      component: ConfirmDialog,
      ...options,
    });
};
