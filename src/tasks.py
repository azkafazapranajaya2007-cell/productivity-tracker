import typer
from rich.console import Console
from rich.table import Table
import sqlite3
import os

app = typer.Typer(help="Kelola tugas akademik dan harian")
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

@app.command("add")
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

@app.command("list")
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
        status_styled = f"[green]{status}[/green]" if status == "Done" else f"[orange1]{status}[/orange1]"
        table.add_row(str(task_id), title, category, deadline, status_styled)

    console.print(table)

@app.command("complete")
def complete_task(
    task_id: int = typer.Option(..., "--id", "-i", help="ID tugas yang ingin diselesaikan")
):
    """Mengubah status tugas menjadi 'Done' berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Done' WHERE id = ?", (task_id,))
    
    if cursor.rowcount == 0:
        console.print(f"[bold red]❌ Gagal![/bold red] Tugas dengan ID [yellow]{task_id}[/yellow] tidak ditemukan.")
    else:
        conn.commit()
        console.print(f"[bold green]✔ Berhasil![/bold green] Tugas dengan ID [yellow]{task_id}[/yellow] diubah menjadi [green]Done[/green].")
    
    conn.close()

@app.command("delete")
def delete_task(
    task_id: int = typer.Option(..., "--id", "-i", help="ID tugas yang ingin dihapus")
):
    """Menghapus tugas dari database berdasarkan ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    
    if cursor.rowcount == 0:
        console.print(f"[bold red]❌ Gagal![/bold red] Tugas dengan ID [yellow]{task_id}[/yellow] tidak ditemukan.")
    else:
        conn.commit()
        console.print(f"[bold red]🗑 Dihapus![/bold red] Tugas dengan ID [yellow]{task_id}[/yellow] berhasil dihapus dari database.")
    
    conn.close()
