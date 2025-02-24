#!/usr/bin/env python3
import os
import subprocess
import sys

class FolderMigrate:
    """
    Migrate local folders to a remote server.
    
    local_addr: str – local directory path.
    remote_addr: str – remote destination in the format user@host:/path/to/dir.
    """
    def __init__(self, local_addr: str, remote_addr: str):
        self.local_addr = local_addr
        self.remote_addr = remote_addr

        folders_to_migrate = self.compare()
        if not folders_to_migrate:
            print("[*] All local folders already exist on the remote server.")
        else:
            print(f"[*] Folders to migrate: {folders_to_migrate}")
            if self.migrate(folders_to_migrate):
                print("[*] Migration completed successfully.")
            else:
                print("[*] Migration encountered errors.")

    def get_folders(self, work_dir: str) -> [str]:
        """
        Return a list of folder names in the given directory.
        If work_dir is remote (format: user@host:/path), use SSH to list folders.
        """
        if "@" in work_dir and ":" in work_dir:
            # Remote directory: split into user@host and remote path
            userhost, remote_path = work_dir.split(":", 1)
            try:
                # List directories remotely; assumes folders have trailing '/'.
                result = subprocess.run(
                    ["ssh", userhost, f"ls -1d {remote_path}/*/"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if result.returncode != 0:
                    print(f"Error listing remote directory: {result.stderr.strip()}")
                    return []
                folders = []
                for line in result.stdout.strip().splitlines():
                    # Remove trailing slashes and path components.
                    folder_name = os.path.basename(os.path.normpath(line))
                    folders.append(folder_name)
                return folders
            except Exception as e:
                print(f"Error accessing remote directory {work_dir}: {e}")
                return []
        else:
            # Local directory
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
            result = subprocess.run(["scp", "-r", local_path, self.remote_addr])
            if result.returncode != 0:
                print(f"Error migrating folder: {folder}")
                success = False
        return success

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python folder_migrate.py <local_folder> <remote_folder>")
        sys.exit(1)
    local_folder = sys.argv[1]
    remote_folder = sys.argv[2]
    FolderMigrate(local_folder, remote_folder)
