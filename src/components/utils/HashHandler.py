import hmac
import hashlib

class HashHandler:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        self.hashname = hashlib.sha256

    def generate_hash(self, message):
        hash_object = hmac.new(self.secret_key, message, self.hashname)
        hexa_hash = hash_object.hexdigest()
        return hexa_hash

if __name__ == "__main__":

    secret_key = b"my_secret_key"  # Key must be bytes
    message = b"This is the message to be authenticated." # Message must be bytes
    hashHandler = HashHandler(secret_key=secret_key)
    hash = hashHandler.generate_hash(message)
    print(hash)

    # print(f"HMAC-SHA256 digest: {hmac_digest}")