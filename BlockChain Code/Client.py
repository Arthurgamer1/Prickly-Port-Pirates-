import socket
from blockchain import Block, Blockchain
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5555))

# Send and receive messages here

client.close()
