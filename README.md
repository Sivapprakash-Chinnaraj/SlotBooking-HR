# Interview Slot Booking System - HR

This Flask-based application manages interview slot bookings, automates notifications, and allows users to select dates and time slots for interviews. It supports MySQL as the database and uses Flask-Mail for email notifications.

## Features

- **User Authentication:** Secure login/logout functionality.
- **Date Selection:** Users can select available dates for interviews.
- **Time Slot Selection:** Choose available time slots for selected dates.
- **Database Integration:** MySQL database to store selected dates, time slots, and their statuses.
- **Email Notifications:** Sends links to HR for time slot selection and updates.
- **Dynamic Slot Management:** Automatically generates and displays available time slots for selected dates.

## Prerequisites

- Python 3.8+
- MySQL Database
- SMTP Email Account (e.g., Gmail)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/interview-slot-booking.git
   cd interview-slot-booking
   ```

2. **Set Up a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database:**
   - Log in to your MySQL server and create a database:
     ```sql
     CREATE DATABASE slot_booking;
     ```
   - Update `db_config` in the code with your MySQL credentials.

5. **Set Up Tables:**
   Use the following SQL commands to create necessary tables:

   ```sql
   CREATE TABLE slots (
       id INT AUTO_INCREMENT PRIMARY KEY,
       date DATE NOT NULL,
       time TIME,
       status ENUM('available', 'booked') DEFAULT 'available'
   );
   ```

6. **Configure Email Credentials:**
   Update the following lines in the code with your email details:
   ```python
   app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
   app.config['MAIL_PASSWORD'] = 'your-app-password'
   HR_EMAIL = 'hr-email@example.com'
   ```

7. **Run the Application:**
   ```bash
   python app.py
   ```

8. **Access the Application:**
   Open your browser and visit `http://127.0.0.1:5000`.

## Database Queries

### Create Tables

#### `slots` Table
```sql
CREATE TABLE slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    time TIME,
    status ENUM('available', 'booked') DEFAULT 'available'
);
```

### Sample Data
Insert sample slots:
```sql
INSERT INTO slots (date, time, status) VALUES
('2024-11-20', '10:00:00', 'available'),
('2024-11-20', '11:00:00', 'available'),
('2024-11-21', '14:00:00', 'available'),
('2024-11-21', '15:00:00', 'available');
```

### View Data
- To view available slots:
  ```sql
  SELECT * FROM slots WHERE status = 'available';
  ```

## Usage

1. **Login:**
   - Access the login page at `/login` and enter the credentials.

2. **Select Dates:**
   - After login, navigate to `/select_dates` to choose available dates.

3. **Select Time Slots:**
   - Click the link sent via email to navigate to `/select_slots` and choose time slots.

4. **Check Slot Status:**
   - Admins can query the database to view booked and available slots.

## Troubleshooting

- **Email Issues:**
  - Ensure SMTP credentials are correct.
  - Use an app-specific password if using Gmail.

- **Database Connection:**
  - Verify that the MySQL server is running and the database credentials are correctly configured.

- **Common Errors:**
  - Missing tables: Ensure the `slots` table is created as described.
  - Port conflicts: Use a different port when running the application if `5000` is already in use.

## Future Enhancements

- Add user registration functionality.
- Support for additional recruitment stages.
- Integration with calendar tools (e.g., Google Calendar).

---
