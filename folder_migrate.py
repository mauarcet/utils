#!/usr/bin/env python3
import os
import subprocess
import sys
import argparse

class FolderMigrate:
    """
    Migrate local folders to a remote server.
    
    local_addr: str – local directory path.
    remote_addr: str – remote destination in the format user@host:/path/to/dir.
    password: Optional SSH password for non-interactive authentication.
    """
    def __init__(self, local_addr: str, remote_addr: str, password: str = None):
        self.local_addr = local_addr
        self.remote_addr = remote_addr
        self.password = password

        folders_to_migrate = self.compare()
        if not folders_to_migrate:
            print("[*] All local folders already exist on the remote server.")
            return

        print(f"[*] Folders to migrate: {folders_to_migrate}")
        confirm = input("Do you want to proceed with migration? (yes/no): ").strip().lower()
        if confirm not in ("yes", "y"):
            print("[*] Migration cancelled by the user.")
            return

        if self.migrate(folders_to_migrate):
            print("[*] Migration completed successfully.")
        else:
            print("[*] Migration encountered errors.")

    def get_folders(self, work_dir: str) -> [str]:
        """
        Return a list of folder names in the given directory.
        If work_dir is remote (format: user@host:/path), use SSH (with sshpass if password is provided).
        """
        if "@" in work_dir and ":" in work_dir:
            userhost, remote_path = work_dir.split(":", 1)
            cmd = (
                ["sshpass", "-p", self.password, "ssh", userhost, f"ls -1d {remote_path}/*/"]
                if self.password
                else ["ssh", userhost, f"ls -1d {remote_path}/*/"]
            )
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(f"Error listing remote directory: {result.stderr.strip()}")
                return []
            folders = []
            for line in result.stdout.strip().splitlines():
                folder_name = os.path.basename(os.path.normpath(line))
                folders.append(folder_name)
            return folders
        else:
            try:
                items = os.listdir(work_dir)
                return [item for item in items if os.path.isdir(os.path.join(work_dir, item))]
            except Exception as e:
                print(f"Error accessing directory {work_dir}: {e}")
                return []

    def compare(self):
        """
        Compare folders in local and remote directories.
        Returns a list of folder names that are present locally but missing remotely.
        If all folders exist remotely, returns None.
        """
        local_folders = self.get_folders(self.local_addr)
        remote_folders = self.get_folders(self.remote_addr)
        missing_folders = [folder for folder in local_folders if folder not in remote_folders]
        return missing_folders if missing_folders else None

    def migrate(self, folders_to_migrate: [str]) -> bool:
        """
        Secure copy (scp) the missing folders to the remote server.
        Returns True if all migrations succeed; otherwise, False.
        """
        success = True
        for folder in folders_to_migrate:
            local_path = os.path.join(self.local_addr, folder)
            print(f"[*] Migrating folder: {folder}...")
            cmd = (
                ["sshpass", "-p", self.password, "scp", "-r", local_path, self.remote_addr]
                if self.password
                else ["scp", "-r", local_path, self.remote_addr]
            )
            result = subprocess.run(cmd)
            if result.returncode != 0:
                print(f"Error migrating folder: {folder}")
                success = False
        return success

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Folder Migrate: Sync local folders to a remote server.")
    parser.add_argument("local_folder", help="Local folder path")
    parser.add_argument("remote_folder", help="Remote folder in the format user@host:/path/to/folder")
    parser.add_argument("--password", help="SSH password for remote server (optional)", default=None)
    args = parser.parse_args()

    FolderMigrate(args.local_folder, args.remote_folder, args.password)
