from flask import Flask, request, render_template_string
import sqlite3
import uuid

app = Flask(__name__)

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
    
    # Read the index.html content and render it with existing data
    with open('index.html') as f:
        return render_template_string(f.read(), data=data)

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

    # Redirect to the index page to display the updated data
    return index()

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)