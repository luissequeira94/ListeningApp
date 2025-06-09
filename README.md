# 🛰️ Python Multi-Mode Traffic Listener

A lightweight Python server that listens for incoming **REST** or **WebSocket** traffic on a specified port. Outputs can be printed to the console or logged to a file, based on configuration.

---

## ⚙️ Features

- 🔁 Multi-mode support: **REST** and **WebSocket**
- 📄 Logs to file or prints to terminal
- 🧩 Configurable via `config.ini`
- 🧵 Threaded handling for socket clients
- 📡 Monitors all traffic on a specified port

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/luissequeira94/ListeningApp.git
cd ListeningApp
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Edit the config.ini file:
```bash
[server]
port = 5000         ; Port to listen on
output = prompt     ; Options: 'prompt' or 'log'
mode = rest         ; Options: 'rest', 'socket', 'soap'

[log]
log_file = log.txt  ; Log file path (used if output = log)
```

## 🌐 Modes Explained
### REST Mode
A Flask server that echoes all HTTP requests.

```bash
python ListeningApp.py
```

Accepts GET, POST, PUT, DELETE, PATCH  
Captures method, headers, and body

Example using curl:

```bash
curl -X POST http://localhost:5000/test -d "hello=world"
```

### Socket Mode
A TCP server that reads newline-terminated messages.  
Use any TCP client to send messages.

> Responds with Socket: "Message received"

Example using Python client:
```bash
import socket
s = socket.create_connection(('localhost', 5000))
s.sendall(b'Hello from client!\n')
print(s.recv(1024).decode())
```

Example Logs
```bash
2025-06-09 14:33:22,100 - REST Request:
Method: POST
Path: /test
Headers: {'Content-Type': 'application/x-www-form-urlencoded', ...}
Body: hello=world
```

## 📁 Project Structure
```bash
.
├── ListeningApp.py          # Main application
├── config.ini      # Configuration file
└── log.txt         # Log file (created at runtime if needed)
```

## 📜 License
MIT License. See LICENSE file for details.

## 🤝 Contributing
Pull requests are welcome.  
For major changes, please open an issue first to discuss what you would like to change.