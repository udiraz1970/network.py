import socket
from datetime import datetime
import random

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 8820))
server_socket.listen()
print("Server is up and running")
(client_socket, client_address) = server_socket.accept()
print("Client connected")
data = ""
while True:
    data = client_socket.recv(1024).decode()
    print("Client sent: " + data)
    if data == "NAME":
        data = "My name is Udi's Server"
    elif data == "TIME":
        now = datetime.now()
        data = now.strftime("%H:%M:%S")
    elif data == "RAND":
        data = str(random.randint(1, 10))
    elif data == 'QUIT':
        print("closing client socket now...")
        client_socket.send("Bye".encode())
        break

    client_socket.send(data.encode())

client_socket.close()
server_socket.close()