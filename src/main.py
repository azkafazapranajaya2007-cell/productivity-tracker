import typer
from tasks import app as tasks_app
from finance import app as finance_app
from academic import app as academic_app
from habit import app as habit_app

app = typer.Typer(
    help="Zenith CLI - Personal Productivity, Academic & Financial Tracker",
    add_completion=False
)

# Hubungkan seluruh sub-module ke main app
app.add_typer(tasks_app, name="task", help="Manajemen Tugas Akademik")
app.add_typer(finance_app, name="finance", help="Manajemen Finansial & Investasi")
app.add_typer(academic_app, name="academic", help="Pelacak SKS, Transkrip & Kalkulator IPS")
app.add_typer(habit_app, name="habit", help="Pelacak Kebiasaan & Rutinitas Harian")

if __name__ == "__main__":
    app()
