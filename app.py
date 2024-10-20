from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': 'roottest@1234',  # Your MySQL password
    'database': 'contact_form_db'  # Your database name
}

# Route for serving the index.html page
@app.route('/')
def index():
    return render_template('index.html')  # Render index.html

# Route for handling form submissions
@app.route('/submit_message', methods=['POST'])
def submit_message():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    message = request.form.get('message')

    # Debug: print submitted form data
    print(f"Inserting: {fullname}, {email}, {message}")  # Check what is being captured

    # Connect to MySQL and insert form data
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # SQL query to insert data
        cursor.execute("INSERT INTO contact_messages (fullname, email, message) VALUES (%s, %s, %s)", 
                       (fullname, email, message))
        connection.commit()  # Commit the transaction
        
        # Debug: print confirmation
        print("Data inserted successfully")

        return redirect(url_for('success'))

    except mysql.connector.Error as err:
        # Debug: print error message
        print(f"Error: {err}")
        return "Failed to submit message.", 500

    finally:
        # Close connection and cursor
        if connection.is_connected():
            cursor.close()
            connection.close()

# Route for success page after message submission
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

if __name__ == '__main__':
    app.run(debug=True)
