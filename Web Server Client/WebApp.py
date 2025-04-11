import os
import io
import sys
import socket
import json
from datetime import datetime, time
import time
from flask import Flask, request, send_file, jsonify, render_template, redirect, url_for, session, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

sys.path.append(os.path.join(os.path.dirname(__file__), '../tinyscpi'))
from tinySCPI import execute_from_file, user_input, scan_raw_points


app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "data/"
IMAGE_FILE = os.path.join(UPLOAD_FOLDER, "screen.png")
LOG_FILE = os.path.join(UPLOAD_FOLDER, "log_file_history.txt")
CSV_FILE = os.path.join(UPLOAD_FOLDER, "data_trace.csv")
LOCK_FILE = os.path.join(UPLOAD_FOLDER, "lock_file.lock")
LOGIN_LOCK = os.path.join(UPLOAD_FOLDER, "login.lock")

# if os.path.exists(LOGIN_LOCK):
#     os.remove(LOGIN_LOCK)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load password from config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)
CORRECT_PASSWORD = config["password"]

execution_count = 0

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    id = "admin"


@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return User()
    return None


def is_logged_in():
    """Check if someone is already logged in globally."""
    return os.path.exists(LOGIN_LOCK)


def set_login_lock():
    """Mark the system as having an active user."""
    with open(LOGIN_LOCK, "w") as f:
        f.write("locked")


def release_login_lock():
    """Release the login lock when the user logs out."""
    for file_path in [LOG_FILE, CSV_FILE,IMAGE_FILE,"data/commands.txt",LOGIN_LOCK]:
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        password = request.form.get("password", "")

        if is_logged_in():
            return render_template("index.html", error="Another user is already logged in. Try again later.")

        if password != CORRECT_PASSWORD:
            return render_template("index.html", error="Incorrect password!")

        user = User()
        login_user(user)
        session["logged_in"] = True
        set_login_lock()
        return redirect(url_for("home"))

    return render_template("index.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("logged_in", None)
    release_login_lock()
    return redirect(url_for("login"))


@app.route("/home")
@login_required
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload_file():

    filename = request.args.get("file")
    if filename:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            return jsonify({"filename": filename, "content": content})
        else:
            return jsonify({"error": f"File {filename} not found"}), 404

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    return jsonify({"filename": file.filename, "content": content})

import csv

@app.route("/execute", methods=["POST"])
@login_required
def execute():
    global execution_count  # Use the in-memory variable to track execution count

    data = request.json
    commands = data.get("commands", "").strip()

    command_file = os.path.join(UPLOAD_FOLDER, "commands.txt")
    with open(command_file, "w") as f:
        f.write(commands)

    class Tee:
        def __init__(self, *streams):
            self.streams = streams

        def write(self, msg):
            for stream in self.streams:
                stream.write(msg)

        def flush(self):
            for stream in self.streams:
                stream.flush()

    log_stream = io.StringIO()

    execution_count += 1  # Increment execution number
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log_file:
        sys.stdout = Tee(sys.stdout, log_stream, log_file)

        # Log header with commands
        log_file.write(f"\n===== Execution {execution_count} - {timestamp} =====\n")
        log_file.write(f"Commands Ran:\n{commands}\n")
        log_file.write("-" * 40 + "\n")

        image_url = None
        graph_data = None

        try:
            logs = execute_from_file(command_file)
            logs = log_stream.getvalue()
        except Exception as e:
            logs = f"Error executing commands: {str(e)}"

        sys.stdout = sys.__stdout__

    scan_raw_points(savedata=True, filename="data_trace.csv", save_dir=UPLOAD_FOLDER)

    # Check if the CSV file exists and read the data
    if os.path.exists(CSV_FILE):
        graph_data = []
        with open(CSV_FILE, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                graph_data.append({
                    'x': float(row['x']),
                    'y': float(row['y'])
                })

    time.sleep(2)

    if "CONF:CAPT" in commands:
        try:
            user_input("CONF:CAPT")
            if os.path.exists(IMAGE_FILE):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                image_url = f"/image/{os.path.basename(IMAGE_FILE)}?t={timestamp}"
            else:
                logs += "\nImage capture failed: File not found."
        except Exception as e:
            logs += f"\nError capturing image: {str(e)}"

    return jsonify({
        "logs": logs,
        "image_url": image_url,
        "graph_data": graph_data
    })

@app.route("/image/<filename>")
@login_required
def get_image(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="image/png")
    return "Image not found", 404


@app.route("/download_log")
@login_required
def download_log():
    if os.path.exists(LOG_FILE):
       return send_file(LOG_FILE, as_attachment=True, download_name="log_file_history.txt")
    else:
        return jsonify({"error": "CSV file not found."}), 404


@app.route("/download_csv")
@login_required
def download_csv():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True, download_name="data_trace.csv")
    else:
        return jsonify({"error": "CSV file not found."}), 404

@app.route("/force_logout", methods=["POST"])
def force_logout():
    """Force logout if the user closes the tab."""
    release_login_lock()

    if current_user.is_authenticated:
        logout_user()
        session.pop("logged_in", None)
        release_login_lock()
    return "", 204

if __name__ == "__main__":
    release_login_lock()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        HOST = s.getsockname()[0]

    PORT = 5000

    print(f"Flask server is running at http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=True)
