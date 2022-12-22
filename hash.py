import hashlib

class Hash:
    def __init__(self,hash_string=""):
        self.hash_string=hash_string

    def set_hash(self,string_value):
        message = string_value.encode()
        self.hash_string= hashlib.sha256(message).hexdigest()

    def get_hash(self):
        return self.hash_string


#test code
hasher=Hash()
hasher.set_hash("tharinda")
print(hasher.get_hash())