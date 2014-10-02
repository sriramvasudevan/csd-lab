import sys

class MemoryAccessEntry:
    def __init__(self, entry_id, rb_entry, address):
        self.id = entry_id
        self.time_in_mem = 0
        self.entry = rb_entry
        self.address = address

    def pop(self):
        if len(memory_access_queue)==0:
            return False
        if(not self.entry.is_finished() or self.entry.is_complete):
            sys.exit(1)

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
                if(instr.type[entry.id]==STORE and entry.store_operand.is_valid() and entry.store_operand.tag_bit==entry_id):
                    entry.store_opeand.set_value(result)

