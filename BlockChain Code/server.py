import socket
import threading
import json
import threading
import time
from blockchain import Block, Blockchain

#blockchain initialization
blockchain = Blockchain()

#this function deals with the client sending messages to the server
def handle_client(connection, address):
    print(f"New connection from {address}")
    # Handle client connection and messages here
    while True:
        try:
            message = connection.recv(1024).decode()
            if message:
                #add out message to blockchain
                new_block = Block(time.time(), message)
                blockchain.add_block(new_block)
                broadcast_blockchain(all_connections)
            else:
                break
        except:
            continue
    connection.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5555))
server.listen()

while True:
    client_conn, client_addr = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_conn, client_addr))
    client_thread.start()
