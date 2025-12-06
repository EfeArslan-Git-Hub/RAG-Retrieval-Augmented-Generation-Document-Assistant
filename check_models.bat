@echo off
echo Starting Auto-Configuration...
call .\.venv\Scripts\activate
python configure_model.py
