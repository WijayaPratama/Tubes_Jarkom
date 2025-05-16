import socket
import threading

def handle_client (connection_socket):
    message = connection_socket.recv(1024).decode()
    try:
        filename = message.split()[1]
        with open(filename[1:], 'rb') as f:  # [1:] untuk menghapus '/'
            output_data = f.read()
        header = f'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {len(output_data)}\r\nConnection: close\r\n\r\n'
        connection_socket.send(header.encode())
        connection_socket.send(output_data)
    except FileNotFoundError:
        body = '<html><body><h1>Error page</h1></body></html>'
        header = f'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: {len(body.encode())}\r\nConnection: close\r\n\r\n'
        connection_socket.send(header.encode())
        connection_socket.send(body.encode())
    except IndexError:
        print("Error opening file, bad request")
    except Exception as e:
        print(f"error:{e}")
    finally:
        connection_socket.close()

if __name__ == "__main__":
    # Setup socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 6789))  # Bind to port 6789
    server_socket.listen(5)
    print("Server is ready to receive...")

    while True:
        connection_socket, addr = server_socket.accept()
        print(f"Connection from {addr} opened")
        t = threading.Thread(target=handle_client, args=(connection_socket,))
        t.start()
        print(f"Connection from {addr} closed")
