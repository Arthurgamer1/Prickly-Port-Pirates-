import socket, threading, json, time, socket, threading, csv
from blockchain import Block, Blockchain


# Peer2Peer class for instantiating each node
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

    # starts the peer server for connecting to other peers
    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Listening for connections on {self.host}:{self.port}")
        # creates a new thread to handle new connections
        threading.Thread(target=self.accept_connections).start()

    # accepts incoming connections
    def accept_connections(self):
        while self.running:
            try:
                connection, address = self.socket.accept()
                if connection:
                    self.connections.append(connection)
                    print(
                        f"Accepted connection from {address}\n> [{self.username}]: ",
                        end="",
                    )
                    threading.Thread(
                        target=self.handle_client,
                        args=(connection, address),
                        daemon=True,
                    ).start()
            except socket.error:
                break  # Socket was closed, exit the loop

    # connects to other nodes given thier host and port
    def connect_to_node(self, peer_host, peer_port):
        try:
            connection = socket.create_connection((peer_host, peer_port))
            self.connections.append(connection)
            print(f"Connected to {peer_host}:{peer_port}")
            threading.Thread(
                target=self.handle_client,
                args=(connection, (peer_host, peer_port)),
                daemon=True,
            ).start()
        except socket.error as e:
            print(f"Failed to connect to {peer_host}:{peer_port}. Error: {e}")

    # used to send message to another peer.
    def send_message(self, message):
        start_time = time.time()
        message = f"{self.username}: {message}"
        for connection in self.connections:
            try:
                connection.sendall(message.encode())
                self.broadcast_block(message, connection)
                if not self.blockchain.is_chain_valid():
                    print("Blockchain validation failed at sender")
                    return
            except socket.error as e:
                print(f"Failed to send message. Error: {e}")
                self.connections.remove(connection)

        # measure time reciever and sender take to validate the blockchain
        end_time = time.time()
        time_taken = end_time - start_time

        # log time data into CSV
        with open("sender_time_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([time_taken])

    # handles recieving message from another peer
    def handle_client(self, connection, address):
        while self.running:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                start_time = time.time()  # recieving message tim
                print(
                    f"\n> Message from {data.decode()}\n> [{self.username}]: ", end=""
                )

                new_block = connection.recv(1024).decode()
                new_block = json.loads(new_block)
                new_block = Block(new_block["timestamp"], new_block["data"])
                self.blockchain.add_block(new_block)

                if not self.blockchain.is_chain_valid():
                    print("Blockchain validation failed at receiver.")
                    return  # Stop the process if validation fails

                with open("blockchain.json", "w") as blockchain_file:
                    # test_hash = new_block.calculate_hash()
                    to_write = json.dumps(
                        self.blockchain.blockchain_to_dict(), indent=2
                    )
                    blockchain_file.write(to_write)

                # log time taken
                end_time = time.time()
                time_taken = end_time - start_time

                # log time in csv
                with open("receiver_time_data.csv", "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([time_taken])

            except socket.error:
                break

    # used for user input of message.
    def start_chat_interface(self):
        while True:
            message = input(f"> [{self.username}]: ")

            if message.startswith("spam"): #starts spam function, input message folowed by minutes you want to runs
                try:
                    _, msgs_per_minute, duration = message.split()
                    msgs_per_minute = int(msgs_per_minute)
                    duration = int(duration)
                    self.spam_messages(msgs_per_minute, duration)
                except ValueError:
                    print("Invalid spam command. Usage: spam [messages_per_minute] [duration_in_minutes]")
            elif message == "is_valid": #allows you to check if the blockchain is valid
                print(self.blockchain.is_chain_valid())
            elif message == "display_chain": #dislpays the current blockchain
                self.blockchain.display_chain()
            else:
                self.send_message(message)

    #updates the blockchain and sends to all clients on blockchain.
    def broadcast_block(self, message, connection):
        new_block = Block(time.time(), message)
        self.blockchain.add_block(new_block)
        
        with open("blockchain.json", "w") as blockchain_file:
            blockchain_string = json.dumps(self.blockchain.blockchain_to_dict())
            blockchain_file.write(blockchain_string)

        connection.sendall(json.dumps(new_block.dict_to_block()).encode())

    def spam_messages(self, messages_per_minute, duration_minutes=1):
        """
        Spams a specified number of messages per minute for a given duration.

        Args:
        messages_per_minute (int): Number of messages to send per minute.
        duration_minutes (int): Duration in minutes for the spamming to last.
        """
        total_messages = messages_per_minute * duration_minutes
        interval = 60.0 / messages_per_minute  # Time interval between messages in seconds

        print(f"Starting to spam {total_messages} messages ({messages_per_minute} messages/minute) for {duration_minutes} minute(s).")
        
        for _ in range(total_messages):
            message = "Spam message"  # or generate a custom message
            self.send_message(message)
            time.sleep(interval)

        print("Completed spamming messages.")

    def shutdown(self):
        # not probably needed, but a function to shutdown the node
        self.running = False
        for conn in self.connections:
            conn.close()
        self.socket.close()
        print("Server shutdown completed.")
