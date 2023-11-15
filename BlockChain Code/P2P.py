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
        self.executor = ThreadPoolExecutor(max_workers=10)
    def start_server(self):
        # Start a server to accept connections
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen(5)
        threading.Thread(target=self.accept_connections, args=(server,)).start()
        # Confirmation message to ensure server is running
        print("Server is Running")

    def accept_connections(self, server):
       while True:
            try:
                conn, addr = server.accept()
                print(f"Accepted connection from {addr}")
                self.sockets.append(conn)
                self.executor.submit(self.handle_client, conn)  # Submit to the executor
            except Exception as e:
                print(f"Error accepting connections: {e}")
                break

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
                    recieved_chain = json.loads(message)
                    #update local blockchain and display message
                    self.update_and_display_new_blocks(recieved_chain)
                else:
                    break
            except Exception as e:
                print(f"Error processing recieved data? {e})")
                break
        conn.close()

    def update_and_display_new_blocks(self, received_chain):
        new_blocks = [Block(block_dict['timestamp'], block_dict['data'], block_dict['previous_hash']) for block_dict in received_chain]
        if self.blockchain.replace_chain(new_blocks):
            # Assuming the new chain is longer and valid, display new messages
            for i in range(len(self.blockchain.chain)):
                block = self.blockchain.chain[i]
                print(f"Block {i} | New message received: {block.data}")

    def broadcast_blockchain(self):
        # Serialize the entire blockchain and send it to all connected nodes
        blockchain_data = json.dumps([block.__dict__ for block in self.blockchain.chain])
        for socket in self.sockets:
            try:
                socket.send(blockchain_data.encode())
            except:
                pass

    def send_message(self, message):
        # Add the message to the blockchain
        new_block = Block(time.time(), message)
        self.blockchain.add_block(new_block)
        # Broadcast the updated blockchain
        self.broadcast_blockchain()
    
    def shutdown(self):
        # Call this method to cleanly shut down the node
        self.executor.shutdown(wait=True)
        for sock in self.sockets:
            sock.close()
# Example usage
#node1 = P2PNode('localhost', 8000)
#node1.start_server()

#node2 = P2PNode('localhost', 8001)
#node2.start_server()

# To connect to another node, use node.connect_to_node('other_host', other_port)
#node2.connect_to_node('localhost', 8000)