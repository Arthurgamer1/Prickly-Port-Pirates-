from P2P import P2PNode
import threading

def start_cli(node):
    while True:
        message = input("Enter message (or type 'exit' to shutdown): ")
        if message == 'exit':
            print("Shutting down node...")
            node.shutdown()
            break
        elif message:
            node.send_message(message)


node2 = P2PNode('localhost', 8001)
node2.start_server()

# Start CLI in a separate thread
cli_thread = threading.Thread(target=start_cli, args=(node2,))
cli_thread.start()

# To connect to another node, use node.connect_to_node('other_host', other_port)
node2.connect_to_node('127.0.0.1', 8000)