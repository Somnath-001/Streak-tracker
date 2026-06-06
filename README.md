# 🔥 Streaks — Habit Tracker & Productivity App

> A full-stack productivity web application to track habits, manage tasks, take notes, and visualize performance — built with Django.

## 🌐 Live Demo
**[https://streak-tracker-a0da.onrender.com](https://streak-tracker-a0da.onrender.com)**

> ⚠️ Hosted on Render free tier — app may take 30–60 seconds to wake up on first visit.

---

## ✨ Features

**Habits**
- Create habits with a start and end date
- Check off each day using a checkbox calendar view
- Track completion rate and highest streak per habit
- Filter habits by Ongoing, Completed, or Deleted

**To-Do List**
- Add tasks with deadlines and reminders
- Toggle task status between Pending and Completed
- Delete tasks when done

**Notes**
- Create notes with title, heading, and content
- View and delete saved notes

**Performance Reports**
- Summary of habit consistency and progress
- Motivational milestones based on achievements
- Bar graph showing habit completion rates
- Pie chart showing completed vs uncompleted days

**Authentication**
- User registration and login
- All pages protected — only accessible after login

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django (Python) |
| Database | SQLite3 |
| Frontend | HTML, CSS, Bootstrap |
| Charts | Chart.js |
| Deployment | Render |
| Task Queue | Celery |

---

## ⚙️ Setup & Installation

**1. Clone the repo**
git clone https://github.com/Somnath-001/Streak-tracker.git
cd Streak-tracker

**2. Create virtual environment**
python3 -m venv venv
source venv/bin/activate

**3. Install dependencies**
pip install -r requirements.txt

**4. Add localhost to ALLOWED_HOSTS in my_webapp/settings.py**
ALLOWED_HOSTS = ['streak-tracker-a0da.onrender.com', '127.0.0.1', 'localhost']

**5. Run migrations**
python3 manage.py migrate

**6. Start the server**
python3 manage.py runserver

**7. Open in browser**
http://127.0.0.1:8000

---

## 📁 Project Structure

Streak-tracker/
├── core/               ← Main Django app
├── my_webapp/          ← Django project settings
├── staticfiles/        ← Static assets
├── manage.py           ← Django entry point
└── requirements.txt    ← Python dependencies

---

## 👨‍💻 Author

Somnath Shinde
MCA Student — PES University, Bangalore
github.com/Somnath-001
