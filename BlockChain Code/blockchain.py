import hashlib #used for creating hashes for reference (chain)
import time
from datetime import datetime
import json

class Block:
    
    def __init__(self, timestamp, data, previous_hash=''):
        '''
        Summary: This block class contructor is used to create a block
        with time, data, and the previous hash value of the block.
        
        Parameters:
        timestamp: the time at which the block is created
        data: this is where transactional data is stored, in our case text messages
        previous_hash: this is the chain variable which holds the hash value of the
        previous block. This represents the chain
        hash: also has it's own hash which is calculated using sha256.

        Returns: no returned value. 
        '''
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Calculate the hash of the block
        block_data = str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(block_data.encode()).hexdigest()
    
    def dict_to_block(self):
        block_dict = {}
        block_dict["timestamp"] = self.timestamp
        block_dict["data"] = self.data
        block_dict["previous_hash"] = self.previous_hash
        block_dict["hash"] = self.hash

        return block_dict
    

class Blockchain:
    def __init__(self, existing_chain=None):
        if(existing_chain != None):
            self.convert_dict_to_blockchain(existing_chain)
        else:
            self.chain = [self.create_genesis_block()]
        self.measure_times = []

    def create_genesis_block(self):
        # Manually construct a block with no previous hash
        return Block(time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        # Retrieve the most recent block in the chain
        return self.chain[-1]

    def convert_dict_to_blockchain(self, to_convert):
        if(type(to_convert) is str):
            to_convert = json.loads(to_convert)

        new_chain = []
        for block in to_convert:
            block = Block(block["timestamp"], block["data"], previous_hash=block["previous_hash"])
            new_chain.append(block)
        self.chain = new_chain

    def add_block(self, new_block):
        # Add a new block if valid
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Check if the blockchain is valid
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def blockchain_to_dict(self):
        return [block.__dict__ for block in self.chain]

    def display_chain(self):
         # Display the entire blockchain
        for block in self.chain:
            # Convert timestamp to human-readable format
            readable_timestamp = datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Block {self.chain.index(block)}: Timestamp: {readable_timestamp}, Data: {block.data}, Hash: {block.hash}, Previous Hash: {block.previous_hash}")

