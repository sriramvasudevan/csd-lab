class Block:
    def __init__():
        self.state = IN
        self.block_address = -1

    def setInvalidate():
        self.state = IN

    def setShared(address):
        self.state = SH
        self.block_address = address

    def setModify(address):
        self.state = MO
        self.block_address = address

    def setExclusive(address):
        self.state = EX
        self.block_address = address

    def setOwned(address):
        self.state = OW
        self.block_address = address

class Cache:
    def __init__():
        self.blocks = [Block() for _ in range(NUM_BLOCKS)]

    def getState(address):
        block_id = address%NUM_BLOCKS
        if(self.blocks[block_id].block_address == address):
            return self.blocks[block_id].state
        return NP

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

    def setModify(address):
        block_id = address%NUM_BLOCKS
        self.blocks[block_id].setModify(address)

    def setOwned(address):
        block_id = address%NUM_BLOCKS
        self.blocks[block_id].setOwned(address)
