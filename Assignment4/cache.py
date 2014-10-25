from params import *
class Block:
    def __init__(self):
        self.state = I
        self.block_address = -1

    def setInvalidate(self):
        self.state = I

    def setShared(self,address):
        self.state = S
        self.block_address = address

    def setModified(self,address):
        self.state = M
        self.block_address = address

    def setExclusive(self,address):
        self.state = E
        self.block_address = address

    def setOwned(self,address):
        self.state = O
        self.block_address = address

class Cache:
    def __init__(self):
        self.blocks = [Block() for _ in range(NUM_BLOCKS_CACHE)]

    def getState(self,address):
        block_id = address%NUM_BLOCKS_CACHE
        if(self.blocks[block_id].block_address == address):
            return self.blocks[block_id].state
        return NP #Not present

    def getBlockState(self,block_id):
        return self.blocks[block_id].state

    def setInvalidate(self,address):
        block_id = address%NUM_BLOCKS_CACHE
        assert (self.blocks[block_id].block_address==address)
        self.blocks[block_id].setInvalidate()

    def setExclusive(self,address):
        block_id = address%NUM_BLOCKS_CACHE
        self.blocks[block_id].setExclusive(address)

    def setShared(self,address):
        block_id = address%NUM_BLOCKS_CACHE
        self.blocks[block_id].setShared(address)

    def setModified(self,address):
        block_id = address%NUM_BLOCKS_CACHE
        self.blocks[block_id].setModified(address)

    def setOwned(self,address):
        block_id = address%NUM_BLOCKS_CACHE
        self.blocks[block_id].setOwned(address)
