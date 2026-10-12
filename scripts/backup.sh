#!/bin/bash
BACKUP_DIR="./backups"
mkdir -p "$BACKUP_DIR"
DATE=$(date +%Y%m%d_%H%M%S)

# Cek apakah sqlite3 terinstall
if ! command -v sqlite3 &> /dev/null
then
    echo "Error: Perintah 'sqlite3' tidak ditemukan. Install dulu dengan 'sudo apt install sqlite3'."
    exit 1
fi

sqlite3 ./db/tracker.db ".backup '$BACKUP_DIR/tracker_backup_$DATE.db'"
echo "Backup database berhasil disimpan pada folder backups dengan timestamp: $DATE"
