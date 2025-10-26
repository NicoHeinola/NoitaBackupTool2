from ttkbootstrap import Window, ttk
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
import datetime

from noita_libs.noita_backup_helper import NoitaBackupHelper
from noita_libs.noita_backup import NoitaBackup
from setting_libs.setting_helper import SettingHelper


class NoitaBackupApp(Window):
    def __init__(self, backup_helper: NoitaBackupHelper):
        super().__init__(themename="flatly")
        self.title("Noita Backup Tool")
        self.geometry("900x550")

        self.backup_helper = backup_helper

        # Notebook with two tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.settings_frame = ttk.Frame(self.notebook)
        self.backups_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.backups_frame, text="Backups")
        self.notebook.add(self.settings_frame, text="Settings")

        self._build_settings_tab()
        self._build_backups_tab()

    def _build_settings_tab(self):
        pad = dict(padx=8, pady=8)

        # Read current settings
        noita_saves_dir = SettingHelper.get_setting(
            "noita_saves_dir_path", "/mnt/c/Users/user/AppData/LocalLow/Nolla_Games_Noita"
        )
        backup_dir = SettingHelper.get_setting("backup_dir_path", "./data/backups")
        backup_filename = SettingHelper.get_setting("backup_filename", "backups.json")

        # Labels + Entries
        lbl1 = ttk.Label(self.settings_frame, text="Noita saves dir:")
        lbl1.grid(row=0, column=0, sticky="w", **pad)
        self.noita_entry = ttk.Entry(self.settings_frame, width=70)
        self.noita_entry.insert(0, noita_saves_dir)
        self.noita_entry.grid(row=0, column=1, sticky="w", **pad)
        btn_browse1 = ttk.Button(self.settings_frame, text="Browse...", command=self._browse_noita)
        btn_browse1.grid(row=0, column=2, sticky="w", **pad)

        lbl2 = ttk.Label(self.settings_frame, text="Backups dir:")
        lbl2.grid(row=1, column=0, sticky="w", **pad)
        self.backup_dir_entry = ttk.Entry(self.settings_frame, width=70)
        self.backup_dir_entry.insert(0, backup_dir)
        self.backup_dir_entry.grid(row=1, column=1, sticky="w", **pad)
        btn_browse2 = ttk.Button(self.settings_frame, text="Browse...", command=self._browse_backup_dir)
        btn_browse2.grid(row=1, column=2, sticky="w", **pad)

        lbl3 = ttk.Label(self.settings_frame, text="Backups filename:")
        lbl3.grid(row=2, column=0, sticky="w", **pad)
        self.backup_filename_entry = ttk.Entry(self.settings_frame, width=70)
        self.backup_filename_entry.insert(0, backup_filename)
        self.backup_filename_entry.grid(row=2, column=1, sticky="w", **pad)

        save_btn = ttk.Button(
            self.settings_frame, text="Save Settings", bootstyle="success", command=self._save_settings
        )
        save_btn.grid(row=3, column=1, sticky="e", pady=16, padx=8)

    def _browse_noita(self):
        path = filedialog.askdirectory(title="Select Noita saves directory")
        if path:
            self.noita_entry.delete(0, "end")
            self.noita_entry.insert(0, path)

    def _browse_backup_dir(self):
        path = filedialog.askdirectory(title="Select backup directory")
        if path:
            self.backup_dir_entry.delete(0, "end")
            self.backup_dir_entry.insert(0, path)

    def _save_settings(self):
        SettingHelper.save_setting("noita_saves_dir_path", self.noita_entry.get())
        SettingHelper.save_setting("backup_dir_path", self.backup_dir_entry.get())
        SettingHelper.save_setting("backup_filename", self.backup_filename_entry.get())

        Messagebox.ok("Settings saved", title="Saved")

    def _build_backups_tab(self):
        pad = dict(padx=8, pady=8)

        # Treeview for backups
        cols = ("name", "date", "description")
        self.tree = ttk.Treeview(self.backups_frame, columns=cols, show="headings", height=18)
        self.tree.heading("name", text="Name")
        self.tree.heading("date", text="Date")
        self.tree.heading("description", text="Description")
        self.tree.column("name", width=200)
        self.tree.column("date", width=100)
        self.tree.column("description", width=400)
        self.tree.grid(row=0, column=0, columnspan=4, sticky="nsew", **pad)

        # Scrollbar
        vsb = ttk.Scrollbar(self.backups_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=4, sticky="ns", pady=8)
        self.tree.configure(yscrollcommand=vsb.set)

        # Buttons
        new_btn = ttk.Button(self.backups_frame, text="New Backup", bootstyle="primary", command=self._new_backup)
        new_btn.grid(row=1, column=0, sticky="w", padx=8, pady=6)

        restore_btn = ttk.Button(
            self.backups_frame, text="Restore Selected", bootstyle="warning", command=self._restore_selected
        )
        restore_btn.grid(row=1, column=1, sticky="w", padx=8, pady=6)

        delete_btn = ttk.Button(
            self.backups_frame, text="Delete Selected", bootstyle="danger", command=self._delete_selected
        )
        delete_btn.grid(row=1, column=2, sticky="w", padx=8, pady=6)

        refresh_btn = ttk.Button(self.backups_frame, text="Refresh", command=self.refresh_backups)
        refresh_btn.grid(row=1, column=3, sticky="e", padx=8, pady=6)

        # Make treeview expandable
        self.backups_frame.rowconfigure(0, weight=1)
        self.backups_frame.columnconfigure(0, weight=1)

        self.refresh_backups()

    def refresh_backups(self):
        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            backups = self.backup_helper.get_all_backups()
        except Exception as e:
            Messagebox.show_error(str(e), title="Error")
            return

        for b in backups:
            self.tree.insert("", "end", iid=b.id, values=(b.name, b.date or "", b.description))

    def _new_backup(self):
        modal = ttk.Toplevel(self)
        modal.title("Create New Backup")
        modal.transient(self)
        modal.grab_set()

        ttk.Label(modal, text="Name:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        name_entry = ttk.Entry(modal, width=50)
        name_entry.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(modal, text="Date (YYYY-MM-DD) (optional):").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        date_entry = ttk.Entry(modal, width=50)
        date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        date_entry.grid(row=1, column=1, padx=8, pady=8)

        ttk.Label(modal, text="Description:").grid(row=2, column=0, padx=8, pady=8, sticky="nw")
        desc_text = ttk.Text(modal, width=50, height=5)
        desc_text.grid(row=2, column=1, padx=8, pady=8)

        def _create():
            name = name_entry.get().strip()
            date = date_entry.get().strip()
            desc = desc_text.get("1.0", "end").strip()

            if not name:
                Messagebox.show_error("Name is required", title="Validation")
                return

            new = NoitaBackup(name=name, description=desc, date=date)
            try:
                self.backup_helper.save_backup(new)
            except Exception as e:
                Messagebox.show_error(str(e), title="Error")
                return

            modal.destroy()
            Messagebox.ok("Backup created", title="Success")
            self.refresh_backups()

        btn = ttk.Button(modal, text="Create", bootstyle="success", command=_create)
        btn.grid(row=3, column=1, sticky="e", padx=8, pady=8)

    def _get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            Messagebox.show_error("No backup selected", title="Error")
            return None
        return sel[0]

    def _restore_selected(self):
        bid = self._get_selected_id()
        if not bid:
            return

        if not Messagebox.yesno(
            "Are you sure you want to restore this backup? This will replace your current save.", title="Confirm"
        ):
            return

        try:
            self.backup_helper.load_backup(bid)
        except Exception as e:
            Messagebox.show_error(str(e), title="Error")
            return

        Messagebox.ok("Backup restored", title="Success")

    def _delete_selected(self):
        bid = self._get_selected_id()
        if not bid:
            return

        if not Messagebox.yesno("Delete selected backup?", title="Confirm"):
            return

        try:
            self.backup_helper.delete_backup(bid)
        except Exception as e:
            Messagebox.show_error(str(e), title="Error")
            return

        Messagebox.ok("Backup deleted", title="Deleted")
        self.refresh_backups()


def main():
    noita_saves_dir_path: str = SettingHelper.get_setting(
        "noita_saves_dir_path", "/mnt/c/Users/user/AppData/LocalLow/Nolla_Games_Noita"
    )
    backup_dir_path: str = SettingHelper.get_setting("backup_dir_path", "./data/backups")
    backup_filename: str = SettingHelper.get_setting("backup_filename", "backups.json")

    noita_backup_helper: NoitaBackupHelper = NoitaBackupHelper(
        noita_saves_dir_path=noita_saves_dir_path,
        backup_dir_path=backup_dir_path,
        backup_filename=backup_filename,
    )

    # Launch the UI
    app = NoitaBackupApp(noita_backup_helper)
    app.mainloop()


if __name__ == "__main__":
    main()
