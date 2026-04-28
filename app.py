from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_PATH = "/tmp/response.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        gender TEXT,
        field_of_study TEXT,
        year_of_study INTEGER,
        stress_level INTEGER,
        sleep_hours REAL,
        social_life INTEGER,
        academic_pressure INTEGER,
        physical_activity TEXT,
        mood TEXT,
        submitted_at TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''INSERT INTO responses 
        (age, gender, field_of_study, year_of_study, stress_level, sleep_hours, social_life, academic_pressure, physical_activity, mood, submitted_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (
            int(data.get('age', 0)),
            data.get('gender'),
            data.get('field_of_study'),
            int(data.get('year_of_study', 1)),
            int(data.get('stress_level', 3)),
            float(data.get('sleep_hours', 7)),
            int(data.get('social_life', 3)),
            int(data.get('academic_pressure', 3)),
            data.get('physical_activity'),
            data.get('mood'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    )
    conn.commit()
    conn.close()
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM responses")
    total = c.fetchone()[0]

    if total == 0:
        conn.close()
        return render_template('dashboard.html', total=0, stats={}, charts={})

    c.execute("SELECT AVG(stress_level), AVG(sleep_hours), AVG(social_life), AVG(academic_pressure) FROM responses")
    avgs = c.fetchone()

    c.execute("SELECT gender, COUNT(*) FROM responses GROUP BY gender")
    gender_data = dict(c.fetchall())

    c.execute("SELECT mood, COUNT(*) FROM responses GROUP BY mood")
    mood_data = dict(c.fetchall())

    c.execute("SELECT physical_activity, COUNT(*) FROM responses GROUP BY physical_activity")
    activity_data = dict(c.fetchall())

    c.execute("SELECT year_of_study, AVG(stress_level) FROM responses GROUP BY year_of_study ORDER BY year_of_study")
    stress_by_year = c.fetchall()

    c.execute("SELECT field_of_study, COUNT(*) FROM responses GROUP BY field_of_study ORDER BY COUNT(*) DESC LIMIT 5")
    top_fields = c.fetchall()

    c.execute("SELECT stress_level, COUNT(*) FROM responses GROUP BY stress_level ORDER BY stress_level")
    stress_dist = c.fetchall()

    conn.close()

    stats = {
        'total': total,
        'avg_stress': round(avgs[0], 2) if avgs[0] else 0,
        'avg_sleep': round(avgs[1], 2) if avgs[1] else 0,
        'avg_social': round(avgs[2], 2) if avgs[2] else 0,
        'avg_pressure': round(avgs[3], 2) if avgs[3] else 0,
    }

    charts = {
        'gender': gender_data,
        'mood': mood_data,
        'activity': activity_data,
        'stress_by_year': stress_by_year,
        'top_fields': top_fields,
        'stress_dist': stress_dist,
    }

    return render_template('dashboard.html', total=total, stats=stats, charts=charts)

@app.route('/api/stats')
def api_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM responses ORDER BY submitted_at DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)
    
 init_db()

if __name__ == '__main__':
    app.run(debug=True)
