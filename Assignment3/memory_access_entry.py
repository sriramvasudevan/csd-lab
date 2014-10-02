import sys

class MemoryAccessEntry:
    def __init__(self, entry_id, rb_entry, address):
        self.id = entry_id
        self.time_in_mem = 0
        self.entry = rb_entry
        self.address = address

    def popleft(self):
        if len(memory_access_queue)==0:
            return False
        if(not self.entry.is_finished() or self.entry.is_complete):
            print "entry not finished or entry completed"
            sys.exit(1)
        if instr_type[self.entry.id] == 'LOAD':
            if buffer_validity[0][self.address]:
                print "buffer validity non-zero"
                sys.exit(1)
            self.entry.set_load_val(buff[1][self.address]);
            self.update_regfile(self.id, self.entry.load_val);
            self.update_reservation_station(self.id, self.entry.load_val);

        elif instr_type[self.entry.id] == 'STORE':
            #This implies the current rb head is a 'STORE'
            if(not len(rb.entries)>0 or not instr_type[rb.entries[0].id]=='STORE'):
                print "rb entries zero or inst type not store"
                sys.exit(1)
            #popleft function will take care of writing the store value in store buffer and popping it
            self.entry.store_memory_access = False;
            rb.popleft();
  
        memory_access_queue.popleft();
        return True;


    def update_regfile(self, entry_id, result):
        for reg in registers:
            if reg.is_busy() and reg.data.tag_bit==entry_id:
                reg.set_data(result)

    def update_reservation_station(self, entry_id, result):
        for entry in rs.entries:
            if entry.is_valid():
                if(not entry.operand1.is_valid() and entry.operand1.tag_bit==entry_id):
                    entry.operand1.set_value(result)
                if(not entry.operand2.is_valid() and entry.operand2.tag_bit==entry_id):
                    entry.operand2.set_value(result)
                if(instr_type[entry.id]=='STORE' and entry.store_operand.is_valid() and entry.store_operand.tag_bit==entry_id):
                    entry.store_opeand.set_value(result)

