# 📚 StudyPlan - Student Workload & Task Manager

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1%2B-green.svg)](https://www.djangoproject.com/)
[![PWA](https://img.shields.io/badge/PWA-Ready-orange.svg)](#progressive-web-app-pwa)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

A clean, modern, and offline-capable student task and study workload planner built with **Django** and **Progressive Web App (PWA)** technology. Organize subjects, manage assignments and labs using an Eisenhower-style priority matrix, capture rich study notes with PDF/image attachments, and install the app seamlessly on desktop or mobile.

---

## ✨ Features

- **📚 Subject Management**: Track subjects by name, code, semester, and course description.
- **⚡ Task Tracking & Prioritization**: Mark study tasks as **Urgent** and/or **Important** (Eisenhower Matrix) and track completion status with dynamic progress meters.
- **📝 Rich Study Notes & Attachments**: Attach Markdown notes, images, and PDF lecture slides directly to specific study tasks.
- **🔔 Smart Alerts & Deadlines**: Instant dashboard visibility into pending and overdue items.
- **🌗 Theme Switcher**: Toggle between **Light**, **Dark**, and **System Auto** modes with instant persistence in `localStorage`.
- **📲 Progressive Web App (PWA)**:
  - Service Worker offline caching.
  - Small, unobtrusive install pop-up banner at the top of the screen.
  - Installable on desktop (Chrome, Edge) and mobile (Android, iOS).
- **🔒 Multi-Tenant Data Isolation**: Robust Django authentication ensures every student's records are completely private.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10 or higher installed on your system.
- Git.

### 2. Clone the Repository
```bash
git clone https://github.com/FalhanFaisal/Studyplan.git
cd Studyplan
```

### 3. Create and Activate a Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Environment Variables (Optional)
Copy `.env.example` to `.env` if you wish to configure production secrets:
```bash
cp .env.example .env
```

### 6. Run Migrations & Setup Database
```bash
python manage.py migrate
```

*(Optional) Create a superuser to access the Django Admin:*
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧪 Running Automated Tests

Run the test suite with:
```bash
python manage.py test
```

---

## 📲 Progressive Web App (PWA)

StudyPlan is fully PWA-compliant:
- **Service Worker** (`static/sw.js`) caches core application shells for fast loading.
- When visiting in supported browsers, a **sleek install pop-up window appears at the top** prompting the user to install StudyPlan for one-click access and offline capability.
- Users can dismiss the pop-up at any time via the close button.

---

## 📁 Project Structure

```text
StudyPlan/
├── accounts/               # Custom user authentication and registration
├── config/                 # Django project settings and root URLs
├── planner/                # Core study planning application
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates (dashboard, subjects, notes)
│   ├── models.py           # Subject, StudyItem, Note, Attachment models
│   ├── views.py            # Dashboard, task toggling, note views
│   └── tests.py            # Unit test suite
├── static/
│   ├── icons/              # PWA app icons (192x192, 512x512)
│   ├── manifest.json       # Web App Manifest
│   └── sw.js               # Service Worker logic
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependency manifest
├── manage.py               # Django management script
└── README.md               # Project documentation
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
