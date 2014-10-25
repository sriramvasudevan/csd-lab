from params import *
class Block:
    def __init__():
        self.state = I
        self.block_address = -1

    def setInvalidate():
        self.state = I

    def setShared(address):
        self.state = S
        self.block_address = address

    def setModified(address):
        self.state = M
        self.block_address = address

    def setExclusive(address):
        self.state = E
        self.block_address = address

    def setOwned(address):
        self.state = O
        self.block_address = address

class Cache:
    def __init__():
        self.blocks = [Block() for _ in range(NUM_BLOCKS)]

    def getState(address):
        block_id = address%NUM_BLOCKS_CACHE
        if(self.blocks[block_id].block_address == address):
            return self.blocks[block_id].state
        return NP #Not present

    def getBlockState(block_id):
        return self.blocks[block_id].state

    def setInvalidate(address):
        block_id = address%NUM_BLOCKS
        assert (self.blocks[block_id].block_address==address)
        self.blocks[block_id].setInvalidate()

    def setExclusive(address):
        block_id = address%NUM_BLOCKS
        self.blocks[block_id].setExclusive(address)

    def setShared(address):
        block_id = address%NUM_BLOCKS
        self.blocks[block_id].setShared(address)

    def setModified(address):
        block_id = address%NUM_BLOCKS
        self.blocks[block_id].setModified(address)

    def setOwned(address):
        block_id = address%NUM_BLOCKS
        self.blocks[block_id].setOwned(address)
