import socket
import threading

def receive_messages(client_socket):
    while True:
        data, address = client_socket.recvfrom(1024)
        print(f"Received: {data.decode()}\n> ", end="")

# Peer 2 (acting as client)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 55555)
username = input("Enter your username: ")

client_socket.sendto(username.encode(), server_address)
print(f"Peer {username} connected to server, establishing connection with peer...")

data = client_socket.recv(1024).decode()
ip, sport, dport, other_user = data.split(" ")
print(f"Connected to username {other_user}.")

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Send messages
while True:
    message = input("> ")
    client_socket.sendto(message.encode(), (ip, int(sport)))
