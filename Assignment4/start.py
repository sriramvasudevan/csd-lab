from cache import Cache
from params import *
from random import randrange


def rwMESI(rw):
    pass


def rwMOESI(rw):
    pass


def simulate(protocol='MESI'):
    proc = [Cache() for _ in range(NUM_PROC)]
    iternos = 0
    trans = {}
    trans['read'] = 0
    trans['write'] = 0
    state_trans = {}
    state_trans['read'] = 0
    state_trans['write'] = 0

    while(iternos<NUM_ITER):
        proc_id = randrange(NUM_PROC)

        for rw in ['read', 'write']:
            mem_block_id = randrange(NUM_BLOCKS_MEM)
            block_id = mem_block_id%NUM_BLOCKS
            if(proc[proc_id].blocks[block_id].block_address!=mem_block_id and 
                    proc[proc_id].getState(mem_block_id)==MO):
                trans[rw] += 1
            print 'Proc:', proc_id, 'Mem', rw, 'location:', mem_block_id, 'block ID:', block_id
            block_state = proc[proc_id].getState(mem_block_id)
            other_block_state = proc[(proc_id+1)%NUM_PROC].getState(mem_block_id)
            print "Current state in", rw, block_state, "; Other block state", other_block_state
            # Read/Write opn
            if(protocol=='MESI'):
                rwMESI(rw)
            elif(protocol=='MOESI'):
                rwMOESI(rw)

        iternos += 1
        
    print "No. iterations:", iternos
    print "Read transactions:", read_trans
    print "Write transactions:", write_trans
    print "Read State transactions:", state_read_trans
    print "Write State transactions:", state_write_trans


if __name__=="__main__":
    for protocol in ['MESI', 'MOESI']:
        print protocol, "Protocol Simulation:"
        simulate(protocol)
