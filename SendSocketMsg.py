import socket

s = socket.create_connection(('localhost', 5000))
s.sendall(b'Hello World!\n')
print(s.recv(1024).decode())
