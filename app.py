from flask import Flask, request, render_template, jsonify
import sqlite3
import uuid
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://jonathanboyd96.github.io"])

# Initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS health_data
                        (id TEXT PRIMARY KEY, age TEXT, gender TEXT, bmi TEXT, blood_sugar TEXT)''')
        conn.commit()

@app.route('/')
def index():
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM health_data')
            data = cursor.fetchall()
    except Exception as e:
        return f"Error: {str(e)}", 500
    
    return render_template('index.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    # Debugging: Print incoming form data
    print("Form data received:", request.form)

    age = request.form.get('age')
    gender = request.form.get('gender')
    bmi = request.form.get('bmi')
    blood_sugar = request.form.get('bloodSugar')

    # Check for missing data and return a 400 error if any field is missing
    if not age or not gender or not bmi or not blood_sugar:
        return {"error": "Missing form data"}, 400

    unique_id = str(uuid.uuid4())

    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO health_data (id, age, gender, bmi, blood_sugar) VALUES (?, ?, ?, ?, ?)', 
                           (unique_id, age, gender, bmi, blood_sugar))
            conn.commit()
    except Exception as e:
        return f"Error: {str(e)}", 500

    return jsonify({"status": "success"})