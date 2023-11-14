import socket
import threading

def receive_messages(client_socket):
    while True:
        data, address = client_socket.recvfrom(1024)
        print(f"Received: {data.decode()}\n> ")

# Peer 2 (acting as client)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("localhost", 55555)

client_socket.sendto("test".encode(), server_address)
print(f"Peer 2 (Client) connected to {server_address[0]}:{server_address[1]}")

data = client_socket.recv(1024).decode()
ip, sport, dport = data.split(" ")
print(data)

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Send messages
while True:
    message = input("> ")
    client_socket.sendto(message.encode(), (ip, int(sport)))
