import sys
from register_file import RegFileEntry, OperandTag
from reorder_buffer import ReorderBuffer, ReorderBufferEntry
from reservation_station import ReservationStation, ReservationStationEntry
from params import *
from instruction import Instruction
from collections import deque

#Dict from type of latency ('add', 'mul' etc) to the int value
latency = {}

#Our registers
registers = []

#Our reorder buffer
rb = ReorderBuffer()

#Our reservation station
rs = ReservationStation

#A list of instructions
all_instructions = []

memory_access_queue = deque()

#A dict from instruction id to its type
instr_type = {}

#A map from integer tuple (a,b) to a double, and a bool for validity
buffer_map = {}
buffer_validity = [{}, {}]

def copy_buffer_mem(): #TODO
    address = []
    for something in buffer_validity:
        if something.first.second == 2:
            continue
        if something.ss:
            address.append(somthing.first.first)
            if(len(address)==bandwidth):
                break
    for a in address:
        buff[1][a] = buff[0][a]
        buffer_validity[0][a] = False
        buffer_validity[1][a] = True

def store_buffer_empty(): #TODO
    for something in buffer_validity:
        if something.first.second==1 and something.second:
            return False
    return True

def populate_instructions():

    global global_ins_counter

    codefilename = 'codefile.s'

    #If the code file is given as an argument:
    if len(sys.argv)>1:
        codefilename = sys.argv[1]

    with open(codefilename,'r') as codefile:
        for line in codefile:
            spline = line.split()
            if len(spline) == 4: #ALU
                all_instructions.append(Instruction(spline[0],spline[1],spline[2],spline[3],global_ins_counter))
            if len(spline) == 3: #Load/Store
                all_instructions.append(Instruction(spline[0],spline[1],spline[2],None,global_ins_counter))
            else:
                #Weird instruction
                print 'WEIRD INSTRUCTION: ' + line
                assert False
            instr_type[global_ins_counter] = spline[0]
            global_ins_counter += 1

def read_input_latencies():
    with open('latencies.txt','r') as latencyfile:
        for line in latencyfile:
            spline = line.split()
            latency[spline[0]] = int(spline[1])

