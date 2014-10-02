# assuming buffer_validity = [{},{}]
from collections import deque

class ReorderBuffer:
    def __init__(self):
        self.entries = deque()

    def set_issue(self, entry_id):
        for entry in self.entries:
            if entry.id == entry_id:
                entry.issue_bit = True
                return True
        return False

    def add_entry(self, entry):
        if(len(self.entries) >= MAX_RB_SIZE):
            return False
        self.entries.append(entry)
        return True

    def popleft(self):
        if len(self.entries)==0 or not self.entries[0].is_finished():
            return False
        if instr_type[self.entries[0].id]=='STORE':
            top_entry = self.entries[0]
            if top_entry.store_memory_access:
                return False
            print "Trying to pop 'STORE' inst.", top_entry.id
            if not top_entry.is_finished():
                print "top entry not finished"
                sys.exit(1)
            if (self.buff_size()<MAX_'STORE'_BUFF or buffer_validity[0][top_entry.store_addreses]):
                buffer_validity[0][top_entry.store_addreses] = True
                buffer_validity[1][top_entry.store_addreses] = False
                buff[0][top_entry.store_addreses] = top_entry.store_val
                top_entry.complete_bit = True
                store_counter -= 1
                print "Store count", store_counter
                if store_counter<0:
                    print "store counter negative"
                    sys.exit(1)
                self.entries.popleft()
                return True
            else:
                print "Couldn't pop the Store Inst.", top_entry.id
                print "Curr size of mem access queue", len(memory_access_queue)
                memory_access_queue.append()
                top_entry.store_memory_access = True
                return False
        elif instr_type[top_entry.id] == 'LOAD':
            if top_entry.is_complete():
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
        for something in buffer_validity:
            if something.first.second == 1 and something.second:
                size += 1
        return size


class ReorderBufferEntry:
    def __init__(self, entry_id):
        self.busy_bit = True;
        self.issue_bit = False;
        self.finish_bit = False;
        self.complete_bit = False;
        self.id = entry_id;
        self.load_val = float("-inf");
        self.store_val = float("+inf");
        self.store_address = -1;
        self.store_memory_access = False;

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



