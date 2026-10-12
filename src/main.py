import typer
from tasks import app as tasks_app
from finance import app as finance_app

app = typer.Typer(
    help="Zenith CLI - Personal Productivity, Academic & Financial Tracker",
    add_completion=False
)

# Hubungkan sub-module ke main app
app.add_typer(tasks_app, name="task", help="Manajemen Tugas Akademik")
app.add_typer(finance_app, name="finance", help="Manajemen Finansial & Investasi")

if __name__ == "__main__":
    app()
