import time
from hashlib import sha256


class Block:

    __slots__ = 'nonce', 'prev_hash', 'index','timestamp'

    def __init__(self, index, prev_hash, timestamp=None, nonce=0):
        self.prev_hash = prev_hash
        self.index = index
        self.nonce = nonce
        self.timestamp = timestamp or int(time.time())

    def hash(self, nonce=None):
        if nonce:
            self.nonce = nonce
        block_string = '{}{}{}{}'.format(
            self.prev_hash, self.index, self.nonce, self.timestamp
        )
        return sha256(sha256(block_string.encode()).hexdigest().encode('utf8')).hexdigest()

    @property
    def as_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "prev_hash": self.prev_hash,
            "hash": self.hash(),
            "nonce": self.nonce
            
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['index'],
            data['prev_hash'],
            data['timestamp'],
            data['nonce']
        )