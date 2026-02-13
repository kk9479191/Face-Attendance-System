from flask import Flask, render_template, request, redirect, url_for
import subprocess
import csv
import os

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "1234"

# LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    records = []

    if os.path.exists("attendance.csv"):
        with open("attendance.csv", "r") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                records.append(row)

    return render_template("dashboard.html", records=records)


# START CAMERA
@app.route("/start-camera")
def start_camera():
    subprocess.Popen(["python", "main.py"])
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
