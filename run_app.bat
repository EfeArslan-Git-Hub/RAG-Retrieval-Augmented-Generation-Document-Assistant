@echo off
echo Starting RAG Document Assistant...
call .\.venv\Scripts\activate
streamlit run app.py
pause
