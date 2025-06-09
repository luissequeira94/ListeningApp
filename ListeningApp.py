from flask import Flask, request
import configparser
import logging
import os
from waitress import serve
import socket
import threading

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Read settings
port = int(config.get('server', 'port', fallback=5000))
output_mode = config.get('server', 'output', fallback='prompt').lower()
log_file = config.get('log', 'log_file', fallback='log.txt')
mode = config.get('server', 'mode', fallback='rest').lower()

# Ensure log file directory exists
log_file_path = os.path.abspath(log_file)
log_dir = os.path.dirname(log_file_path)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging
logger = logging.getLogger('TrafficLogger')
logger.setLevel(logging.INFO)
# Ensure log directory exists
log_path = os.path.abspath(log_file)
log_dir = os.path.dirname(log_path)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logger setup
logger = logging.getLogger('ServerLogger')
logger.setLevel(logging.INFO)
logger.handlers.clear()
if output_mode == 'log':
    fh = logging.FileHandler(log_path)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logger.addHandler(fh)

def output(message):
    if output_mode == 'prompt':
        print(message)
    else:
        logger.info(message)
        
# Flask REST Server
def run_rest_server():
    app = Flask(__name__)

    @app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    @app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    def catch_all(path):
        info = f"""REST Request:
Method: {request.method}
Path: /{path}
Headers: {dict(request.headers)}
Body: {request.get_data(as_text=True)}"""
        output(info)
        return 'REST: Received', 200

    output(f"Starting REST server on port {port}")
    serve(app, host="0.0.0.0", port=port)

# Socket Server
def run_socket_server():
    def handle_client(conn, addr):
        buffer = ""
        with conn:
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                buffer += data
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    output(f"Socket Message from {addr}: {message.strip()}")
                    conn.sendall(b"Socket: Message received\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('0.0.0.0', port))
        s.listen()
        output(f"Socket server listening on port {port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# Entry Point
if __name__ == '__main__':
    try:
        if mode == 'rest':
            run_rest_server()
        elif mode == 'socket':
            run_socket_server()
        else:
            output(f"Unsupported mode: {mode}")
    except Exception as e:
        output("Unknown error occured: {e}")