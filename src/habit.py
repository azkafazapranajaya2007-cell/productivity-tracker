import typer
from rich.console import Console
from rich.table import Table
import sqlite3
import os
from datetime import date

app = typer.Typer(help="Pelacak kebiasaan harian dan kedisiplinan (Habit Tracker)")
console = Console()
DB_PATH = "db/tracker.db"

def init_habit_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            target_days TEXT DEFAULT 'Everyday'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            log_date TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits (id)
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    init_habit_db()
    return sqlite3.connect(DB_PATH)

@app.command("add")
def add_habit(
    name: str = typer.Option(..., "--name", "-n", help="Nama habit/kebiasaan"),
    category: str = typer.Option("Produktivitas", "--category", "-c", help="Kategori habit")
):
    """Menambahkan kebiasaan baru ke pelacak."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO habits (name, category) VALUES (?, ?)",
        (name, category)
    )
    conn.commit()
    conn.close()
    console.print(f"[bold green]✔ Sukses![/bold green] Habit '[cyan]{name}[/cyan]' berhasil ditambahkan.")

@app.command("list")
def list_habits():
    """Menampilkan daftar seluruh habit yang sedang dilacak."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category FROM habits")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]Belum ada habit tersimpan. Gunakan 'add' untuk menambah.[/yellow]")
        return

    table = Table(title="Daftar Habit & Rutinitas Zenith CLI", header_style="bold blue")
    table.add_column("ID", justify="center", style="dim")
    table.add_column("Nama Habit", style="bold white")
    table.add_column("Kategori", style="cyan")

    for row in rows:
        h_id, name, category = row
        table.add_row(str(h_id), name, category)

    console.print(table)

@app.command("check")
def check_habit(
    habit_id: int = typer.Option(..., "--id", "-i", help="ID habit yang diselesaikan hari ini"),
    log_date: str = typer.Option(str(date.today()), "--date", "-d", help="Tanggal pencatatan (YYYY-MM-DD)")
):
    """Menandai habit selesai untuk tanggal tertentu (default: hari ini)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Cek apakah habit ada
    cursor.execute("SELECT name FROM habits WHERE id = ?", (habit_id,))
    habit = cursor.fetchone()
    if not habit:
        console.print(f"[bold red]❌ Gagal![/bold red] Habit dengan ID [yellow]{habit_id}[/yellow] tidak ditemukan.")
        conn.close()
        return

    # Cek apakah sudah dicek di tanggal yang sama
    cursor.execute("SELECT id FROM habit_logs WHERE habit_id = ? AND log_date = ?", (habit_id, log_date))
    existing = cursor.fetchone()
    if existing:
        console.print(f"[yellow]⚠️ Perhatian:[/yellow] Habit '[cyan]{habit[0]}[/cyan]' sudah ditandai selesai pada tanggal {log_date}.")
        conn.close()
        return

    cursor.execute("INSERT INTO habit_logs (habit_id, log_date) VALUES (?, ?)", (habit_id, log_date))
    conn.commit()
    conn.close()
    console.print(f"[bold green]✔ Hebat![/bold green] Habit '[cyan]{habit[0]}[/cyan]' tercatat selesai pada [yellow]{log_date}[/yellow].")

@app.command("summary")
def summary_habits(
    target_date: str = typer.Option(str(date.today()), "--date", "-d", help="Tanggal ringkasan (YYYY-MM-DD)")
):
    """Melihat status penyelesaian habit pada tanggal tertentu."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT h.id, h.name, h.category, 
        EXISTS(SELECT 1 FROM habit_logs hl WHERE hl.habit_id = h.id AND hl.log_date = ?) as is_done
        FROM habits h
    """, (target_date,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]Belum ada habit terdaftar.[/yellow]")
        return

    table = Table(title=f"Ringkasan Habit Tanggal: {target_date}", header_style="bold magenta")
    table.add_column("ID", justify="center", style="dim")
    table.add_column("Habit", style="bold white")
    table.add_column("Kategori", style="cyan")
    table.add_column("Status Hari Ini", justify="center")

    for row in rows:
        h_id, name, category, is_done = row
        status_styled = "[bold green]✔ Selesai[/bold green]" if is_done else "[dim]Belum[/dim]"
        table.add_row(str(h_id), name, category, status_styled)

    console.print(table)
