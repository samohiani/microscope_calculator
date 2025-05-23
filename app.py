from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            microscope_size REAL,
            magnification REAL,
            actual_size REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_record(username, microscope_size, magnification, actual_size):
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO records (username, microscope_size, magnification, actual_size)
        VALUES (?, ?, ?, ?)
    ''', (username, microscope_size, magnification, actual_size))
    conn.commit()
    conn.close()

def get_all_records():
    conn = sqlite3.connect("specimens.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, microscope_size, magnification, actual_size FROM records ORDER BY id DESC")
    records = cursor.fetchall()
    conn.close()
    return records

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        username = request.form["username"]
        microscope_size = float(request.form["microscope_size"])
        magnification = float(request.form["magnification"])
        actual_size = microscope_size / magnification
        insert_record(username, microscope_size, magnification, actual_size)
        result = round(actual_size, 4)

    records = get_all_records()
    return render_template("index.html", result=result, records=records)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)