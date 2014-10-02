import params
from register_file import OperandTag

class ReservationStation:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        if(len(self.entries) >= params.MAX_RS_SIZE):
            return False
        self.entries.append(entry)
        return True

    def remove_entry(self, entry_id):
        for entry in self.entries:
            if (entry.index == entry_id and entry.is_valid()):
                    del entry
                    return True
        return False

    def get_alu_entries(self):
        alu_entries = []
        for entry in self.entries:
            if (not params.instr_type[entry.index]=='LOAD' and not params.instr_type[entry.index]=='STORE' and entry.is_valid() and not entry.issued):
                alu_entries.append(entry)
                if(len(alu_entries)==params.NUM_ALU):
                    return alu_entries
        return alu_entries

    def get_load_entries(self):
        for entry in self.entries:
            if(params.instr_type[entry.index]=='LOAD' and entry.is_valid() and not entry.issued):
                return entry
        return None

    def get_store_entries(self):
        for entry in self.entries:
            if(params.instr_type[entry.index]=='STORE' and entry.is_valid() and not entry.issued):
                return entry
        return None

class ReservationStationEntry:
    def __init__(self, entry_id):
        self.index = entry_id
        self.operand1 = self.operand2 = self.store_operand = OperandTag(0,1.0)
        self.issued = False

    def is_valid(self):
        return (self.operand1.is_valid() and self.operand2.is_valid() and (True if not params.instr_type[self.index]=='STORE' else this.store_operand.is_valid()))
