import socket

# Setup socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 6789))  # Bind to port 6789
server_socket.listen(1)  # Listen to 1 client at a time
print("Server is ready to receive...")

while True:
    connection_socket, addr = server_socket.accept()
    message = connection_socket.recv(1024).decode()
    print("Request:", message)

    # Ambil nama file
    try:
        filename = message.split()[1]
        with open(filename[1:], 'rb') as f:  # [1:] untuk menghapus '/'
            output_data = f.read()

        header = 'HTTP/1.1 200 OK\r\n\r\n'
        connection_socket.send(header.encode())
        connection_socket.send(output_data)
    except FileNotFoundError:
        header = 'HTTP/1.1 404 Not Found\r\n\r\n'
        body = '<html><body><h1>404 Not Found</h1></body></html>'
        connection_socket.send(header.encode())
        connection_socket.send(body.encode())

    connection_socket.close()
