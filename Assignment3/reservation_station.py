def ReservationStation:
    def __init__(self):
        self.entries = None

    def add_entry(self, entry):
        if(len(self.entries) >= MAX_RS_SIZE):
            return False
        self.entries.append(entry) #TODO: Check this
        return True

    def remove_entry(self, entry_id):
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
