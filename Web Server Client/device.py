from flask import Flask, request, send_file, jsonify, render_template
import io
import os
import sys
import socket
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../tinyscpi'))
from tinySCPI import execute_from_file, user_input

app = Flask(__name__)
UPLOAD_FOLDER = "data/"
IMAGE_FILE = os.path.join(UPLOAD_FOLDER, "screen.png")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST", "GET"])
def upload_file():
    filename = request.args.get("file")
    if filename:
        # Load predefined file
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                content = f.read()
            return jsonify({"filename": filename, "content": content})
        else:
            return jsonify({"error": f"File {filename} not found"}), 404

    # Normal file upload
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
    data = request.json
    commands = data.get("commands", "")

    # Save edited commands to a file
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
    sys.stdout = Tee(sys.stdout, log_stream)

    image_url = None
    try:
        # Execute commands using tinySCPI
        logs = execute_from_file(command_file)
        logs = log_stream.getvalue()
    except Exception as e:
        logs = f"Error executing commands: {str(e)}"

    sys.stdout = sys.__stdout__

    if "CONF:CAPT" in commands:
        try:
            user_input("CONF:CAPT")
            if os.path.exists(IMAGE_FILE):
                # Add timestamp to the image URL to force refresh
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                image_url = f"/image/{os.path.basename(IMAGE_FILE)}?t={timestamp}"
            else:
                logs += "\nImage capture failed: File not found."
        except Exception as e:
            logs += f"\nError capturing image: {str(e)}"

    return jsonify({"logs": logs, "image_url": image_url})


@app.route("/image/<filename>")
def get_image(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype="image/png")
    return "Image not found", 404


if __name__ == "__main__":
    # Use socket to get the local machine's IP address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))  # Connect to Google's DNS server
        HOST = s.getsockname()[0]  # Get the local IP address used for the connection

    PORT = 5000  # Port remains the same
    DATA_DIR = 'data'  # Directory for file uploads

    print(f"Flask server is running at http://{HOST}:{PORT}")

    # Run the Flask app
    app.run(host=HOST, port=PORT, debug=True)