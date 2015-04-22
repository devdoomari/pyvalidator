class NotEqual(Exception):
    def __init__(self, instead_of, got):
        self.instead_of = instead_of
        self.got = got

    def __eq__(self, other):
        return (other.instead_of == self.instead_of and other.got == self.got)

    def __cmp__(self, other):
        if type(other) != type(self):
            return -1
        if other.got > self.got:
            return -1
        elif other.got < self.got:
            return 1
        if other.instead_of < self.instead_of:
            return 1
        elif other.instead_of > self.instead_of:
            return -1
        return 0

    def __repr__(self):
        got_str = str(self.got)[7:-2]
        instead_of_str = str(self.instead_of)[7:-2]
        return "Not Equal: got {0} instead of {1}" \
               .format(got_str, instead_of_str)
