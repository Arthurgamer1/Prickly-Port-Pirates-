from P2P import P2PNode

node2 = P2PNode('localhost', 8001)
node2.start_server()

# To connect to another node, use node.connect_to_node('other_host', other_port)
node2.connect_to_node('localhost', 8000)