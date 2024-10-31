from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS user_data
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    unique_identifier TEXT,
                    age TEXT,
                    gender TEXT,
                    bmi TEXT,
                    blood_sugar TEXT);''')
    conn.close()

init_db()

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.form
    unique_id = str(uuid.uuid4())
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_data (unique_identifier, age, gender, bmi, blood_sugar) VALUES (?, ?, ?, ?, ?)",
                   (unique_id, data['age'], data['gender'], data['bmi'], data['blood_sugar']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "unique_id": unique_id})