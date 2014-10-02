class Instruction:
    def __init__(self,opcode,dest,src1,src2,index):
        self.opcode = opcode 
        self.src1 = src1
        self.dest = dest
        self.src2 = src2
        self.index = index
