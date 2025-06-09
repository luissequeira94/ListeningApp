from flask import Flask, request
import configparser
import logging
import os
from waitress import serve

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Read settings
port = int(config.get('server', 'port', fallback=5000))
output_mode = config.get('server', 'output', fallback='prompt').lower()
log_file = config.get('log', 'log_file', fallback='log.txt')

# Ensure log file directory exists
log_file_path = os.path.abspath(log_file)
log_dir = os.path.dirname(log_file_path)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set up logging
logger = logging.getLogger('TrafficLogger')
logger.setLevel(logging.INFO)

if output_mode == 'log':
    file_handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
else:
    # If using prompt, ensure no file handlers interfere
    logging.getLogger().handlers.clear()

# Create Flask app
app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def catch_all(path):
    # Request info
    info = f"""Method: {request.method}
Path: /{path}
Headers: {dict(request.headers)}
Body: {request.get_data(as_text=True)}
"""
    if output_mode == 'prompt':
        print(info)
    else:
        logger.info(info)
    return 'Received', 200

if __name__ == '__main__':
    print(f"Starting server on port {port}, output mode: {output_mode}")
    #app.run(host='0.0.0.0', port=port)
    serve(app, host="0.0.0.0", port=port)