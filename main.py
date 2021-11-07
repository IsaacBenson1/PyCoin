import hashlib
import datetime
import cryptography
import json
import time
import rsa




class Transaction:
    def __init__(self, public, private, amount):
        self.publicKey = public
        self.privateKey = private
        self.amount = amount

    def __str__(self):
        return json.dumps(self)


class Block:
    def __init__(self, prev, transaction):
        self.prev = prev
        self.transaction = transaction
        t = time.localtime()
        self.time = time.strftime("%H:%M:%S", t)

    def getHash(self):
        string = json.dumps(self)
        hashed = hashlib.sha256(string)
        return hashed.hexdigest()


class Chain:
    def __init__(self, chain, length):
        self.chain = [Block(None, Transaction('Genesis', 'Naruto', 100))]
        self.length = 0

    def getLast(self):
        return self.chain[self.length]

    def addBlock(self, transaction, public, private):
        verify = hashlib.


myChain = Chain()


class Wallet:
    def __init__(self, public, private):
        self.public = rsa.PublicKey()
        self.private = rsa.PrivateKey

    def sendMoney(self, amount, recieverpublickey):
        transaction = Transaction(amount, self.public, recieverpublickey)
        sign = rsa.sign(transaction, self.private, 'SHA256')
        myChain.addBlock(transaction, self.public, sign)












