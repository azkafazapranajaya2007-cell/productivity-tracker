import typer
from rich.console import Console
from rich.table import Table
import sqlite3
import os

app = typer.Typer(help="Kelola mata kuliah, SKS, dan kalkulator IPS/IPK")
console = Console()
DB_PATH = "db/tracker.db"

# Kamus konversi nilai huruf ke bobot angka
GRADE_POINTS = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "D": 1.0,
    "E": 0.0
}

def init_academic_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS academics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            sks INTEGER NOT NULL,
            score_letter TEXT DEFAULT '-',
            semester TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_connection():
    init_academic_db()
    return sqlite3.connect(DB_PATH)

@app.command("add")
def add_course(
    name: str = typer.Option(..., "--name", "-n", help="Nama mata kuliah"),
    sks: int = typer.Option(..., "--sks", "-s", help="Jumlah SKS"),
    score: str = typer.Option("-", "--score", "-sc", help="Nilai huruf (A, B+, B, dll)"),
    semester: str = typer.Option("1", "--semester", "-sm", help="Semester (misal: 1, 2)")
):
    """Menambahkan mata kuliah ke transkrip akademik."""
    score_upper = score.upper()
    if score_upper != "-" and score_upper not in GRADE_POINTS:
        console.print(f"[bold red]❌ Error![/bold red] Nilai '[yellow]{score}[/yellow]' tidak valid. Gunakan: A, A-, B+, B, dll.")
        raise typer.Exit(code=1)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO academics (course_name, sks, score_letter, semester) VALUES (?, ?, ?, ?)",
        (name, sks, score_upper, semester)
    )
    conn.commit()
    conn.close()
    console.print(f"[bold green]✔ Sukses![/bold green] Mata kuliah '[cyan]{name}[/cyan]' ({sks} SKS) berhasil ditambahkan.")

@app.command("list")
def list_courses(
    semester: str = typer.Option(None, "--semester", "-sm", help="Filter berdasarkan semester tertentu")
):
    """Menampilkan daftar mata kuliah, SKS, nilai, dan kalkulasi IPS."""
    conn = get_connection()
    cursor = conn.cursor()
    
    if semester:
        cursor.execute("SELECT id, course_name, sks, score_letter, semester FROM academics WHERE semester = ?", (semester,))
    else:
        cursor.execute("SELECT id, course_name, sks, score_letter, semester FROM academics")
        
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        console.print("[yellow]Belum ada data mata kuliah tersimpan.[/yellow]")
        return

    table_title = f"Transkrip Akademik Zenith CLI (Semester {semester})" if semester else "Seluruh Transkrip Akademik Zenith CLI"
    table = Table(title=table_title, header_style="bold green")
    table.add_column("ID", justify="center", style="dim")
    table.add_column("Mata Kuliah", style="bold white")
    table.add_column("SKS", justify="center", style="cyan")
    table.add_column("Nilai", justify="center", style="yellow")
    table.add_column("Bobot", justify="center", style="dim")
    table.add_column("Semester", justify="center", style="magenta")

    total_sks = 0
    total_points = 0.0

    for row in rows:
        c_id, name, sks, score, sem = row
        point = GRADE_POINTS.get(score, 0.0) if score in GRADE_POINTS else 0.0
        
        if score in GRADE_POINTS:
            total_sks += sks
            total_points += (sks * point)

        table.add_row(str(c_id), name, str(sks), score, str(point), sem)

    console.print(table)

    if total_sks > 0:
        ips = total_points / total_sks
        console.print(f"\n[bold]Total SKS Diambil (Dinilai):[/bold] {total_sks}")
        console.print(f"[bold]Estimasi IPS:[/bold] [bold green]{ips:.2f}[/bold green]\n")
    else:
        console.print("\n[yellow]Belum ada mata kuliah yang memiliki nilai huruf valid untuk kalkulasi IPS.[/yellow]\n")

@app.command("delete")
def delete_course(
    course_id: int = typer.Option(..., "--id", "-i", help="ID mata kuliah yang ingin dihapus")
):
    """Menghapus mata kuliah dari transkrip."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM academics WHERE id = ?", (course_id,))
    
    if cursor.rowcount == 0:
        console.print(f"[bold red]❌ Gagal![/bold red] Mata kuliah dengan ID [yellow]{course_id}[/yellow] tidak ditemukan.")
    else:
        conn.commit()
        console.print(f"[bold red]🗑 Dihapus![/bold red] Mata kuliah dengan ID [yellow]{course_id}[/yellow] berhasil dihapus.")
    
    conn.close()
