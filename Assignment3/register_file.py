class RegFileEntry:
    def __init__(self, val):
        self.busy_bit = False
        self.data = OperandTag(0, val)

    def is_busy(self):
        return self.busy_bit

    def get_tag(self):
        return self.data.tag_bit if self.is_busy() else 0

    def get_data(self):
        return float("-inf") if self.is_busy() else self.data.value

    def set_tag(self, tag):
        self.busy_bit = True
        return self.data.set_tag(tag)

    def set_data(self, val):
        self.busy_bit = False
        return self.data.set_value(val)

class OperandTag:
    def __init__(self, tag, val):
        self.tag_bit = tag
        self.value = val

    def is_valid(self):
        return self.tag_bit==0

    def set_value(self, val):
        self.value = val
        return self.set_tag(0)

    def set_tag(self, tag):
        self.tag_bit = tag
        return True
