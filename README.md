# 📊 Enterprise Productivity & Task Tracker

> A modern, containerized productivity and task management tracking system designed for streamlined workflow analytics, personal milestone monitoring, and task tracking efficiency.

---

## 🚀 Overview

**Productivity Tracker** is a full-stack application built to monitor, analyze, and manage daily development tasks, project timelines, and productivity metrics. Designed with clean architectural standards, it bridges the gap between daily task execution and high-level progress evaluation.

---

## 🛠️ Tech Stack

* **Backend & API:** Python, FastAPI
* **Data Persistence:** SQLite, SQLAlchemy
* **Frontend & Visualization:** Streamlit / Modern Web Interface
* **Containerization & Deployment:** Docker, Docker Compose
* **Environment Management:** WSL2 (Linux)

---

## 📂 Project Architecture

```text
productivity-tracker/
├── backend/
│   ├── main.py            # FastAPI REST API endpoints & business logic
│   ├── models.py          # Database schemas & ORM configurations
│   ├── requirements.txt   # Python dependencies for backend
│   └── Dockerfile         # Container build file for backend service
├── dashboard/
│   ├── app.py             # Interactive frontend UI & analytics charts
│   ├── requirements.txt   # Python dependencies for dashboard
│   └── Dockerfile         # Container build file for dashboard service
├── data/                  # Persistent SQLite database volume
└── docker-compose.yml     # Multi-container orchestration config
