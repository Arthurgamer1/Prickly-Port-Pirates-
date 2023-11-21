from P2P import P2PNode
import threading

if __name__ == "__main__":
    # Initialize and start the node server

    #username = input("Enter  your username: ")
    username = "robot2"

    node = P2PNode('localhost', 8001, username)  # Use appropriate port for each node
    node.start_server()

    # Connect to other node
    node.connect_to_node('localhost', 8000)

    # Start chat interface in a new thread
    chat_thread = threading.Thread(target=node.start_chat_interface)
    chat_thread.start()

    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Shutting down...")
        node.shutdown()