from flask import Flask, request, redirect, render_template, jsonify
from flask_cors import CORS  # Import CORS
import sqlite3
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

# Initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS health_data
                        (id TEXT PRIMARY KEY, age TEXT, gender TEXT, bmi TEXT, blood_sugar TEXT)''')
        conn.commit()

@app.route('/')
def index():
    # Fetch all existing data from the database to display
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM health_data')
        data = cursor.fetchall()
    
    # Render the index.html template with existing data
    return render_template('index.html', data=data)

@app.route('/submit', methods=['POST'])
def submit():
    age = request.json['age']
    gender = request.json['gender']
    bmi = request.json['bmi']
    blood_sugar = request.json['bloodSugar']
    unique_id = str(uuid.uuid4())  # Generate a unique identifier

    # Store the data in the database
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO health_data (id, age, gender, bmi, blood_sugar) VALUES (?, ?, ?, ?, ?)', 
                       (unique_id, age, gender, bmi, blood_sugar))
        conn.commit()

    # Return a JSON response
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(host='0.0.0.0', port=5000, debug=True)  # Make sure Flask is accessible