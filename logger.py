# logger.py
import json
import csv
import os
from datetime import datetime

JSON_LOG_FILE = "conversation_history.json"
CSV_LOG_FILE = "conversation_history.csv"

def log_interaction_json(scheme_name: str, question: str, answer: str, retrieved_chunks: list):
    """Appends question, answer, retrieved chunks, and timestamp to a JSON file."""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scheme_name": scheme_name,
        "question": question,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks
    }

    history = []
    if os.path.exists(JSON_LOG_FILE):
        try:
            with open(JSON_LOG_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    history.append(log_entry)

    with open(JSON_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

def log_interaction_csv(scheme_name: str, question: str, answer: str):
    """Appends question, answer, and timestamp to a CSV file."""
    file_exists = os.path.exists(CSV_LOG_FILE)

    with open(CSV_LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Scheme Name", "Question", "Answer"])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            scheme_name,
            question,
            answer
        ])