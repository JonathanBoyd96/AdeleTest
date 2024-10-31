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
    # Read the index.html content and render it
    with open('index.html') as f:
        return render_template_string(f.read())

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

    # Render the HTML page again with the submitted data
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Adele Health Data Testing</title>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
            <header>
                <h1>Adele Health Data Testing</h1>
            </header>
            <div class="container">
                <h2>Fill out this form to have AI analyze your results</h2>
                <form action="/submit" method="post">
                    <label for="age">Age</label>
                    <input type="text" id="age" name="age" required>

                    <label for="gender">Gender</label>
                    <input type="text" id="gender" name="gender" required>

                    <label for="bmi">BMI</label>
                    <input type="text" id="bmi" name="bmi" required>

                    <label for="bloodSugar">Blood Sugar (mg/dL)</label>
                    <input type="text" id="bloodSugar" name="bloodSugar" required>

                    <button type="submit">Submit</button>
                </form>
                
                <h2>Submitted Data</h2>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Age</th>
                        <th>Gender</th>
                        <th>BMI</th>
                        <th>Blood Sugar</th>
                    </tr>
                    <tr>
                        <td>{{ unique_id }}</td>
                        <td>{{ age }}</td>
                        <td>{{ gender }}</td>
                        <td>{{ bmi }}</td>
                        <td>{{ blood_sugar }}</td>
                    </tr>
                </table>
            </div>
        </body>
        </html>
    ''', unique_id=unique_id, age=age, gender=gender, bmi=bmi, blood_sugar=blood_sugar)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)