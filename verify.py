class BlockOutOfChain(Exception):
    pass

class BlockVerificationFailed(Exception):
    pass

class BlockVerifier:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        
    def verify(self, head, block):
        # verifying block hash
        if int(block.hash(), 16) > (2 ** (256-self.difficulty)):
            raise BlockVerificationFailed('Block hash not satisfying condition')     
        
        # verifying some other things
        if head:
            if head.index >= block.index:
                raise BlockOutOfChain('Block index number wrong')
            if head.hash() != block.prev_hash:
                raise BlockOutOfChain('New block not pointed to the head')
            if head.timestamp > block.timestamp:
                raise BlockOutOfChain('Block from the past')

        return True