# Online Subscription Portal (Flask + MySQL)

## 📌 Project Overview

This is a simple subscription-based web application built using Flask and MySQL.  
Users can register, log in, browse offerings, and subscribe to available services.

---

## 🚀 Features

- User registration with password hashing
- Secure login system using sessions
- Browse available offerings
- Subscribe to offerings using AJAX
- Personal dashboard showing user subscriptions
- REST API endpoint for offerings

---

## 🛠️ Technologies Used

- Python (Flask)
- MySQL (flask-mysqldb)
- HTML / CSS (Bootstrap 5)
- JavaScript (AJAX)
- Werkzeug (password hashing)

---

## 📁 Project Structure

```

project/
│── app.py
│── config.py
│── database.py
│── requirements.txt
│── README.md
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── offerings.html
│
├── static/
│   └── js/
│       └── main.js

```

---

## ⚙️ How to Run the Project Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Setup MySQL Database

Create database:

```sql
CREATE DATABASE subscription_portal;
```

Create tables:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255)
);

CREATE TABLE offerings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    description TEXT
);

CREATE TABLE subscriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    offering_id INT,
    date DATETIME
);
```

Insert sample data:

```sql
INSERT INTO offerings(title, description)
VALUES
('Full-Stack Web Development', 'Learn modern web development'),
('Database Systems', 'Learn SQL and database design'),
('AI Fundamentals', 'Introduction to machine learning');
```

---

### 3. Configure Database

Edit `config.py`:

```python
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "subscription_portal"
```

---

### 4. Run the application

```bash
python app.py
```

Open in browser:

```
http://127.0.0.1:5000
```

---

## 🔑 Test Login (for examiner)

```
Email: admin
Password: admin
```

_(Make sure to insert this user manually)_

---

## 🌐 API Endpoints

### Get all offerings

```
GET /api/offerings
```

### Subscribe to offering

```
POST /ajax/subscribe
Body: { "offering_id": 1 }
```

---

## 👨‍💻 Developer Notes

- Sessions are used for authentication
- Passwords are securely hashed using Werkzeug
- AJAX is used for subscription without page reload
- MySQL handles all persistent data
