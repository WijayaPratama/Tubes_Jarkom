import sys
import socket

def connect_to_server():
    if len(sys.argv) != 4:
        print("Usage: client.py <server_host> <server_port> <filename>")
        return
    
    server_adr = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_adr, server_port))
    except Exception:
        print(f"Error server address: {server_adr} with server port: {server_port} not found")
        print("make sure your flag is correct")
        print("the correct usage: client.py <server_host> <server_port> <filename>")

    host = f"{server_adr}:{server_port}"
    request = f"GET /{filename} HTTP/1.1\r\nHost: {host}\r\n\r\n"

    try:
        client_socket.sendall(request.encode())

        response = b""
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response += chunk

        response_text = response.decode()
        print(response_text.strip())
    except Exception as e:
        print("Error while sending/receiving data:", e)
    finally:
        client_socket.close()

if __name__ == "__main__":
    connect_to_server()
