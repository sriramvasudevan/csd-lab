from reservation_station import ReservationStationEntry

class FunctionalUnit:

    def __init__(self):
        self.busy = False
        self.time_in_fu = 1
        self.entry = None

    def is_busy(self):
        return self.busy

    def set_instruction(self, i_entry):
        if self.is_busy() or not i_entry.is_valid():
            return False
        self.entry = i_entry
        self.busy = True
        self.entry.issued = True
        rob.set_issue(self.entry.id)
        return True

    def execute_load_instruction(self ):
        if not self.is_busy() and not self.entry.is_valid():
            return False

        result = self.entry.operand1.value + self.entry.operand2.value
        self.time_in_fu = 1

        self.update_reorder_buffer(self.entry.id,instr_type[self.entry.id],result)
        rs.remove_entry(self.entry.id)

        return remove_instruction()

    def execute_store_instruction(self ):
        if not self.is_busy() and not self.entry.is_valid():
            return False

        result = self.entry.operand1.value + self.entry.operand2.value
        self.time_in_fu = 1

        self.update_reorder_buffer(self.entry.id,instr_type[self.entry.id],result)
        rs.remove_entry(self.entry.id)

        return remove_instruction()

    def execute_instruction(self ):
        if not self.is_busy() and not self.entry.is_valid():
            return False

        result = -1
        itype = instr_type[self.entry.id]

        if itype == 'ADD':
            result = self.entry.operand1.value + self.entry.operand2.value
        if itype == 'SUB':
            result = self.entry.operand1.value - self.entry.operand2.value
        if itype == 'MUL':
            result = self.entry.operand1.value * self.entry.operand2.value
        if itype == 'DIV':
            result = self.entry.operand1.value / self.entry.operand2.value
        if itype == 'AND':
            result = self.entry.operand1.value & self.entry.operand2.value
        if itype == 'OR':
            result = self.entry.operand1.value | self.entry.operand2.value
        if itype == 'XOR':
            result = self.entry.operand1.value ^ self.entry.operand2.value

        self.time_in_fu = 1
        self.update_register_file(self.entry.id, result)
        self.update_reservation_station(self.entry.id, result)
        self.update_reorder_buffer(self.entry.id, result)

        rs.remove_entry(self.entry.id)

        return remove_instruction()

        def remove_instruction(self ):
            if not self.is_busy():
                return False
            self.entry = None
            self.busy = False
            return True

        def update_register_file(self, i_id, result):
            for reg in registers:
                if reg.is_busy() and reg.data.tag_bit == i_id:
                    reg.set_data(result)

        def update_reservation_station(self, i_id, result):

            for entry in rs.entries:
                if not entry.is_valid():
                    if not entry.operand1.is_valid() and entry.operand1.tag_bit == i_id:
                        entry.operand1.set_value(result)
                    if not entry.operand2.is_valid() and entry.operand2.tag_bit == i_id:
                        entry.operand2.set_value(result)

                    if instr_type[entry.id] == 'STORE' and not entry.store_operand.is_valid() and entry.store_operand.tag_bit == id:
                        entry.store_operand.set_value(result)
                        
        def update_reorder_buffer(self, i_id,itype,result):
            address = int(result)
            if itype == 'LOAD':
                for entry in rob.entries:
                    if entry.id == i_id:
                        if buffer_validity[(address,1)]: #TODO
                            entry.load_val = buffer[(address,1)]
                            self.update_register_file(i_id,entry.load_val)
                            self.update_reservation_station(i_id,entry.load_val)
                            entry.finish_bit = True
                            entry.complete_bit = True
                        else:
                            entry.finish_bit = True
                            memory_access_queue.append(MemoryAccessEntry(i_id,entry,address)
                        return
            elif type == 'STORE':
                for entry in rob.entries:
                    if entry.id == i_id:
                        entry.store_val = entry.store_operand.value
                        entry.store_address = address
                        entry.finish_bit = True
                        return


        def update_reorder_buffer(self, i_id):
            for entry in rob.entries:
                if entry.is_busy() and entry.is_issued() and entry.id == i_id:
                    entry.finish_bit = True
                    entry.complete_bit = True
                    return

        def increment_time(self):
            if self.is_busy():
                self.time_in_fu += 1
                return True
            return False

        def instruction_wait_done(self):
            if self.is_busy():
                itype = instr_type[self.entry.id]
                if itype == 'LOAD' or itype == 'STORE':
                    itype = 'ADD'
            
                assert self.time_in_fu <= latency[itype]

                if self.time_in_fu >= latency[itype]:
                    return True
                return False
            return True