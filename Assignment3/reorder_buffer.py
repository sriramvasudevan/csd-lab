def ReorderBuffer:
    def __init__(self):
        self.entries = None

    def add_entry(self, entry):
        if(len(self.entries) >= MAX_RB_SIZE):
            return False
        self.entries.append(entry) #TODO: Check this
        return True

    def pop_entry(self, entry_id):
        if len(self.entries)==0 or !self.entries[-1].is_finished():
            return False
        if self.entries[-1].is_store():
            top_entry = self.entries[-1]
            if top_entry.store_memory_access:
                return False
            print "Trying to pop STORE inst.", top_entry.id
            print top_entry.is_finished()
            if (self.buff_size()<MAX_STORE_BUFF or buffer_validity[mp(top_entry.store_addreses,1)]):
                buffer_validity[mp(top_entry.store_addreses,1)] = True
                buffer_validity[mp(top_entry.store_addreses,2)] = False
                buff[mp(top_entry.store_addreses,1)] = top_entry.store_val
        for entry in self.entries:
            if (entry.id == entry_id and entry.is_valid()):
                    del entry
                    return True
        return False

    def get_alu_entries(self):
        alu_entries = []
        for entry in self.entries:
            if (!entry.is_load() and !entry.is_store() and entry.is_valid() and !entry.is_issued()):
                alu_entries.append(entry)
                if(len(alu_entries)==NUM_ALU):
                    return alu_entries
        return alu_entries

    def get_load_entries(self):
        for entry in self.entries:
            if(entry.is_load() and entry.is_valid() and !entry.is_issued()):
                return entry
        return None

    def get_store_entries(self):
        for entry in self.entries:
            if(entry.is_store() and entry.is_valid() and !entry.is_issued()):
                return entry
        return None

def ReservationStationEntry:
    def __init__(self, entry_id):
        this.id = entry_id
        this.operand1 = this.operand2 = this.store_operand = None
        this.issued = False

    def is_valid(self):
        if self.is_store()
        return (self.operand1.is_valid() and self.operand2.is_valid() and (True if !entry.is_store() else this.store_operand.is_valid()))

