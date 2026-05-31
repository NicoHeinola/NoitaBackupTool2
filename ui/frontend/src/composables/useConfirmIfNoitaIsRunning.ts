import { useConfirm } from '@/components/dialogs/use-dialog/confirm/useConfirm';
import { useSafetyStore } from '@/stores/safety';

const useConfirmIfNoitaIsRunning = () => {
  const safetyStore = useSafetyStore();
  const openConfirm = useConfirm();

  const confirmIfNoitaIsRunning = async () => {
    await safetyStore.checkIsNoitaRunning();

    if (safetyStore.isNoitaRunning) {
      return await openConfirm({
        props: {
          title: 'Noita is running!',
          text: `Noita is currently running. It is recommended to close Noita before performing this action to avoid potential corruption.\nDo you want to proceed anyway?`,
          cancelText: 'Cancel',
          confirmText: 'Proceed',
          persistent: false,
        },
      });
    }

    return true;
  };

  return {
    confirmIfNoitaIsRunning,
  };
};

export default useConfirmIfNoitaIsRunning;
