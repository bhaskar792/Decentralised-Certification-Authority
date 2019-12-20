import time
import hashlib

import socket
from time import sleep
from threading import *



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
        return "{} - {} - {} - {} - {}".format(str(self.index),str(self.proof),str(self.previous_hash),str(self.transactions),str(self.timestamp))
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
        self.current_block_transactions.append({
            'sender':sender,
            'recipient': recipient,
            'amount': amount})
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

class recieve(Thread,BlockChain):
    def run(self):
        print('starting socket in try')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 1234))
        print(s.recv(1024))
        clientsocket = s
        while True:
            mess=clientsocket.recv(1024)
            if mess:
                message = str(mess.decode("utf-8"))
                print(message)
                if message=='create transaction':
                    while True:
                        mess = clientsocket.recv(1024)
                        if mess:
                            message = str(mess.decode("utf-8"))
                            print(message)
                            sender_sock=message
                            break
                    while True:
                        mess = clientsocket.recv(1024)
                        if mess:
                            message = str(mess.decode("utf-8"))
                            print(message)
                            recipient_sock=message
                            break
                    while True:
                        mess = clientsocket.recv(1024)
                        if mess:
                            message = str(mess.decode("utf-8"))
                            print(message)
                            amount_sock=message
                            break
                    print(sender_sock+recipient_sock+amount_sock)
                    sock_transaction=BlockChain()
                    sock_transaction.create_new_transaction(sender_sock,amount_sock,recipient_sock)
                if message=='mine block':
                    while True:
                        mess = clientsocket.recv(1024)
                        if mess:
                            message = str(mess.decode("utf-8"))
                            print(message)
                            miner_addr = message
                            break
                    mine_sock=blockchain
                    mine_sock.mine_block(miner_addr)
                    print(mine_sock.chain)

r=recieve()
r.start()
