# 🚀 CareerSync — AI Resume & Job Matching App

> **"Connecting Filipino Talent with Better Career Opportunities"**

CareerSync is a complete Django prototype for an AI-powered career platform featuring resume building, job matching, mock interview practice, and a recruiter dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 Landing Page | Modern SaaS homepage with hero, features, pricing, testimonials |
| 🔐 Authentication | Register, Login, Logout with user type (Job Seeker / Recruiter) |
| 📊 Dashboard | Stats cards, job matches, quick actions, interview history |
| 📄 Resume Builder | Full resume with education, experience, skills, certifications |
| 🤖 AI Analyzer | Rule-based scoring (0–100) with actionable feedback |
| 🎯 Job Matching | Skill-based match % algorithm sorting jobs by relevance |
| 🎙️ Mock Interview | 5-question sessions with AI feedback on each answer |
| 👥 Recruiter Hub | Post jobs, view applicants, see resume scores |
| 📬 Contact Page | Contact form with database storage |

---

## 🛠️ Installation

### Step 1 — Create Project Folder
```bash
mkdir careersync_project
cd careersync_project
```

### Step 2 — Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Copy Project Files
Place the `careersync` project folder (containing `manage.py`) inside `careersync_project/`.

### Step 4 — Install Dependencies
```bash
cd careersync
pip install -r requirements.txt
```

### Step 5 — Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6 — Seed Sample Data
```bash
python manage.py seed_data
```

This creates:
- ✅ 10 sample jobs (BPO, IT, Remote, Overseas)
- ✅ 10 interview questions with tips
- ✅ 5 sample users
- ✅ 1 complete resume for demo_user

### Step 7 — Create Admin (Optional)
```bash
python manage.py createsuperuser
```

### Step 8 — Run Server
```bash
python manage.py runserver
```

Open: **http://127.0.0.1:8000**

---

## 🔑 Demo Login

| Field | Value |
|---|---|
| Username | `demo_user` |
| Password | `CareerSync2024!` |

---

## 📁 Project Structure

```
careersync/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3              (created after migrate)
├── careersync/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── models.py           # All database models
│   ├── views.py            # All views
│   ├── urls.py             # URL routing
│   ├── forms.py            # All forms
│   ├── admin.py            # Admin config
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py
│   └── templates/
│       └── core/
│           ├── base.html
│           ├── base_dashboard.html
│           ├── landing.html
│           ├── about.html
│           ├── contact.html
│           ├── dashboard.html
│           ├── auth/
│           ├── resume/
│           ├── jobs/
│           ├── interview/
│           └── recruiter/
└── static/
    ├── css/style.css
    └── js/main.js
```

---

## 🎨 Tech Stack

- **Backend:** Django 5.x (Pure Python)
- **Database:** SQLite (zero config)
- **Frontend:** Bootstrap 5 + Custom CSS
- **Icons:** Bootstrap Icons
- **Charts:** Chart.js
- **Fonts:** Inter (Google Fonts)

---

## 🌐 Pages & URLs

| URL | Page |
|---|---|
| `/` | Landing Page |
| `/auth/register/` | Register |
| `/auth/login/` | Login |
| `/dashboard/` | User Dashboard |
| `/resume/` | Resume List |
| `/resume/create/` | Create Resume |
| `/resume/<id>/edit/` | Edit Resume |
| `/resume/<id>/preview/` | Preview Resume |
| `/resume/<id>/analyze/` | AI Analysis |
| `/jobs/` | Browse Jobs |
| `/jobs/<id>/` | Job Detail |
| `/jobs/<id>/apply/` | Apply to Job |
| `/my-applications/` | My Applications |
| `/interview/` | Interview Practice Home |
| `/interview/start/` | Start New Session |
| `/recruiter/` | Recruiter Dashboard |
| `/recruiter/post/` | Post a Job |
| `/about/` | About Page |
| `/contact/` | Contact Page |
| `/admin/` | Django Admin |

---

## 🏗️ Models

- `UserProfile` — extends User with type (jobseeker/recruiter)
- `Resume` — main resume with scoring
- `Education` — education entries
- `Experience` — work experience
- `Skill` — skills with proficiency level
- `Certification` — certifications
- `Job` — job listings with categories
- `JobApplication` — links users to jobs
- `InterviewSession` — groups interview answers
- `InterviewQuestion` — question bank
- `InterviewAnswer` — answers with AI scoring
- `ContactMessage` — contact form submissions

---

## 🤖 AI Features (Rule-Based)

### Resume Scoring Algorithm
- Professional Summary: up to 20 points
- Education: up to 20 points
- Work Experience: up to 25 points
- Skills Count: up to 25 points
- Certifications: up to 10 points

### Job Match Algorithm
Compares resume skills against job's required skills list using substring matching, returns a percentage.

### Interview Answer Scoring
Analyzes: word count, relevant keywords (action verbs), and sentence structure. Returns 0–100 score with written feedback.

---

Made with ❤️ for Filipino Talent | CareerSync © 2024
