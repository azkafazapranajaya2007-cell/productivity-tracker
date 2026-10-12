import typer
from rich.console import Console
from rich.table import Table
import sqlite3
import os

app = typer.Typer(help="Zenith CLI - Personal Productivity & Academic Tracker")
console = Console()
DB_PATH = "db/tracker.db"

def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'To-Do'
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    init_db()
    return sqlite3.connect(DB_PATH)

@app.command("add-task")
def add_task(
    title: str = typer.Option(..., "--title", "-t", help="Judul tugas"),
    category: str = typer.Option("Umum", "--category", "-c", help="Kategori"),
    deadline: str = typer.Option("Besok", "--deadline", "-d", help="Deadline")
):
    """Menambahkan tugas baru ke database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, category, deadline, status) VALUES (?, ?, ?, ?)",
        (title, category, deadline, "To-Do")
    )
    conn.commit()
    conn.close()
    console.print(f"[bold green]✔ Sukses![/bold green] Tugas '[cyan]{title}[/cyan]' berhasil ditambahkan.")

@app.command("list-tasks")
def list_tasks():
    """Menampilkan daftar tugas dalam bentuk tabel."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category, deadline, status FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]Belum ada tugas tersimpan.[/yellow]")
        return

    table = Table(title="Daftar Tugas Zenith CLI", header_style="bold magenta")
    table.add_column("ID", justify="center", style="dim")
    table.add_column("Judul Tugas", style="bold white")
    table.add_column("Kategori", style="blue")
    table.add_column("Deadline", style="yellow")
    table.add_column("Status", justify="center", style="green")

    for row in rows:
        task_id, title, category, deadline, status = row
        table.add_row(str(task_id), title, category, deadline, status)

    console.print(table)

if __name__ == "__main__":
    app()
