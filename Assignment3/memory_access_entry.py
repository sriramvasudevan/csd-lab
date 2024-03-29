import params

class MemoryAccessEntry:
    def __init__(self, entry_id, rb_entry, address):
        self.index = entry_id
        self.time_in_mem = 0
        self.entry = rb_entry
        self.address = address

    def popleft(self):
        if len(params.memory_access_queue)==0:
            return False
        assert (self.entry.is_finished() and not self.entry.is_complete())
        if params.instr_type[self.entry.index] == 'LOAD':
            assert not params.buffer_validity[0][self.address]
            self.entry.set_load_val(params.buff[1][self.address])
            self.update_regfile(self.index, self.entry.load_val)
            self.update_reservation_station(self.index, self.entry.load_val)

        elif params.instr_type[self.entry.index] == 'STORE':
            #This implies the current rb head is a 'STORE'
            assert (len(params.rb.entries)>0 and params.instr_type[params.rb.entries[0].index]=='STORE')
            #popleft function will take care of writing the store value in store buffer and popping it
            self.entry.store_memory_access = False
            params.rb.popleft()
  
        params.memory_access_queue.popleft()
        return True


    def update_regfile(self, entry_id, result):
        for reg in params.registers:
            if reg.is_busy() and reg.data.tag_bit==entry_id:
                reg.set_data(result)

    def update_reservation_station(self, entry_id, result):
        for entry in params.rs.entries:
            if entry.is_valid():
                if(not entry.operand1.is_valid() and entry.operand1.tag_bit==entry_id):
                    entry.operand1.set_value(result)
                if(not entry.operand2.is_valid() and entry.operand2.tag_bit==entry_id):
                    entry.operand2.set_value(result)
                if(params.instr_type[entry.index]=='STORE' and entry.store_operand.is_valid() and entry.store_operand.tag_bit==entry_id):
                    entry.store_opeand.set_value(result)