def simulate():

    cycle_no = 1
    iq = deque()
    curr_index = 0
    global store_counter

    while True:
        while len(iq) < MAX_INSTR and curr_index < len(all_instructions):
            if all_instructions[curr_index].opcode=='LOAD' and store_counter != 0:
                break
            iq.append(all_instructions[curr_index])
            curr_index += 1

        if len(iq) == 0 and len(rb.entries) == 0 and curr_index >= len(all_instructions) and len(memory_access_queue) == 0:
            break

        #Index into instruction queue
        iq_i = 0
        while iq_i < len(iq):
            instr = iq[0]

            if store_counter != 0 and instr.opcode == 'LOAD':
                break

            if len(rs.entries)>= MAX_RESERVATION_STATION or len(rb.entries) >= MAX_REORDER_BUFFER:
                break
            print 'Next instruction: ID ' + str(instr.index)

            rsentry = ReservationStationEntry(instr.index)
            assert rs.add_entry(rsentry)

            iq.popleft()

            if instr.opcode != 'LOAD' and instr.opcode != 'STORE':
                print 'Alu instruction: ID ' + str(instr.index)

                if instr.src1[0] == 'R':
                    reg1 = int(instr.src1[1:])
                else:
                    reg1 = None
                if instr.src2[0] == 'R':
                    reg2 = int(instr.src2[1:])
                else:
                    reg2 = None
                regdest = int(instr.dest[1:])

                if reg1:
                    if registers[reg1].is_busy():
                        entry.operand1.set_tag(registers[reg1].get_tag())
                    else:
                        entry.operand1.set_value(registers[reg1].get_data())
                #If it's an immediate value
                else:
                    entry.operand1.set_value(int(instr.src1))

                 if reg2:
                    if registers[reg2].is_busy():
                        entry.operand2.set_tag(registers[reg2].get_tag())
                    else:
                        entry.operand2.set_value(registers[reg2].get_data())
                #If it's an immediate value
                else:
                    entry.operand2.set_value(int(instr.src2))
                
                registers[regdest].set_tag(instr.index)

                rb.add_entry(ReorderBufferEntry(instr.index))

            elif instr.opcode == 'STORE':
                print 'Store instruction: ID ' + instr.index

                store_counter += 1
                #Store to register. TODO: Other case.
                if instr.dest[0] == 'R':
                    regdest = int(instr.dest[1:])

                    reg1 = int(instr.src1[1:])
                    if registers[reg1].is_busy():
                        entry.operand1.set_tag(registers[reg1].get_tag())
                    else:
                        entry.operand1.set_value(registers[reg1].get_value())

                    if registers[regdest].is_busy():
                        entry.store_operand.set_tag(registers[regdest].get_tag())
                    else:
                        entry.store_operand.set_value(registers[regdest].get_data())

                rb.add_entry(ReorderBufferEntry(instr.index))
        
        entries = rs.get_alu_entries()
        j = 0
        for i in range(NUM_ALU):
            if j >= len(entries):
                break
            if fu[i].set_instruction(entries[j]):
                print 'Setting alu ' + str(i) + ' the instruction ' + entries[j].id
                j += 1
        entry = rs.get_load_entries()
        if entry:
            if load_fu.set_instruction(entry):
                print 'Setting load fu to ' + entry.id
        entry = rs.get_store_entries()
        if entry:
            if store_fu.set_instruction(entry):
                print 'Setting store fu to ' + entry.id

        for i in range(NUM_ALU):
            print 'FU ' + str(i)
            if fu[i].is_busy():
                if fu[i].instruction_wait_done():
                    print 'Instruction ' + fu[i].entry.id + ' in ALU ' + str(i) + ' is done.'
                    fu[i].execute_instruction()
                else:
                    fu[i].increment_time()

        if load_fu.is_busy():
            print 'LOAD FU'
            if load_fu.instruction_wait_done():
                print 'Instruction ' + load_fu.entry.id + ' in load FU is done.'
                load_fu.execute_load_instruction()
            else:
                load_fu.increment_time()

        if store_fu.is_busy():
            if store_fu.instruction_wait_done():
                print 'Instruction ' + store_fu.entry.id + ' in store FU is done.'
                store_fu.execute_store_instruction()
            else:
                store_fu.increment_time()

        while rb.popleft():
            pass

        if len(memory_access_queue) > 0:
            top_elem = memory_access_queue[0]
            if instr_type[top_elem.index] == 'STORE':
                if top_elem.time_in_mem < latency['STORE']:
                    print 'Waiting time for store in queue ' + str(top_elem.time_in_mem)
                    top_elem.time_in_mem += 1
                else:
                    copy_buffer_mem()
                    print 'Flushing store buffer.'
                    if store_buffer_empty():
                        top_elem.popleft()
                    else:
                        top_elem.time_in_mem = 0
            if instr_type[top_elem.index] == 'LOAD':
                if top_elem.time_in_mem < latency['LOAD']:
                    top_elem.time_in_mem += 1
                else:
                    top_elem.popleft()

        while rb.popleft():
            pass

        print 'RX Value Busy Tag'
        i = 0
        for reg in registers:
            print str(i) + ' ' + str(reg.data.value) + ' ' + str(reg.busy_bit) + ' ' + str(reg.get_tag())
            i += 1


        print 'End of cycle ' + cycle_no
        cycle_no += 1

if __name__ == "__main__":
    read_input_latencies()

    for i in range(MAX_REGISTERS):
        registers.append(RegFileEntry(i))

    buffer_map[(0,1)] = 10
    buffer_map[(4,1)] = 5
    buffer_map[(8,1)] = 4
    buffer_map[(12,1)] = 7

    buffer_validity[0][0] = True
    buffer_validity[0][4] = True
    buffer_validity[0][8] = True
    buffer_validity[0][12] = True

    populate_instructions()
    simulate()
