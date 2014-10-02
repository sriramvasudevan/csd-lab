import sys
from register_file import RegFileEntry
from reorder_buffer import ReorderBufferEntry
from reservation_station import ReservationStationEntry
from functional_unit import FunctionalUnit
import params
from instruction import Instruction
from collections import deque

load_fu = FunctionalUnit()
store_fu = FunctionalUnit()

def copy_buffer_mem():
    address = []
    for add in params.buffer_validity[0]:
        if params.buffer_validity[0][add]:
            address.append(add)
            if(len(address)==bandwidth):
                break
    for a in address:
        params.buff[1][a] = params.buff[0][a]
        params.buffer_validity[0][a] = False
        params.buffer_validity[1][a] = True

def store_buffer_empty():
    for add in params.buffer_validity[0]:
        if params.buffer_validity[0][add]:
            return False
    return True

def populate_instructions():

    codefilename = 'codefile.s'

    #If the code file is given as an argument:
    if len(sys.argv)>1:
        codefilename = sys.argv[1]

    with open(codefilename,'r') as codefile:
        for line in codefile:
            spline = line.split()
            if len(spline) == 4: #ALU
                params.all_instructions.append(Instruction(spline[0],spline[1],spline[2],spline[3],params.global_ins_counter))
            elif len(spline) == 3: #Load/Store
                params.all_instructions.append(Instruction(spline[0],spline[1],spline[2],None,params.global_ins_counter))
            else:
                #Weird instruction
                print 'WEIRD INSTRUCTION:', line
                assert False
            params.instr_type[params.global_ins_counter] = spline[0]
            params.global_ins_counter += 1

def read_input_latencies():
    with open('latencies.txt','r') as latencyfile:
        for line in latencyfile:
            spline = line.split()
            params.latency[spline[0]] = int(spline[1])

def simulate():

    cycle_no = 1
    iq = deque()
    curr_index = 0

    while True:
        while len(iq) < params.MAX_INSTR and curr_index < len(params.all_instructions):
            if params.all_instructions[curr_index].opcode=='LOAD' and params.store_counter != 0:
                break
            iq.append(params.all_instructions[curr_index])
            curr_index += 1

        if len(iq) == 0 and len(params.rb.entries) == 0 and curr_index >= len(params.all_instructions) and len(params.memory_access_queue) == 0:
            break

        #Index into instruction queue
        iq_i = 0
        while iq_i < len(iq):
            instr = iq[0]

            if params.store_counter != 0 and instr.opcode == 'LOAD':
                break

            if len(params.rs.entries)>= params.MAX_RS_SIZE or len(params.rb.entries) >= params.MAX_RB_SIZE:
                break
            print 'bext instruction: ID', instr.index

            entry = ReservationStationEntry(instr.index)
            assert params.rs.add_entry(entry)

            iq.popleft()

            if instr.opcode != 'LOAD' and instr.opcode != 'STORE':
                print 'Alu instruction: ID', instr.index

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
                    if params.registers[reg1].is_busy():
                        entry.operand1.set_tag(params.registers[reg1].get_tag())
                    else:
                        entry.operand1.set_value(params.registers[reg1].get_data())
                #If it's an immediate value
                else:
                    entry.operand1.set_value(int(instr.src1))

                if reg2:
                    if params.registers[reg2].is_busy():
                        entry.operand2.set_tag(params.registers[reg2].get_tag())
                    else:
                        entry.operand2.set_value(params.registers[reg2].get_data())
                #If it's an immediate value
                else:
                    entry.operand2.set_value(int(instr.src2))
                
                params.registers[regdest].set_tag(instr.index)

                params.rb.add_entry(ReorderBufferEntry(instr.index))

            elif instr.opcode == 'STORE':
                print 'Store instruction: ID ', instr.index

                params.store_counter += 1
                #Store to register. TODO: Other case.
                if instr.dest[0] == 'R':
                    regdest = int(instr.dest[1:])
                    if params.registers[regdest].is_busy():
                        entry.store_operand.set_tag(params.registers[regdest].get_tag())
                    else:
                        entry.store_operand.set_value(params.registers[regdest].get_data())

                else:
                    entry.store_operand.set_value(int(instr.dest))
                reg1 = int(instr.src1[1:])
                if params.registers[reg1].is_busy():
                    entry.operand1.set_tag(params.registers[reg1].get_tag())
                else:
                    entry.operand1.set_value(params.registers[reg1].get_data())

                params.rb.add_entry(ReorderBufferEntry(instr.index))

            elif instr.opcode == 'LOAD':
                params.registers[int(instr.dest[1:])].set_tag(instr.index)
        
        entries = params.rs.get_alu_entries()
        j = 0
        for i in range(params.NUM_ALU):
            if j >= len(entries):
                break
            if params.fu[i].set_instruction(entries[j]):
                print 'Setting alu ', i, ' the instruction ', entries[j].index
                j += 1
        entry = params.rs.get_load_entries()
        if entry:
            if load_fu.set_instruction(entry):
                print 'Setting load fu to ', entry.index
        entry = params.rs.get_store_entries()
        if entry:
            if store_fu.set_instruction(entry):
                print 'Setting store fu to ', entry.index

        for i in range(params.NUM_ALU):
            print 'FU ', i
            if params.fu[i].is_busy():
                if params.fu[i].instruction_wait_done():
                    print 'Instruction ', params.fu[i].entry.index, ' in ALU ', i, ' is done.'
                    params.fu[i].execute_instruction()
                else:
                    params.fu[i].increment_time()

        if load_fu.is_busy():
            print 'LOAD FU'
            if load_fu.instruction_wait_done():
                print 'Instruction ', load_fu.entry.index, ' in load FU is done.'
                load_fu.execute_load_instruction()
            else:
                load_fu.increment_time()

        if store_fu.is_busy():
            if store_fu.instruction_wait_done():
                print 'Instruction ', store_fu.entry.index, ' in store FU is done.'
                store_fu.execute_store_instruction()
            else:
                store_fu.increment_time()

        while params.rb.popleft():
            pass

        if len(params.memory_access_queue) > 0:
            top_elem = params.memory_access_queue[0]
            if params.instr_type[top_elem.index] == 'STORE':
                if top_elem.time_in_mem < params.latency['STORE']:
                    print 'Waiting time for store in queue ', top_elem.time_in_mem
                    top_elem.time_in_mem += 1
                else:
                    copy_buffer_mem()
                    print 'Flushing store buffer.'
                    if store_buffer_empty():
                        top_elem.popleft()
                    else:
                        top_elem.time_in_mem = 0
            if params.instr_type[top_elem.index] == 'LOAD':
                if top_elem.time_in_mem < params.latency['LOAD']:
                    top_elem.time_in_mem += 1
                else:
                    top_elem.popleft()

        while params.rb.popleft():
            pass

        print 'RX Value Busy Tag'
        i = 0
        for reg in params.registers:
            print i, reg.data.value, reg.busy_bit, reg.get_tag()
            i += 1

        print 'Reservation station entries:'
        for entry in params.rs.entries:
            print entry.index


        print 'End of cycle ', cycle_no
        cycle_no += 1

if __name__ == "__main__":
    params.initvars()
    read_input_latencies()

    for i in range(params.MAX_REGISTERS):
        params.registers.append(RegFileEntry(i))

    params.buff[0][0] = 10
    params.buff[0][4] = 5
    params.buff[0][8] = 4
    params.buff[0][12] = 7

    params.buffer_validity[0][0] = True
    params.buffer_validity[0][4] = True
    params.buffer_validity[0][8] = True
    params.buffer_validity[0][12] = True

    populate_instructions()
    simulate()
