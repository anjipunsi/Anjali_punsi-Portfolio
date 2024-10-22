from flask import Flask, render_template, request, redirect, url_for
import psycopg2  # Use psycopg2 for PostgreSQL
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# PostgreSQL database configuration from environment variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'contact_form_db_user'),
    'password': os.getenv('DB_PASSWORD', 'N7xmlnv00dYMvGGClGMgCflzkUJlztyE'),
    'dbname': os.getenv('DB_NAME', 'contact_form_db'),
    'port': 5432
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_message', methods=['POST'])
def submit_message():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    message = request.form.get('message')

    print(f"Inserting: {fullname}, {email}, {message}")

    connection = None  # Initialize connection

    try:
        connection = psycopg2.connect(**db_config)  # Change to psycopg2
        cursor = connection.cursor()
        cursor.execute("INSERT INTO contact_messages (fullname, email, message) VALUES (%s, %s, %s)", 
                       (fullname, email, message))
        connection.commit()
        print("Data inserted successfully")
        return redirect(url_for('success'))

    except psycopg2.Error as err:  # Change error handling
        print(f"Error: {err}")
        return "Failed to submit message.", 500

    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/success')
def success():
    return '''
    <html>
        <head>
            <style>
                body {
                    background-color: black;
                    color: white;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }
                .success-message {
                    text-align: center;
                    border: 1px solid white;
                    padding: 20px;
                    border-radius: 10px;
                    background-color: #222;
                }
                a {
                    color: white;
                    text-decoration: none;
                    margin-top: 10px;
                    display: inline-block;
                    padding: 5px 10px;
                    border: 1px solid white;
                    border-radius: 5px;
                    background-color: black;
                }
                a:hover {
                    background-color: white;
                    color: black;
                }
            </style>
        </head>
        <body>
            <div class="success-message">
                <h1>Message sent successfully!</h1>
                <a href="/">Go back to home</a>
            </div>
        </body>
    </html>
    '''

@app.route('/healthz')
def health_check():
    return "Healthy", 200

if __name__ == '__main__':
    app.run(debug=True)
