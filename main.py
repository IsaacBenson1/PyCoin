import pickle
from hashlib import md5
import json
import time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256, MD5
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
import random


class Transaction:
    def __init__(self, public, private, amount):
        self.publicKey = public
        self.privateKey = private
        self.amount = amount

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return self.toJSON()


class Block:
    nonce = random.random() * 9999999

    def __init__(self, prevHash, transaction):
        self.prevHash = prevHash
        self.transaction = transaction
        createdAt = time.localtime()
        self.time = time.strftime("%H:%M:%S", createdAt)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def getHash(self):                      # this returns a JSON string of the block object which is then converted to hexadecimal
        string = self.toJSON()
        hashed = SHA256.new(str(string).encode())
        return hashed.hexdigest()


class Chain:
    def __init__(self, chain=Block(None, Transaction('Genesis', 'Naruto', 100))):
        self.chain = [chain]

    def getLast(self):
        return self.chain[len(self.chain)-1]

    def mine(self, nonce):
        solution = 1
        print('mining...')
        while True:
            possibleSolution = MD5.new(nonce+solution).hexdigest()
            if possibleSolution[0:4] == '0000':
                print('Solution found. You earned some coin!')
                return possibleSolution

            solution += 1

    def addBlock(self, transaction, senderPublicKey, signature):
        toBeVerified = SHA256.new(str(transaction).encode())
        verifier = PKCS115_SigScheme(senderPublicKey)
        try:
            verifier.verify(toBeVerified, signature)
            self.chain.append(Block(self.getLast().getHash(), transaction))
            print("Verification complete. Block successfully added!")
            return 1

        except ValueError:
            print("Invalid block :(")
            return 0


myChain = Chain()


class Wallet:

    def __init__(self, balance, keyPair=RSA.generate(bits=2048)):
        self.keyPair = keyPair
        self.publicKey = keyPair.public_key()
        self.signer = PKCS115_SigScheme(keyPair)
        self.balance = balance

    def sendMoney(self, amount, reciever):
        recieverpublickey = reciever.publicKey
        if amount > self.balance:
            print('insufficient funds :(')
            return

        transaction = Transaction(self.publicKey, recieverpublickey, amount)
        myHash = SHA256.new(str(transaction).encode())
        signature = self.signer.sign(myHash)
        # myChain.addBlock(transaction, self.publicKey, signature)
        if myChain.addBlock(transaction, self.publicKey, signature) == 1:
            reciever.balance += transaction.amount
            self.balance -= transaction.amount
            print("Sender balance: $"+str(self.balance)+" Reciever Balance: $"+str(reciever.balance))


isaac = Wallet(100)
forrest = Wallet(0)
owen = Wallet(0)
berg = Wallet(0)


isaac.sendMoney(100, forrest)
forrest.sendMoney(50, owen)
owen.sendMoney(25, berg)




















