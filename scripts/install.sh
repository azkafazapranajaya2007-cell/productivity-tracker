#!/bin/bash

# Dapatkan absolute path dari direktori project saat ini
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN_PATH="/usr/local/bin/zenith"

echo "Membuat symlink global untuk Zenith CLI..."

# Buat wrapper script yang otomatis menjalankan python di dalam venv project
sudo bash -c "cat > $BIN_PATH" << WRAPPER
#!/bin/bash
source "$PROJECT_DIR/venv/bin/activate"
python3 "$PROJECT_DIR/src/main.py" "\$@"
WRAPPER

# Berikan izin eksekusi
sudo chmod +x $BIN_PATH

echo "✔ Berhasil! Sekarang kamu bisa mengetik 'zenith' dari direktori mana pun."
echo "Contoh: zenith task list"
