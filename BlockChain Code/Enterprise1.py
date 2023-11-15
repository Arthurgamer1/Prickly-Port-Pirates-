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


node = P2PNode('localhost', 8000)
node.start_server()

cli_thread = threading.Thread(target=start_cli, args=(node,))
cli_thread.start()

try:
    cli_thread.join()
except KeyboardInterrupt:
    print("Interrupt received, shutting down...")
    node.shutdown()
