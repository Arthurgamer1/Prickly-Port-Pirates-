import socket
import threading
import json
import time
from blockchain import Block, Blockchain 

import socket
import threading

class P2PNode:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connections = [] 
        self.running = True

    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Listening for connections on {self.host}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        while self.running:
            try:
                connection, address = self.socket.accept()
                if connection:
                    self.connections.append(connection)
                    print(f"Accepted connection from {address}\n> ", end="")
                    threading.Thread(target=self.handle_client, args=(connection, address), daemon=True).start()
            except socket.error:
                break  # Socket was closed, exit the loop

    def connect_to_node(self, peer_host, peer_port):
        try:
            connection = socket.create_connection((peer_host, peer_port))
            self.connections.append(connection)
            print(f"Connected to {peer_host}:{peer_port}")
            threading.Thread(target=self.handle_client, args=(connection, (peer_host, peer_port)), daemon=True).start()
        except socket.error as e:
            print(f"Failed to connect to {peer_host}:{peer_port}. Error: {e}")

    def send_message(self, message):
        message = f"{self.username}: {message}"
        for connection in self.connections:
            try:
                connection.sendall(message.encode())
            except socket.error as e:
                print(f"Failed to send message. Error: {e}")
                self.connections.remove(connection)

    def handle_client(self, connection, address):
        while self.running:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Received data from {address}: {data.decode()}\n> ", end="")
            except socket.error:
                break

    def start_chat_interface(self):
        while True:
            message = input("> ")
            self.send_message(message)

    def shutdown(self):
        self.running = False
        for conn in self.connections:
            conn.close()
        self.socket.close()
        print("Server shutdown completed.")

#testing P2P class below
'''
if __name__ == "__main__":

    # Example usage
    node1 = P2PNode('localhost', 8000)
    node1.start_server()

    node2 = P2PNode('localhost', 8001)
    node2.start_server()

    time.sleep(1)

    # To connect to another node, use node.connect_to_node('other_host', other_port)
    node2.connect_to_node('localhost', 8000)
    time.sleep(1)
    
    #start chatting
    chat_thread = threading.Thread(target=node2.start_chat_interface)
    chat_thread.start()

'''