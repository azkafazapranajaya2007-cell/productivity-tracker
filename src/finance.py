import typer
from rich.console import Console
from rich.table import Table
import sqlite3
import os

app = typer.Typer(help="Kelola pencatatan finansial dan investasi")
console = Console()
DB_PATH = "db/tracker.db"

def init_finance_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS finances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    init_finance_db()
    return sqlite3.connect(DB_PATH)

@app.command("add")
def add_finance(
    title: str = typer.Option(..., "--title", "-t", help="Keterangan transaksi"),
    type: str = typer.Option(..., "--type", "-tp", help="Tipe: 'Masuk' atau 'Keluar'"),
    category: str = typer.Option("Umum", "--category", "-c", help="Kategori (misal: Investasi, Kuliah, Jajan)"),
    amount: float = typer.Option(..., "--amount", "-a", help="Nominal uang (Rupiah)"),
    date: str = typer.Option("Hari ini", "--date", "-d", help="Tanggal (YYYY-MM-DD)")
):
    """Menambahkan catatan pemasukan atau pengeluaran finansial."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO finances (title, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
        (title, type, category, amount, date)
    )
    conn.commit()
    conn.close()
    
    console.print(f"[bold green]✔ Sukses![/bold green] Transaksi '[cyan]{title}[/cyan]' senilai Rp {amount:,.0f} berhasil dicatat.")

@app.command("list")
def list_finances():
    """Menampilkan seluruh daftar transaksi finansial dalam bentuk tabel."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, type, category, amount, date FROM finances")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]Belum ada catatan finansial.[/yellow]")
        return

    table = Table(title="Laporan Finansial & Investasi Zenith CLI", header_style="bold cyan")
    table.add_column("ID", justify="center", style="dim")
    table.add_column("Keterangan", style="bold white")
    table.add_column("Tipe", justify="center")
    table.add_column("Kategori", style="blue")
    table.add_column("Nominal (Rp)", justify="right", style="yellow")
    table.add_column("Tanggal", style="dim")

    total_balance = 0

    for row in rows:
        fin_id, title, f_type, category, amount, date = row
        if f_type.lower() == "masuk":
            type_styled = "[green]Masuk[/green]"
            total_balance += amount
            amount_styled = f"[green]Rp {amount:,.0f}[/green]"
        else:
            type_styled = "[red]Keluar[/red]"
            total_balance -= amount
            amount_styled = f"[red]-Rp {amount:,.0f}[/red]"

        table.add_row(str(fin_id), title, type_styled, category, amount_styled, date)

    console.print(table)
    
    balance_color = "green" if total_balance >= 0 else "red"
    console.print(f"\n[bold]Total Estimasi Saldo/Aset:[/bold] [{balance_color}]Rp {total_balance:,.0f}[/{balance_color}]\n")

