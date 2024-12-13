# sign(Message, secret key)= signature
# verify(Message, signature, public key)= T/F
# blok[data, time, prev hash]->blok...
# tuttuğu indexe, veriye, zamana, önceki bloğun hash değerine (ve onun da tüm diğer değerlerine) bağlı olarak değişen bir yapı var

import hashlib
import time
import rsa #key'ler için gerekli

class Block:
    def __init__(self, index, prev_hash, data, timestamp=None):
        self.index= index
        self.prev_hash= prev_hash
        self.data = data
        self.timestamp = timestamp or time.time() #timestamp girmezsek şu anki zamanı almak için time.time kullandık
        self.hash = self.calculate_hash() #bloğun hash değeri

    def calculate_hash(self):
        block_string= f"{self.index}{self.prev_hash}{self.data}{self.timestamp}" #bu değerleri string haline getiriyoz kısaca hash(str) yapıyoruz ve nur topu gibi bir hash değerimiz oluyor
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain= [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "Genesis_Block", time.time())

    def get_latest_block(self):
        return self.chain[-1] #son eleman -1 index'ine sahip


    def add_block(self, new_block):
        new_block.prev_hash= self.get_latest_block().hash #yeni bloğun prev_hash değeri son bloğun hash değeri
        new_block.hash= new_block.calculate_hash()
        self.chain.append(new_block)


class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender= sender
        self.receiver= receiver
        self.amount= amount


    def sign_transaction(self, private_key):
        self.signature= rsa.sign(f"{self.sender}{self.receiver}{self.amount}".encode(), private_key, 'SHA-256')

    def is_valid(self, public_key):
        try:
            rsa.verify(f"{self.sender}{self.receiver}{self.amount}".encode(), self.signature, public_key)
            return True
        except:
            return False


(public_key, private_key)= rsa.newkeys(512)

tx=Transaction("Alice", "Bob", 10)
tx.sign_transaction(private_key)

print("Transaction validity: ", tx.is_valid(public_key))




mi_blockchain= Blockchain()

mi_blockchain.add_block(Block(1, "", "First"))
mi_blockchain.add_block(Block(2, "", "Second"))
mi_blockchain.add_block(Block(3, "", "Third"))

for block in mi_blockchain.chain:
    print(f"Index: {block.index}")
    print(f"Previous Hash: {block.prev_hash}")
    print(f"Data: {block.data}")
    print(f"Hash: {block.hash}")
    print(f"Timestamp: {block.timestamp}")
    print("-" * 30)





