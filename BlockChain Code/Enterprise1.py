from P2P import P2PNode
import threading

if __name__ == "__main__":
    # Initialize and start the node server
    node = P2PNode('localhost', 8000)  # Use appropriate port for each node
    node.start_server()

    # Connect to other node if necessary
    # node.connect_to_node('localhost', 8001)

    # Start chat interface in a new thread
    chat_thread = threading.Thread(target=node.start_chat_interface)
    chat_thread.start()

    #this allows us to shutdown the node cleanly with ctrl+C
    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        print("Shutting down...")
        node.shutdown()