from blockchain import Block, Blockchain
import json

new_blockchain = Blockchain()

with open("blockchain.json", "w") as blockchain_file:
    blockchain_string = json.dumps(new_blockchain)