import socket
import os

# Specify the server's IP manually
SERVER_IP = '192.168.0.106'  # Replace this with the server's IP
PORT = 5000  # Main communication port
RECEIVED_DIR = 'data'

os.makedirs(RECEIVED_DIR, exist_ok=True)

def request_file(file_type):
    """Requests a file (CSV, image, or console log) from the server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    client.send(file_type.encode())

    response = client.recv(1024)
    print(f"Response from server: {response}")  # Debug log

    if response == b"EXISTS":
        filename = os.path.join(RECEIVED_DIR, {
            "GET_CSV": "trace.csv",
            "GET_IMAGE": "screen.png",
            "GET_CONSOLE": "console.log"
        }.get(file_type, "unknown_file"))

        print(f"Receiving file: {filename}")  # Debug log
        with open(filename, 'wb') as f:
            while True:
                chunk = client.recv(4096)
                if not chunk:
                    break  # Stop when no more data
                f.write(chunk)
                print(f"Received {len(chunk)} bytes")  # Debug log

        print(f"File {filename} received successfully")
    else:
        print(f"{file_type} not found on server.")  # Debug log

    client.close()

def send_script(script_path):
    """Sends a script file to the server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))
    client.send(b"SEND_SCRIPT")

    with open(script_path, 'rb') as f:
        client.sendall(f.read())

    client.close()
    print(f"Script sent successfully: {script_path}")

