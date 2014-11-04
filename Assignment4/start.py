from cache import Cache
from params import *
from random import randrange,choice

def other(proc_id):
    return (proc_id+1)%2

def rwMOESI(rw,proc,trans,state_trans,proc_id,mem_block_id,block_id,bs,obs):
    if rw == 'read':
        if bs == NP or bs == I:
            #BusRd request
            trans[rw] += 1
            if obs == NP or obs == I:
                proc[proc_id].setExclusive(mem_block_id)
                state_trans[rw] += 1
            elif obs == E:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2
            elif obs == S:
                proc[proc_id].setShared(mem_block_id)
                state_trans[rw] += 1
            elif obs == M:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setOwned(mem_block_id)
                state_trans[rw] += 2
            elif obs == O:
                proc[proc_id].setShared(mem_block_id)
                state_trans[rw] += 1
        elif bs == M:
            #The other processor shouldn't be in any other state
            assert obs == NP or obs == I
        elif bs == E:
            #The other processor shouldn't be in any other state
            assert obs == NP or obs == I
        elif bs == S:
            assert obs == NP or obs == I or obs == S or obs == O
        elif bs == O:
            assert obs == NP or obs == I or obs == S

    elif rw == 'write':
        if bs == NP or bs == I:
            #busreadx request
            trans[rw] += 1
            if obs == NP or obs == I:
                proc[proc_id].setModified(mem_block_id)
                state_trans[rw] += 1
            elif obs == E:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
            elif obs == S:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2 
            elif obs == M:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
            elif obs == O:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
        elif bs == M:
            assert obs == NP or obs == I
        elif bs == E:
            assert obs == NP or obs == I
            proc[proc_id].setModified(mem_block_id)
            state_trans[rw] += 1
        elif bs == S:
            assert obs != M and obs != E
            #BusrdX request
            trans[rw] += 1
            proc[proc_id].setModified(mem_block_id)
            state_trans[rw] += 1
            if obs == S:
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 1
            elif obs == O:
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 1
        elif bs == O:
            assert obs != M and obs != E and obs != O
            #BusrdX request
            trans[rw] += 1
            proc[proc_id].setModified(mem_block_id)
            state_trans[rw] += 1
            if obs == S:
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 1

def rwMESI(rw,proc,trans,state_trans,proc_id,mem_block_id,block_id,bs,obs):
    if rw == 'read':
        if bs == NP or bs == I:
            #BusRd request
            trans[rw] += 1
            if obs == NP or obs == I:
                proc[proc_id].setExclusive(mem_block_id)
                state_trans[rw] += 1
            elif obs == E:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2
            elif obs == S:
                proc[proc_id].setShared(mem_block_id)
                state_trans[rw] += 1
            elif obs == M:
                proc[proc_id].setShared(mem_block_id)
                proc[other(proc_id)].setShared(mem_block_id)
                state_trans[rw] += 2
        elif bs == M:
            #The other processor shouldn't be in any other state
            assert obs == NP or obs == I
        elif bs == E:
            #The other processor shouldn't be in any other state
            assert obs == NP or obs == I
        elif bs == S:
            assert obs == NP or obs == I or obs == S

    elif rw == 'write':
        if bs == NP or bs == I:
            #busreadx request
            trans[rw] += 1
            if obs == NP or obs == I:
                proc[proc_id].setModified(mem_block_id)
                state_trans[rw] += 1
            elif obs == E:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
            elif obs == S:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2 
            elif obs == M:
                proc[proc_id].setModified(mem_block_id)
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 2
        elif bs == M:
            assert obs == NP or obs == I
        elif bs == E:
            assert obs == NP or obs == I
            proc[proc_id].setModified(mem_block_id)
            state_trans[rw] += 1
        elif bs == S:
            assert obs != M and obs != E
            #BusrdX request
            trans[rw] += 1
            proc[proc_id].setModified(mem_block_id)
            state_trans[rw] += 1
            if obs == S:
                proc[other(proc_id)].setInvalidate(mem_block_id)
                state_trans[rw] += 1

def simulate(protocol='MESI'):
    proc = [Cache(), Cache()]
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

        rw = choice(['read','write'])

        block_state = proc[proc_id].getState(mem_block_id)

        #TODO: Verify that it's okay to comment this.
#        if (block_state == NP or block_state == I) and 
#                proc[proc_id].getBlockState(block_id)==M:
#            trans[rw] += 1 
#            print 'Proc:', proc_id, ' Mem ', rw, ' location: ', mem_block_id, ' block ID: ', block_id

        #Assuming two processors
        other_block_state = proc[other(proc_id)].getState(mem_block_id)
#            print "Current state in ", rw," ", block_state, "; Other block state ", other_block_state
        # Read/Write opn
        if(protocol=='MESI'):
            rwMESI(rw,proc,trans,state_trans,proc_id,mem_block_id,block_id,block_state,other_block_state)
        elif(protocol=='MOESI'):
            rwMOESI(rw,proc,trans,state_trans,proc_id,mem_block_id,block_id,block_state,other_block_state)
        iternos += 1
        if iternos%100000 == 0:
            print iternos
        
    print "No. iterations:", iternos
    print "Read coherence places:", trans['read']
    print "Write coherence places:", trans['write']
    print "Read State transactions:", state_trans['read']
    print "Write State transactions:", state_trans['write']
    print
    print "Total coherence places:", trans['write'] + trans['read']
    print "Total state transactions:", state_trans['read'] + state_trans['write']


if __name__=="__main__":
    for protocol in ['MESI', 'MOESI']:
        print protocol, "Protocol Simulation:"
        simulate(protocol)
