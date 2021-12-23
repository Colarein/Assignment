import socket


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port=1234

serverSocket.bind(('192.168.0.30', port))

print("Server listening on port "+ str(port))


# queue up to 5 requests

serverSocket.listen()

connection,addr = serverSocket.accept()

while True:

    data = connection.recv(1024)

    print(data.decode('ascii'))

    if not data:

        break
