from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_mail import Mail, Message
import random
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sivapprakash1634@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'zlkr jowl nyfw osgy'  # Replace with your password
app.config['MAIL_DEFAULT_SENDER'] = 'your_email@gmail.com'

mail = Mail(app)

# MySQL database connection configuration
db_config = {
    'user': 'root',
    'password': 'hsakarppavis@1634',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'slot_booking'  # Replace with your database name
}

HR_EMAIL = 'sivapp.ad.2021@snsce.ac.in'  # Replace with the actual HR email

# Predefined users
users = {
    "siva.c.ihub@snsgroups.com": "zxcvbnm,./"
}

# Authentication route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate credentials
        if email in users and users[email] == password:
            session['user'] = email
            flash("Login successful!", "success")
            return redirect(url_for('select_dates'))
        else:
            flash("Invalid email or password.", "danger")

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# Ensure authentication for protected routes
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

# Redirect home page to login
@app.route('/')
def home():
    
    return redirect(url_for('login'))
# Apply login_required decorator to protected routes
@app.route('/select_dates', methods=['GET', 'POST'])
@login_required
def select_dates():
    # Your select_dates logic here...
    if request.method == 'POST':
        selected_dates = request.form.getlist('dates')
        if not selected_dates:
            return "No dates selected."

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
        except mysql.connector.Error as err:
            return "Database connection error."

        for date in selected_dates:
            try:
                cursor.execute('INSERT INTO slots (date, status) VALUES (%s, %s)', (date, 'available'))
            except mysql.connector.Error as err:
                pass

        conn.commit()
        cursor.close()
        conn.close()

        link = url_for('select_slots', dates=selected_dates, _external=True)
        msg = Message('Selected Dates for Slot Booking', recipients=[HR_EMAIL])
        msg.body = f"Click here to select time slots: {link}"
        mail.send(msg)

        return redirect(url_for('select_slots', dates=selected_dates))

    today = datetime.now()
    next_30_days = [(today + timedelta(days=i)).date() for i in range(15)]
    return render_template('select_dates.html', next_30_days=next_30_days)

# Placeholder for the select_slots route
@app.route('/select_slots', methods=['GET', 'POST'])
def select_slots():
    selected_dates = request.args.getlist('dates')  # Get dates from the URL parameters

    if request.method == 'POST':
        selected_slots = request.form.getlist('timeslots')

        if not selected_slots:
            return "No slots selected."

        # Connect to MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert each selected slot into the database
        for slot in selected_slots:
            date_str, time_str = slot.split(' ', 1)
            time_obj = datetime.strptime(time_str, '%I:%M %p').time()
            time_formatted = time_obj.strftime('%H:%M:%S')

            try:
                cursor.execute('INSERT INTO slots (date, time, status) VALUES (%s, %s, %s)', 
                               (date_str, time_formatted, 'available'))
                print(f"Inserted date: {date_str}, time: {time_formatted}, status: available")
            except mysql.connector.Error as err:
                print(f"Error inserting data: {err}")

        conn.commit()
        cursor.close()
        conn.close()

        return "Slots saved successfully!"

    # Generate time slots for each selected date
    time_slots = {}  # Use a dictionary to group time slots by date
    for date in selected_dates:
        time_slots[date] = []
        for hour in range(10, 17):  # 10 AM to 4 PM
            time_slot = f"{date} {hour}:00 PM"
            time_slots[date].append(time_slot)

    # Fetch available slots from the database for selected dates
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    if selected_dates:
        placeholders = ', '.join(['%s'] * len(selected_dates))
        sql = f"SELECT date, time FROM slots WHERE status = 'available' AND date IN ({placeholders})"
        cursor.execute(sql, selected_dates)
    else:
        sql = "SELECT date, time FROM slots WHERE status = 'available'"
        cursor.execute(sql)

    available_slots = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()

    # Format time slots and mark available slots
    formatted_slots = {}  # Use a dictionary to group formatted slots by date
    for date in time_slots:
        formatted_slots[date] = []
        for time in time_slots[date]:
            # Remove the 'PM' from the time string
            time = time.replace(" PM", "")
            time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M').time()  # Correct format
            formatted_time = time_obj.strftime('%I:%M %p')  
            is_available = (date, formatted_time) in available_slots
            formatted_slots[date].append((formatted_time, is_available))

    return render_template('select_slots.html', formatted_slots=formatted_slots)

if __name__ == '__main__':
    app.run(debug=True)
