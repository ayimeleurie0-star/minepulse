# MindPulse — Student Mental Health Survey App
## INF232 TP — Data Collection & Descriptive Analysis

---

## 🚀 How to Deploy on Render.com (Free)

### Step 1 — Put your code on GitHub
1. Create a free account on https://github.com
2. Create a new repository called `mindpulse`
3. Upload all these files to the repo

### Step 2 — Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select your `mindpulse` repo
4. Fill in the settings:
   - **Name**: mindpulse
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click **"Create Web Service"**
6. Wait ~2 minutes → You'll get a live URL like: `https://mindpulse.onrender.com`

### Step 3 — Send URL to professor
Send the live URL to: rollinfrancis28@gmail.com

---

## 🏃 Run Locally (for testing)

```bash
pip install flask
python app.py
```
Then open: http://localhost:5000

---

## 📁 Project Structure

```
mental_health_app/
├── app.py              # Flask backend + routes
├── requirements.txt    # Dependencies
├── Procfile           # For Render deployment
└── templates/
    ├── base.html      # Shared layout
    ├── index.html     # Home page
    ├── survey.html    # Survey form (3 sections)
    ├── thank_you.html # Confirmation page
    └── dashboard.html # Analysis dashboard
```

---

## 📊 Features
- ✅ 3-section animated survey form
- ✅ SQLite database storage
- ✅ Live dashboard with 6 charts (Chart.js)
- ✅ KPI cards: avg stress, sleep, pressure, social life
- ✅ Fully responsive design
- ✅ 100% anonymous
