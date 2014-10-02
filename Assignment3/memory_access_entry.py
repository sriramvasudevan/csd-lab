def MemoryAccessEntry:
    def __init__(self, entry_id, rb_entry, address):
        self.id = entry_id
        self.time_in_mem = 0
        self.entry = rb_entry
        self.address = address

    def pop(self):
        if len(memory_access_queue)==0:
            return False
        pass

    def update_regfile(self, entry_id, result):
        registers = [x.set_data(result) for x in registers if x.is_busy() and x.data.tag_bit==entry_id]

    def update_reservation_station(self, entry_id, result):
        for entry in rs.entries:
            if entry.get_entry_valid():
                if(!entry.operand1.is_valid() and entry.operand1.tag_bit==entry_id):
                    entry.operand1.set_value(result)
                if(!entry.operand2.is_valid() and entry.operand2.tag_bit==entry_id):
                    entry.operand2.set_value(result)
                if(entry.is_store() and entry.store_operand.is_valid() and entry.store_operand.tag_bit==entry_id):
                    entry.store_opeand.set_value(result)

