from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def insert_record(username, microscope_size, magnification, actual_size):
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
    cursor.execute('''
        INSERT INTO records (username, microscope_size, magnification, actual_size)
        VALUES (?, ?, ?, ?)
    ''', (username, microscope_size, magnification, actual_size))
    conn.commit()
    conn.close()

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
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
