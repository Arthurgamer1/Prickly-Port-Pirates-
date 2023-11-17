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
        with open("blockchain.json", "r") as blockchain_file:
            self.blockchain = Blockchain(existing_chain=blockchain_file.read())


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
        message = f"{self.username}: {message}"
        for connection in self.connections:
            try:
                connection.sendall(message.encode())
                self.broadcast_block(message, connection)
            except socket.error as e:
                print(f"Failed to send message. Error: {e}")
                self.connections.remove(connection)

    #handles recieving message from another peer
    def handle_client(self, connection, address):
        while self.running:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"\n> Message from {data.decode()}\n> [{self.username}]: ", end="")

                #made recv size as large as it can go
                new_block = connection.recv(1024).decode()
                new_block = json.loads(new_block)
                new_block = Block(new_block["timestamp"], new_block["data"])
                self.blockchain.add_block(new_block)

                with open("blockchain.json", "w") as blockchain_file:
                    #test_hash = new_block.calculate_hash()
                    to_write = json.dumps(self.blockchain.blockchain_to_dict(), indent=2)
                    blockchain_file.write(to_write)
                


                #writes received message as new blockchain
                # with open("blockchain.json", "w") as blockchain_file:
                #     new_blockchain = json.loads(new_blockchain)
                #     new_blockchain = json.dumps(new_blockchain, indent=2)
                #     blockchain_file.write(new_blockchain)
                #     print(new_blockchain)
                #     self.blockchain = Blockchain(existing_chain=new_blockchain)

                
            except socket.error:
                break
    

    #used for user input of message. 
    def start_chat_interface(self):
        while True:
            message = input(f"> [{self.username}]: ")
            if(message == "is_valid"):
                print(self.blockchain.is_chain_valid())
            elif(message == "display_chain"):
                self.blockchain.display_chain()
            else:
                self.send_message(message)


    def broadcast_block(self, message, connection):
        
        new_block = Block(time.time(), message)
        self.blockchain.add_block(new_block)
        
        with open("blockchain.json", "w") as blockchain_file:
            blockchain_string = json.dumps(self.blockchain.blockchain_to_dict())
            blockchain_file.write(blockchain_string)

        connection.sendall(json.dumps(new_block.dict_to_block()).encode())



        



    def shutdown(self):
        #not probably needed, but a function to shutdown the node
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