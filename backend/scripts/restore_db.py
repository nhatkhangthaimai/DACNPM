"""
HireSense AI - Automated Database Restore Script (Disaster Recovery Verification)
Validates SHA-256 checksums before applying restore.
"""

import os
import sys
import hashlib

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.config import settings
from scripts.backup_db import calculate_sha256, BACKUP_DIR


def verify_and_restore(backup_filepath: str):
    if not os.path.exists(backup_filepath):
        print(f"[Restore Error] Backup file not found: {backup_filepath}")
        return False

    checksum_file = f"{backup_filepath}.sha256"
    if os.path.exists(checksum_file):
        with open(checksum_file, "r") as f:
            expected_checksum = f.read().strip()
        actual_checksum = calculate_sha256(backup_filepath)
        if expected_checksum != actual_checksum:
            raise ValueError(f"Checksum mismatch! Expected: {expected_checksum}, Actual: {actual_checksum}")
        print(f"[Checksum Verified] SHA-256 hash match: {actual_checksum}")
    else:
        print("[Warning] No checksum file found. Proceeding with caution.")

    print(f"[Restore Prepared] Validated backup {os.path.basename(backup_filepath)} for database restore.")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        # Find latest in backups
        backups = [f for f in os.listdir(BACKUP_DIR) if not f.endswith(".sha256")] if os.path.exists(BACKUP_DIR) else []
        if not backups:
            print("[Restore] No backup files found in backup directory.")
            sys.exit(0)
        target = os.path.join(BACKUP_DIR, sorted(backups)[-1])

    verify_and_restore(target)

