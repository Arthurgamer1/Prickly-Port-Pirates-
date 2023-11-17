import socket
import threading
import json
import threading
import time
from blockchain import Block, Blockchain

# blockchain initialization
blockchain = Blockchain()


# this function deals with the client sending messages to the server
def handle_client(connection, address, all_connections):
    print(f"New connection from {address}")
    # Handle client connection and messages here
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                # add out message to blockchain
                new_block = Block(time.time(), message)
                blockchain.add_block(new_block)
                broadcast_blockchain(all_connections)
            else:
                break
        except:
            continue
    connection.close()


# This function brodcasts blockchain updates to clients
def broadcast_blockchain(connections):
    for conn in connections:
        conn.send(json.dumps([block.__dict__ for block in blockchain.chain]).encode())


# global variable for server listening loop
running = True


# Server loop function
def server_loop(server, all_connections):
    global running
    while running:
        try:
            server.settimeout(1)  # Set a timeout for blocking operations
            client_conn, client_addr = server.accept()
            all_connections.append(client_conn)
            client_thread = threading.Thread(
                target=handle_client, args=(client_conn, client_addr, all_connections)
            )
            client_thread.start()
        except socket.timeout:
            continue  # Continue to check if the server is still running


# Start the server
def start_server():
    global running

    # Server details
    host = "localhost"
    port = 8001
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    all_connections = []

    # Confirmation message to ensure server is running
    print(f"Server is listening on {host}:{port}")

    # Start server loop in a separate thread
    server_thread = threading.Thread(target=server_loop, args=(server, all_connections))
    server_thread.start()

    try:
        while True:
            time.sleep(
                1
            )  # Main thread doing nothing, just waiting for KeyboardInterrupt
    except KeyboardInterrupt:
        running = False
        server_thread.join()  # Wait for server thread to finish
        print("Shutting down server...")
        for conn in all_connections:
            conn.close()
        server.close()


# Run the server
start_server()
