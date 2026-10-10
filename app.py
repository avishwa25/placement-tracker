from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

import config
from db import get_connection

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "student_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
def home():
    if "student_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or len(password) < 6:
            flash("Fill all fields. Password must be at least 6 characters.")
            return render_template("register.html")

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO students (name, email, password_hash) VALUES (%s, %s, %s)",
                (name, email, generate_password_hash(password)),
            )
            conn.commit()
        except mysql.connector.IntegrityError:
            flash("That email is already registered.")
            return render_template("register.html")
        finally:
            cur.close()
            conn.close()

        flash("Account created. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM students WHERE email = %s", (email,))
        student = cur.fetchone()
        cur.close()
        conn.close()

        if student and check_password_hash(student["password_hash"], password):
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            return redirect(url_for("dashboard"))

        flash("Wrong email or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True) 