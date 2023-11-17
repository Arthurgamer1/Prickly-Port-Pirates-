import socket
import threading
import json
import time
from blockchain import Block, Blockchain 
import socket
import threading

#Peer2Peer class for instantiating each node
class P2PNode:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = [] 
        self.running = True
        self.blockchain = Blockchain()

    #starts the peer server for connecting to other peers
    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Listening for connections on {self.host}:{self.port}")
        #creates a new thread to handle new connections
        threading.Thread(target=self.accept_connections).start()
    
    #accepts incoming connections
    def accept_connections(self):
        while self.running:
            try:
                connection, address = self.socket.accept()
                if connection:
                    self.connections.append(connection)
                    print(f"Accepted connection from {address}\n> [{self.username}]: ", end="")
                    threading.Thread(target=self.handle_client, args=(connection, address), daemon=True).start()
            except socket.error:
                break  # Socket was closed, exit the loop
    
    #connects to other nodes given thier host and port
    def connect_to_node(self, peer_host, peer_port):
        try:
            connection = socket.create_connection((peer_host, peer_port))
            self.connections.append(connection)
            print(f"Connected to {peer_host}:{peer_port}")
            threading.Thread(target=self.handle_client, args=(connection, (peer_host, peer_port)), daemon=True).start()
        except socket.error as e:
            print(f"Failed to connect to {peer_host}:{peer_port}. Error: {e}")

    #used to send message to another peer.
    def send_message(self, message):
        #create a new block with message
        new_block = Block(time.time(), message)
        self.blockchain.add_block(new_block)
        
        #broadcast the block to peers
        self.broadcast_block(new_block)

        message = f"{self.username}: {message}"
        for connection in self.connections:
            try:
                connection.sendall(message.encode())
            except socket.error as e:
                print(f"Failed to send message. Error: {e}")
                self.connections.remove(connection)

    #handles recieving message from another peer
    def handle_client(self, connection, address):
         # Send the current blockchain to the newly connected peer
        self.send_entire_blockchain(connection)
        
        while self.running:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                # Try to interpret received data as a blockchain or block
                try:
                    received_data = json.loads(data.decode())
                    if isinstance(received_data, list):  # Assume it's a blockchain
                        self.replace_chain(received_data)
                    else:  # Assume it's a single block
                        if self.validate_and_add_block(received_data):
                            print(f"New block added from {address}")
                except json.JSONDecodeError:
                    print(f"\n> Message from {data.decode()}\n> [{self.username}]: ", end="")
            except socket.error:
                break
    
    #used for user input of message. 
    def start_chat_interface(self):
        while True:
            message = input(f"> [{self.username}]: ")
            self.send_message(message)

    def shutdown(self):
        #not probably needed, but a function to shutdown the node
        self.running = False
        for conn in self.connections:
            conn.close()
        self.socket.close()
        print("Server shutdown completed.")
    
    def broadcast_block(self, block):
        block_data = json.dumps(block.__dict__)
        for connection in self.connections:
            try:
                connection.sendall(block_data.encode())
            except socket.error as e:
                print(f"Failed to broadcast block. Error: {e}")
                self.connections.remove(connection)
            #save after broadcast
            self.blockchain.save_to_file()
    
    def validate_and_add_block(self, block_data):
        new_block = Block(block_data['timestamp'], block_data['data'], block_data['previous_hash'])
        new_block.hash = block_data['hash']
        if self.blockchain.is_chain_valid() and new_block.previous_hash == self.blockchain.get_latest_block().hash:
            self.blockchain.add_block(new_block)
            self.blockchain.save_to_file() #save after adding new block
            return True
        return False

    #send the blockchain to all peers
    def send_entire_blockchain(self, connection):
        blockchain_data = json.dumps([block.__dict__ for block in self.blockchain.chain])
        try:
            connection.sendall(blockchain_data.encode())
        except socket.error as e:
            print(f"Failed to send blockchain. Error: {e}")

    #fixes the double genesis problem?
    def replace_chain(self, new_chain):
        new_blockchain = Blockchain()
        new_blockchain.chain = [Block(block['timestamp'], block['data'], block['previous_hash']) for block in new_chain]
        if new_blockchain.is_chain_valid() and len(new_blockchain.chain) > len(self.blockchain.chain):
            self.blockchain = new_blockchain
            self.blockchain.save_to_file() #save blockchain after replacing 
            return True
        return False
    
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