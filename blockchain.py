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

#from uudi import uuid4

import requests
from flask_wtf import FlaskForm
from flask import Flask,render_template,flash,request,url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

app = Flask(__name__,template_folder='templates')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
blockchain.mine_block('address')
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

@app.route('/mine',methods=['POST','GET'])
def mine():

    return render_template('mine.html',your_list=ch)
@app.route('/transaction',methods=['POST','GET'])
def create_transactions():
    form=create_transaction()
    form1= mine1()
    if form.is_submitted():
        sender=str(form.sender._value())
        recipient=str(form.recipient._value())
        amount=str(form.amount._value())
        blockchain.create_new_transaction(sender,recipient,amount)
    if form1.is_submitted():
        blockchain.mine_block(str(form1.miner_address._value()))


    return render_template('transaction.html', form=form,form1=form1)

if __name__=='__main__':
    app.run(debug=True)
