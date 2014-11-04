from collections import deque
import params

class ReorderBuffer:
    def __init__(self):
        self.entries = deque()

    def set_issue(self, entry_id):
        for entry in self.entries:
            if entry.index == entry_id:
                entry.issue_bit = True
                return True
        return False

    def add_entry(self, entry):
        if(len(self.entries) >= params.MAX_RB_SIZE):
            return False
        self.entries.append(entry)
        return True

    def popleft(self):
        if len(self.entries)==0 or not self.entries[0].is_finished():
            return False
        if params.instr_type[self.entries[0].index]=='STORE':
            top_entry = self.entries[0]
            if top_entry.store_memory_access:
                return False
            print "Trying to pop 'STORE' inst.", top_entry.index
            assert top_entry.is_finished()
            if (self.buff_size()<params.MAX_STORE_BUFF or params.buffer_validity[0][top_entry.store_address]):
                params.buffer_validity[0][top_entry.store_address] = True
                params.buffer_validity[1][top_entry.store_address] = False
                params.buff[0][top_entry.store_address] = top_entry.store_val
                print 'Storing', top_entry.store_address, top_entry.store_val
                top_entry.complete_bit = True
                params.store_counter -= 1
                print "Store count", params.store_counter
                assert params.store_counter>=0
                self.entries.popleft()
                return True
            else:
                print "Couldn't pop the Store Inst.", top_entry.index
                print "Curr size of mem access queue", len(params.memory_access_queue)
                params.memory_access_queue.append(MemoryAccessEntry(top_entry.index, top_entry, top_entry.store_address))
                top_entry.store_memory_access = True
                return False
        elif params.instr_type[self.entries[0].index] == 'LOAD':
            if not self.entries[0].is_complete():
                return False
            else:
                self.entries.popleft()
                return True
        else:
            if not self.entries[0].is_complete():
                return False
            self.entries.popleft()
            return True

    def buff_size(self):
        size = 0
        for add in params.buffer_validity[0]:
            if params.buffer_validity[0][add]:
                size += 1
        return size


class ReorderBufferEntry:
    def __init__(self, entry_id):
        self.busy_bit = True
        self.issue_bit = False
        self.finish_bit = False
        self.complete_bit = False
        self.index = entry_id
        self.load_val = float("-inf")
        self.store_val = float("+inf")
        self.store_address = -1
        self.store_memory_access = False

    def is_busy(self):
        return self.busy_bit

    def is_issued(self):
        return self.issue_bit

    def is_finished(self):
        return self.finish_bit

    def is_complete(self):
        return self.complete_bit

    def set_load_val(self, val):
        if (not self.is_complete() and self.is_finished()):
            self.load_val = val
            self.complete_bit = True
            return True
        return False

