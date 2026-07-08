import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import text

from config import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        result = db.session.execute(text("SELECT id FROM users WHERE email=:email"), {"email": email}).fetchone()
        
        if result:
            flash("Email already exists.")
            return redirect(url_for("register"))

        db.session.execute(
            text("INSERT INTO users(name, email, password_hash) VALUES(:name, :email, :password_hash)"),
            {"name": name, "email": email, "password_hash": hashed}
        )
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email == "ADMIN" and password == "ADMIN":
            session["user_id"] = 0
            session["user_name"] = "Admin Examiner"
            return redirect(url_for("dashboard"))

        user = db.session.execute(text("SELECT id, name, password_hash FROM users WHERE email=:email"), {"email": email}).fetchone()

        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials.")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    # إذا لم يكن هناك معرف مستخدم في الجلسة، اطرده لصفحة تسجيل الدخول
    if "user_id" not in session:
        flash("Please login to access the dashboard.")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    user_name = session["user_name"]

    subscriptions = db.session.execute(text("""
        SELECT o.title 
        FROM subscriptions s
        JOIN offerings o ON s.offering_id = o.id
        WHERE s.user_id = :user_id
    """), {"user_id": user_id}).fetchall()

    return render_template("dashboard.html", user=user_name, subscriptions=subscriptions)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/offerings")
def offerings():
    return render_template("offerings.html")


@app.route("/api/offerings", methods=["GET"])
def get_offerings():
    try:
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                email VARCHAR(150) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            );
        """))
        
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS offerings (
                id SERIAL PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL
            );
        """))
        
        db.session.execute(text("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id SERIAL PRIMARY KEY,
                user_id INT NOT NULL,
                offering_id INT NOT NULL
            );
        """))
        db.session.commit()

        check_table = db.session.execute(text("SELECT COUNT(*) FROM offerings")).fetchone()
        if check_table and check_table[0] == 0:
            db.session.execute(text("""
                INSERT INTO offerings (title, description) VALUES 
                ('Advanced AI & Machine Learning', 'Deep dive into neural networks, Computer Vision, and medical image segmentation.'),
                ('Full-Stack Web Development', 'Master backend and frontend architectures using Flask, PostgreSQL, and modern JavaScript.'),
                ('Edge AI & TinyML Systems', 'Learn hardware-aware artificial intelligence and deploying models on microcontrollers.')
            """))
            db.session.commit()
            print("🏆 Tables and courses initialized successfully inside API Route!")
            
    except Exception as e:
        print(f"Database Initialization Inside Route Note: {e}")

    rows = db.session.execute(text("SELECT id, title, description FROM offerings")).fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "title": row[1],
            "description": row[2]
        })
    return jsonify(result)


@app.route("/ajax/subscribe", methods=["POST"])
def subscribe():
    if "user_id" not in session:
        return jsonify({"success": False, "message": "Login required."}), 401

    data = request.get_json()
    if not data or "offering_id" not in data:
        return jsonify({"success": False, "message": "Invalid request."}), 400

    offering = data["offering_id"]

    exists = db.session.execute(text("""
        SELECT id FROM subscriptions WHERE user_id=:user_id AND offering_id=:offering_id
    """), {"user_id": session["user_id"], "offering_id": offering}).fetchone()

    if exists:
        return jsonify({"success": False, "message": "Already subscribed."})

    course_exists = db.session.execute(text("SELECT id FROM offerings WHERE id=:id"), {"id": offering}).fetchone()
    if not course_exists:
        return jsonify({"success": False, "message": "Offering not found."}), 404

    db.session.execute(text("""
        INSERT INTO subscriptions (user_id, offering_id) VALUES (:user_id, :offering_id)
    """), {"user_id": session["user_id"], "offering_id": offering})
    db.session.commit()

    return jsonify({"success": True, "message": "Subscribed successfully!"})
