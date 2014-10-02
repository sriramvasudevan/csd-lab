import reorder_buffer
import reservation_station
import functional_unit
from collections import deque

# Global Vars
NUM_RS=1
NUM_ALU=2
NUM_TYPES_INSTR=9
MAX_RB_SIZE=128
MAX_STORE_BUFF=8 
MAX_RS_SIZE=128
MAX_REGISTERS=8
MAX_INSTR=1

global_ins_counter = 0
store_counter = 0
global_time = 0

#Dict from type of latency ('add', 'mul' etc) to the int value
latency = {}

#Our registers
registers = []

rb = rs = fu = None

#A list of instructions
all_instructions = []

memory_access_queue = deque()

#A dict from instruction id to its type
instr_type = {}

#A map from integer tuple (a,b) to a double, and a bool for validity
buff = [{},{}]
buffer_validity = [{},{}]

def initvars():
    global rb, rs, fu
    #Our reorder buffer
    rb = reorder_buffer.ReorderBuffer()

    #Our reservation station
    rs = reservation_station.ReservationStation()

    fu = [functional_unit.FunctionalUnit() for i in range(NUM_ALU)]
