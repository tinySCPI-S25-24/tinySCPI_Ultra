import time
import os
import io
import sys
import socket
from datetime import datetime
from flask import Flask, request, send_file, jsonify, render_template

sys.path.append(os.path.join(os.path.dirname(__file__), '../tinyscpi'))
from tinySCPI import execute_from_file, user_input

app = Flask(__name__)
UPLOAD_FOLDER = "data/"
IMAGE_FILE = os.path.join(UPLOAD_FOLDER, "screen.png")
LOG_FILE = os.path.join(UPLOAD_FOLDER, "log_file_history.txt")
LOCK_FILE = os.path.join(UPLOAD_FOLDER, "lock_file.lock")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Reset log file on server start
with open(LOG_FILE, "w") as f:
    f.write("===== Log File History =====\n")

# Initialize execution counter (in-memory, not persisted)
execution_count = 0


def is_locked():
    """Check if the system is locked."""
    return os.path.exists(LOCK_FILE)


def create_lock():
    """Create a lock file."""
    with open(LOCK_FILE, "w") as lock:
        lock.write("locked")


def release_lock():
    """Remove the lock file."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


@app.route("/")
def home():
    if is_locked():
        return render_template("system_locked.html")
    return render_template("index.html")


@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    if is_locked():
        return jsonify({"error": "System is currently in use. Please try again later."}), 403

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


@app.route("/execute", methods=["POST"])
def execute():
    global execution_count  # Use the in-memory variable to track execution count

    if is_locked():
        return jsonify({"error": "System is currently in use. Please try again later."}), 403

    # Lock the system to prevent other users from accessing it
    create_lock()

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
        try:
            logs = execute_from_file(command_file)
            logs = log_stream.getvalue()
        except Exception as e:
            logs = f"Error executing commands: {str(e)}"

        sys.stdout = sys.__stdout__

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

    # Release the lock after execution is complete
    release_lock()

    return jsonify({"logs": logs, "image_url": image_url})


@app.route("/image/<filename>")
def get_image(filename):
    if is_locked():
        return jsonify({"error": "System is currently in use. Please try again later."}), 403

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="image/png")
    return "Image not found", 404


@app.route("/download_log")
def download_log():
    if is_locked():
        return jsonify({"error": "System is currently in use. Please try again later."}), 403

    return send_file(LOG_FILE, as_attachment=True, download_name="log_file_history.txt")


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        HOST = s.getsockname()[0]

    PORT = 5000

    print(f"Flask server is running at http://{HOST}:{PORT}")
    app.run(host=HOST, port=PORT, debug=True)
