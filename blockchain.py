from block import Block
from verify import BlockOutOfChain, BlockVerifier
import logging

logger = logging.getLogger('Blockchain')


class Blockchain: 

    __slots__ =  'max_nonce', 'chain', 'difficulty', 'wallet'

    def __init__(self, difficulty, wallet):
        self.max_nonce = 2**32
    
        self.difficulty = difficulty
        self.wallet = wallet
        self.chain = []  
 
    def create_first_block(self):
        block = Block(0, 0x0)
        self.mine_block(block)

    def is_valid_block(self, block):
        bv = BlockVerifier(self.difficulty)
        return bv.verify(self.head, block)

    def add_block(self, block):
        if self.head and block.hash() == self.head.hash():
            logger.error('Duplicate block')
            return False  
        try:
            self.is_valid_block(block)
        except BlockOutOfChain as e:
            logger.error('Block verification failed: %s' % e)
            return False
        else:        
            self.chain.append(block)
            logger.info('   Block added   ')
            return True

    def helpfunc_mine_block(self, check_stop=None):
        block = Block(
            index=self.head.index+1,
            prev_hash=self.head.hash()
        )
        self.mine_block(block, check_stop)


    def mine_block(self, block, check_stop=None):
        for n in range(self.max_nonce):
            if check_stop and check_stop():
                logger.error('Mining interrupted.')
                return
            if int(block.hash(nonce=n), 16) <= (2 ** (256-self.difficulty)):
                self.add_block(block)
                logger.info('  Block mined at nonce: %s' % n)
                logger.info(" block details(prev block hash and current block hash):  %s   %s\n", str(block.prev_hash), str(block.hash()))
                break
                
    #core of the blockchain
    #consensus algorithm
    @property
    def head(self):
        if not self.chain:
            return None
        return self.chain[-1]

    @property
    def blockchain(self):
        return [el.as_dict for el in reversed(self.chain)]