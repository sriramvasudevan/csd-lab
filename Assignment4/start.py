from cache import Cache
from params import *
from random import randrange

def other(proc_id):
    return (proc_id+1)%2

def rwMESI(rw,proc,trans,state_trans,proc_id,mem_block_id,block_id,block_state,bs,obs):
    if rw == 'read':
        if bs == NP:
            if obs == NP or obs == I:
                proc[proc_id].setExclusive(mem_block_id)
                state_trans[rw] += 1
                trans[rw] += 1
            elif obs == E:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2
                trans[rw] += 1
            elif obs == S:
                proc[proc_id].setShared(mem_block_id)
                state_trans[rw] += 1
                trans[rw] += 1    
            elif obs == M:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2
                trans[rw] += 2
        elif bs == M:
            if obs == NP or obs == I:
                pass
            else:
                assert False
        elif bs == E:
            if obs == NP or obs == I:
                pass
            else:
                assert False

        elif bs == S:
            if obs == NP or obs == S:
                trans[rw] += 1
            else:
                assert False
        elif bs == I:
            if obs == NP or obs == I:
                proc[proc_id].setExclusive(mem_block_id)
                state_trans[rw] += 1
                trans[rw] += 1
            elif obs == E:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2
                trans[rw] += 1
            elif obs == S:
                assert False
            elif obs == M:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2
                trans[rw] += 2


    elif rw == 'write':
        if bs == NP:
            if obs == NP or obs == I:
                proc[proc_id].setModified(mem_block_id)
                state_trans[rw] += 1
                trans[rw] += 1
            elif obs == E:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
                trans[rw] += 1
            elif obs == S:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2 #TODO: Shouldn't this just be 1?
                trans[rw] += 1    
            elif obs == M:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
                trans[rw] += 2
        elif bs == M:
            if obs == NP or obs == I:
                pass
            else:
                assert False
        elif bs == E:
            if obs == NP or obs == I:
                proc[proc_id].setModified(mem_block_id)
                state_trans[rw] += 1
            else:
                assert False
         elif bs == S:
            if obs == IN:
                assert False
            if obs == S:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
                trans[rw]+= 1
                trans[rw] += 1
            else:
                assert False
        elif bs == I:
            if obs == NP or obs == I:
                proc[proc_id].setModified(mem_block_id)
                state_trans[rw] += 1
                trans[rw] += 1
            elif obs == E:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
                trans[rw] += 1
            elif obs == S:
                assert False
            elif obs == M:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2
                trans[rw] += 2

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
        mem_block_id = randrange(NUM_BLOCKS_MEM)
        block_id = mem_block_id%NUM_BLOCKS_CACHE

        for rw in ['read', 'write']:

            #TODO: Understand this. We'll have to write back to memory in this case.
            if (proc[proc_id].getState(mem_block_id) == NP and 
                    proc[proc_id].getBlockState(block_id)==M):
                trans[rw] += 1 
            print 'Proc:', proc_id, ' Mem ', rw, ' location: ', mem_block_id, ' block ID: ', block_id
            block_state = proc[proc_id].getState(mem_block_id)

            #Assuming two processors
            other_block_state = proc[other(proc_id)].getState(mem_block_id)
            print "Current state in ", rw," ", block_state, "; Other block state ", other_block_state
            # Read/Write opn
            if(protocol=='MESI'):
                rwMESI(rw,proc,trans,state_trans,proc_id,mem_block_id,block_id,block_state,other_block_state)
            elif(protocol=='MOESI'):
                rwMOESI(rw,proc,trans,state_trans,proc_id,mem_block_id,block_id,block_state,other_block_state)
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
