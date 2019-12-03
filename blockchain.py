import time
import hashlib

class Block(object):
    def __init__(self,index,proof,previous_hash,transactions,timestamp=None):
        self.index=index
        self.proof=proof
        self.previous_hash=previous_hash
        self.transactions=transactions
        self.timestamp =time.time()


    def get_block_hash(self):
        block_string="{}{}{}{}{}".format(self.index,self.proof,self.previous_hash,self.transactions,self.timestamp)
        return hashlib.sha256(block_string.encode()).hexdigest()
    #hexdigest() return in hexadecimal form
    #sha256 and encode are self explanatory

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index,self.proof,self.previous_hash,self.transactions,self.timestamp)
    #method for representing
class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_block_transactions = []

    def create_new_block(self,proof,previous_hash):
        block = Block(index=len(self.chain),proof=proof,previous_hash=previous_hash,transactions = self.current_block_transactions)
        self.current_block_transactions=[] #making transaction list empty as they are added to the block
        self.chain.append(block)
        return block

    def create_new_transaction(self,sender,recipient,amount):
        self.current_block_transactions.append({'sender':sender, 'recipient': recipient,'amount': amount})
        return True

    def create_proof_of_work(self,previous_proof):
        # a simple pow just by dividing with 99
        proof=previous_proof + 1
        while not BlockChain.is_valid_proof(proof,previous_proof):
            proof=proof+1
        return proof

    def is_valid_proof(proof,previous_proof):
        return (proof + previous_proof)%99==0

    def get_last_block(self):
        return self.chain[-1]

    def mine_block(self,miner_address):

        self.create_new_transaction(
            sender="0",
            recipient=miner_address,
            amount=1
            )
        last_block = self.get_last_block()

        last_proof= last_block.proof
        proof = self.create_proof_of_work(last_proof)

        last_hash = last_block.get_block_hash()
        block = self.create_new_block(proof,last_hash)

blockchain = BlockChain()
blockchain.create_new_block(proof=0, previous_hash=0)

print("Before Mining")
print(blockchain.chain)
blockchain.mine_block('miner')

print(" After Mining")
print(blockchain.chain)