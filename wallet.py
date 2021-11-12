import rsa
import binascii


class Wallet:

    __slots__ = 'public_key', 'private_key'
    
    def __init__(self, pub=None, priv=None):
        if pub:
            self.public_key = pub
            self.private_key = rsa.PrivateKey.load_pkcs1(priv)

    @classmethod
    def create(cls):
        instance = cls(b'',b'')
        public_key, private_key = rsa.newkeys(512)
        instance.public_key = public_key
        instance.private_key = private_key
        return instance
  
    @property
    def public_address(self):
        return str(self.public_key)

    @property
    def private_address(self):
        return self.private_key.save_pkcs1()

    def sign(self, hash):
        return binascii.hexlify(rsa.sign(hash, self.private_key, 'SHA-256')).decode()

