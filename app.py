from __future__ import annotations

import os
import re
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "portfolio.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "local-development-key-change-before-deploy")
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

# Edit bagian ini untuk mengganti informasi profil.
PROFILE = {
    "name": "Muhammad Reza Hakiki Putra",
    "nickname": "Reza",
    "role": "Information Technology Student",
    "location": "Balikpapan, Indonesia",
    "email": "rezaputra110308@gmail.com",
    "tagline": "Curious about systems. Interested in how things work.",
    "about": (
        "Saya mahasiswa Teknologi Informasi yang senang memahami cara kerja teknologi "
        "dari sisi software maupun hardware. Saat ini saya mengeksplorasi pemrograman, "
        "jaringan komputer, Linux, dan troubleshooting melalui latihan serta proyek kecil."
    ),
    "university": "Universitas Mulia",
    "major": "Teknologi Informasi",
}

SKILLS = [
    {"name": "Python", "category": "Programming", "level": 65},
    {"name": "HTML & CSS", "category": "Programming", "level": 75},
    {"name": "Flask", "category": "Programming", "level": 45},
    {"name": "Computer Networking", "category": "Networking", "level": 70},
    {"name": "MikroTik Basics", "category": "Networking", "level": 60},
    {"name": "Linux & Ubuntu", "category": "Systems", "level": 60},
    {"name": "RAID & Storage Lab", "category": "Systems", "level": 50},
    {"name": "Hardware Troubleshooting", "category": "Hardware", "level": 75},
]

PROJECTS = [
    {
        "number": "01", "title": "Personal Portfolio", "category": "Programming",
        "subtitle": "A small space on the web", "description": "Website portfolio responsif yang dibangun dengan Flask, HTML, CSS, JavaScript, dan SQLite. Proyek ini menjadi tempat untuk mendokumentasikan proses belajar dan eksperimen web.",
        "stack": ["Python", "Flask", "HTML", "CSS", "JavaScript", "SQLite"],
        "status": "In progress", "icon": "{ }", "year": "2026",
    },
    {
        "number": "02", "title": "Linux Storage Lab", "category": "Systems",
        "subtitle": "Learning storage from the terminal", "description": "Eksperimen menggunakan Ubuntu dan virtual disk untuk memahami partisi, filesystem, mdadm, serta konsep RAID. Pengujian dilakukan pada lingkungan virtual agar konfigurasi dapat dipelajari dengan aman.",
        "stack": ["Ubuntu", "Linux", "RAID", "mdadm", "VirtualBox"],
        "status": "Learning lab", "icon": "⌁", "year": "2026",
    },
    {
        "number": "03", "title": "Network Configuration", "category": "Networking",
        "subtitle": "Connecting devices, understanding traffic", "description": "Latihan konfigurasi jaringan lokal yang mencakup pengalamatan IP, DHCP, access point, repeater, dan troubleshooting konektivitas dasar.",
        "stack": ["MikroTik", "DHCP", "Wi-Fi", "TCP/IP"],
        "status": "Learning lab", "icon": "⌘", "year": "2026",
    },
    {
        "number": "04", "title": "PC Hardware Notes", "category": "Hardware",
        "subtitle": "Understanding the parts inside a PC", "description": "Catatan pembelajaran mengenai kompatibilitas motherboard, prosesor, RAM, PSU, media penyimpanan, dan proses perakitan serta diagnosis perangkat.",
        "stack": ["PC Hardware", "Troubleshooting", "Components"],
        "status": "Ongoing notes", "icon": "▦", "year": "2026",
    },
]

EDUCATION = [
    {
        "period": "2026 — Present", "title": "Teknologi Informasi",
        "place": "Universitas Mulia · Balikpapan",
        "description": "Mempelajari dasar pemrograman, sistem komputer, jaringan, dan pemanfaatan teknologi informasi."
    }
]

INTERESTS = ["Linux & Open Source", "Computer Networking", "Web Development", "PC Hardware", "Manhwa & Anime", "Game"]
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def get_db() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_db() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )


@app.before_request
def ensure_csrf_token() -> None:
    session.setdefault("csrf_token", secrets.token_hex(32))


@app.get("/")
def home():
    return render_template(
        "index.html", profile=PROFILE, skills=SKILLS, projects=PROJECTS,
        education=EDUCATION, interests=INTERESTS, current_year=datetime.now().year,
    )


@app.post("/contact")
def contact():
    submitted = request.form.get("csrf_token", "")
    expected = session.get("csrf_token", "")
    if not expected or not secrets.compare_digest(submitted, expected):
        abort(400, description="Token formulir tidak valid. Muat ulang halaman lalu coba lagi.")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()

    errors = []
    if not 2 <= len(name) <= 80:
        errors.append("Nama harus berisi 2 sampai 80 karakter.")
    if len(email) > 120 or not EMAIL_PATTERN.fullmatch(email):
        errors.append("Format email belum benar.")
    if not 3 <= len(subject) <= 100:
        errors.append("Subjek harus berisi 3 sampai 100 karakter.")
    if not 10 <= len(message) <= 2000:
        errors.append("Pesan harus berisi 10 sampai 2.000 karakter.")

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("home", _anchor="contact"))

    with get_db() as connection:
        connection.execute(
            "INSERT INTO contact_messages (name, email, subject, message, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, email, subject, message, datetime.now(timezone.utc).isoformat(timespec="seconds")),
        )

    flash("Pesan berhasil disimpan. Terima kasih sudah menghubungi saya!", "success")
    return redirect(url_for("home", _anchor="contact"))


@app.errorhandler(400)
def bad_request(error):
    return render_template("error.html", code=400, message=error.description), 400


@app.errorhandler(413)
def request_too_large(_error):
    return render_template("error.html", code=413, message="Ukuran data yang dikirim terlalu besar."), 413


if __name__ == "__main__":
    init_db()
    # Port khusus agar tidak tertukar dengan server portfolio versi lama.
    
if __name__ == "__main__":
    init_db()

    port = int(os.environ.get("PORT", 5051))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
