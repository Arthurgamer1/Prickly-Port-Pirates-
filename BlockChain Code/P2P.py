import socket
import threading
import json
import time
from blockchain import Block, Blockchain 
from concurrent.futures import ThreadPoolExecutor

class P2PNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sockets = []
        self.blockchain = Blockchain()  # Initialize the blockchain

    def start_server(self):
        # Start a server to accept connections
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        threading.Thread(target=self.accept_connections, args=(server,)).start()
        # Confirmation message to ensure server is running
        print("Server is Running")

    def accept_connections(self, server):
        #limits the threads run at one time to 10 for connections
        with ThreadPoolExecutor(max_workers=10) as executor: 
            while True:
                conn, addr = server.accept()
                self.sockets.append(conn)
                threading.Thread(target=self.handle_client, args=(conn,)).start()

    def connect_to_node(self, host, port):
        # Connect to another node
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        self.sockets.append(conn)

    def handle_client(self, conn):
        while True:
            try:
                message = conn.recv(1024).decode()
                if message:
                    # Add message to blockchain
                    new_block = Block(time.time(), message)
                    self.blockchain.add_block(new_block)
                    self.broadcast_blockchain()
                else:
                    break
            except:
                continue
        conn.close()

    def broadcast_blockchain(self):
        # Broadcast updated blockchain to all connected nodes
        for socket in self.sockets:
            try:
                socket.send(json.dumps([block.__dict__ for block in self.blockchain.chain]).encode())
            except:
                pass

# Example usage
#node1 = P2PNode('localhost', 8000)
#node1.start_server()

#node2 = P2PNode('localhost', 8001)
#node2.start_server()

# To connect to another node, use node.connect_to_node('other_host', other_port)
#node2.connect_to_node('localhost', 8000)