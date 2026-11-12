@echo off
cd /d "%~dp0"
echo Menjalankan Reza Portfolio v2.1 pada http://127.0.0.1:5051
python app.py
if errorlevel 1 pause
