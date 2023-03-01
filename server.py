import socket
import threading

def handle_client(client_socket, client_address):
    header_length = 64
    encoding = 'utf-8'

    while True:
        # Receive the message header
        header_bytes = client_socket.recv(header_length)
        if not header_bytes:
            # The client has closed the connection
            break
        message_length = int(header_bytes.decode(encoding).strip())

        # Receive the message body
        message_bytes = client_socket.recv(message_length)
        if not message_bytes:
            # The client has closed the connection
            break
        message = message_bytes.decode(encoding)

        # Handle the message
        print(f"Received message from {client_address}: {message}")

    # Close the client socket
    client_socket.close()

def start_server():
    server_address = ('', 5555)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen()

    print(f"Server started on {server_address}")

    while True:
        # Accept incoming connections
        client_socket, client_address = server_socket.accept()

        # Create a thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    start_server()
