from blockchain import Block, Blockchain
import json
import time

new_blockchain = Blockchain()

with open("blockchain.json", "w") as blockchain_file:
    blockchain_string = json.dumps(new_blockchain.blockchain_to_dict())
    blockchain_file.write(blockchain_string)

