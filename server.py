import socket
import threading

def handle_client(connection, address):
    print(f"New connection from {address}")
    # Handle client connection and messages here
    connection.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen()

while True:
    client_conn, client_addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_conn, client_addr))
    client_thread.start()
