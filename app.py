from flask import Flask, request, render_template
import sqlite3
import uuid
import os

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS health_data
                        (id TEXT PRIMARY KEY, age TEXT, gender TEXT, bmi TEXT, blood_sugar TEXT)''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')  # Use render_template

@app.route('/submit', methods=['POST'])
def submit():
    age = request.form['age']
    gender = request.form['gender']
    bmi = request.form['bmi']
    blood_sugar = request.form['bloodSugar']
    unique_id = str(uuid.uuid4())  # Generate a unique identifier

    # Store the data in the database
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO health_data (id, age, gender, bmi, blood_sugar) VALUES (?, ?, ?, ?, ?)', 
                       (unique_id, age, gender, bmi, blood_sugar))
        conn.commit()

    return "Data submitted successfully!"

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))  # Use the port from environment variable