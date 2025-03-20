import socket
import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '../tinyscpi'))

# Now import the execute_from_file function
from tinySCPI import execute_from_file, capture, scan_raw_points

#HOST = '0.0.0.0'  # Listen on all interfaces
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    HOST = s.getsockname()[0]
PORT = 5000
DATA_DIR = 'data'

def handle_client(conn):
    try:
        request = conn.recv(1024).decode()
        if request == "GET_CSV":
            send_file(conn, os.path.join(DATA_DIR, "trace.csv"))
        elif request == "GET_IMAGE":
            send_file(conn, os.path.join(DATA_DIR, "screen.jpg"))
        elif request == "SEND_SCRIPT":
            receive_file(conn, os.path.join(DATA_DIR, "script.txt"))
    finally:
        conn.close()

def send_file(conn, filepath):
    if os.path.exists(filepath):
        conn.send(b"EXISTS")
        print(f"Sending file: {filepath}")  # Debug log
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                conn.send(chunk)
                print(f"Sent {len(chunk)} bytes")  # Debug log
    else:
        conn.send(b"NO_FILE")
        print(f"File not found: {filepath}")  # Debug log

def receive_file(conn, filepath):
    file_type = conn.recv(1024).decode()
    file_extension = None
    if file_type == "SEND_SCRIPT":
        file_extension = '.txt'
    with open(filepath, "wb") as f:
        while chunk := conn.recv(4096):
            f.write(chunk)
    print(f"Received file: {filepath}")
    if file_extension == '.txt':
        execute_from_file(f"data/{filepath}")
        capture("screenshot.jpeg")

def start_server():
    os.makedirs(DATA_DIR, exist_ok=True)  # Ensure the data directory exists
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, _ = server.accept()
            handle_client(conn)

if __name__ == "__main__":
    start_server()
