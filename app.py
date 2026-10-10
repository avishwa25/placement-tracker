from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import date
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

STATUSES = ["Applied", "Shortlisted", "Interview", "Offer", "Rejected"]


def row_to_dict(row):
    row["applied_on"] = str(row["applied_on"]) if row["applied_on"] else ""
    return row


@app.route("/applications")
@login_required
def applications_page():
    return render_template("applications.html", statuses=STATUSES)


@app.route("/api/applications", methods=["GET"])
@login_required
def list_applications():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT id, company_name, job_role, job_link, status, applied_on, notes "
        "FROM applications WHERE student_id = %s ORDER BY id DESC",
        (session["student_id"],),
    )
    rows = [row_to_dict(r) for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(rows)


@app.route("/api/applications", methods=["POST"])
@login_required
def add_application():
    data = request.get_json(silent=True) or {}
    company = (data.get("company_name") or "").strip()
    role = (data.get("job_role") or "").strip()
    if not company or not role:
        return jsonify({"error": "Company and role are required."}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO applications "
        "(student_id, company_name, job_role, job_link, applied_on, notes) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (
            session["student_id"],
            company,
            role,
            (data.get("job_link") or "").strip() or None,
            data.get("applied_on") or date.today().isoformat(),
            (data.get("notes") or "").strip() or None,
        ),
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"id": new_id}), 201


@app.route("/api/applications/<int:app_id>", methods=["PUT"])
@login_required
def update_application(app_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    if status not in STATUSES:
        return jsonify({"error": "Invalid status."}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE applications SET status = %s WHERE id = %s AND student_id = %s",
        (status, app_id, session["student_id"]),
    )
    conn.commit()
    changed = cur.rowcount
    cur.close()
    conn.close()
    if changed == 0:
        return jsonify({"error": "Not found."}), 404
    return jsonify({"ok": True})


@app.route("/api/applications/<int:app_id>", methods=["DELETE"])
@login_required
def delete_application(app_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM applications WHERE id = %s AND student_id = %s",
        (app_id, session["student_id"]),
    )
    conn.commit()
    deleted = cur.rowcount
    cur.close()
    conn.close()
    if deleted == 0:
        return jsonify({"error": "Not found."}), 404
    return jsonify({"ok": True})


@app.route("/api/stats")
@login_required
def stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT status, COUNT(*) FROM applications "
        "WHERE student_id = %s GROUP BY status",
        (session["student_id"],),
    )
    counts = {s: 0 for s in STATUSES}
    for status, n in cur.fetchall():
        counts[status] = n
    cur.close()
    conn.close()
    return jsonify(counts)

if __name__ == "__main__":
    app.run(debug=True) 