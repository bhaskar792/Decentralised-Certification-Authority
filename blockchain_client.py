import time
import hashlib


first=1

class Block(object):
    def __init__(self,index,proof,previous_hash,transactions,timestamp=None):
        global first
        self.index=index
        self.proof=proof
        self.previous_hash=previous_hash
        self.transactions=transactions
        if first==1:
            self.timestamp =1
            first = 0
        else:
            self.timestamp=time.time()

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

import socket
from time import sleep
from threading import *
import queue



class recieve(Thread,BlockChain):
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 1234))
        print(s.recv(1024))
        clientsocket = s
        q.put(clientsocket)


        #recieving
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
                    blockchain
                    blockchain.create_new_transaction(sender_sock,recipient_sock,amount_sock)
                if message=='mine block':
                    while True:
                        mess = clientsocket.recv(1024)
                        if mess:
                            message = str(mess.decode("utf-8"))
                            print(message)
                            miner_addr = message
                            break

                    blockchain.mine_block(miner_addr)
                    print(blockchain.chain)
#from uudi import uuid4

import requests
from flask_wtf import FlaskForm
from flask import Flask,render_template,flash,request,url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__,template_folder='templates')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

ch=blockchain.chain


#node_address=uuid4().hex #unique address for current node
class create_transaction(FlaskForm):
    sender=StringField('sender')
    recipient=StringField('recipient')
    amount=StringField('amount')
    submit=SubmitField('create_transaction ')


class mine1(FlaskForm):
    miner_address = StringField('miner_address')
    mine = SubmitField('mine')


q=queue.Queue()

r=recieve()
r.start()

class flask(Thread):
    def run(self):
        @app.route('/mine', methods=['POST', 'GET'])
        def mine():
            form1 = mine1()
            if form1.is_submitted():
                blockchain.mine_block(str(form1.miner_address._value()))
                clientsocket.send(bytes('mine block','utf-8'))
                clientsocket.send(bytes(str(form1.miner_address._value()), 'utf-8'))
            return render_template('mine.html', your_list=ch,form1=form1)

        @app.route('/transaction', methods=['POST', 'GET'])
        def create_transactions():


            form = create_transaction()

            if form.is_submitted():
                sender = str(form.sender._value())
                recipient = str(form.recipient._value())
                amount = str(form.amount._value())
                blockchain.create_new_transaction(sender, recipient, amount)
                # sending to another node

                clientsocket.send(bytes('create transaction', 'utf-8'))
                sleep(0.2)
                clientsocket.send(bytes(sender, 'utf-8'))
                sleep(0.2)
                clientsocket.send(bytes(recipient, 'utf-8'))
                sleep(0.2)
                clientsocket.send(bytes(amount, 'utf-8'))



            return render_template('transaction.html', form=form)

        if __name__=='__main__':

            app.run(debug=True,port=5001,use_reloader=False)
clientsocket = q.get(timeout=20)
f=flask()
f.run()


