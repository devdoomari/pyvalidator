class WrongType(Exception):
    def __init__(self, got, instead_of):
        self.error_name = "wrong_type"
        self.got = got
        self.instead_of = instead_of

    def __eq__(self, other):
        return (type(self) == type(other) and other.instead_of ==
                self.instead_of and other.got == self.got)

    def __gt__(self, other):
        return (self.got.__name__ < other.got.__name__ or
                self.instead_of.__name__ < other.instead_of.__name__)

    def __lt__(self, other):
        return (not self.__gt__(other)) and (not self.__eq__(other))

    def __cmp__(self, other):
        if self.__eq__(other):
            return 0
        elif self.__lt__(other):
            return -1
        else:
            return 1

    def __hash__(self):
        return (hash(self.error_name) ^ hash(self.instead_of) ^ hash(self.got))

    def __repr__(self):
        got_str = str(self.got)[7:-2]
        instead_of_str = str(self.instead_of)[7:-2]
        return "Wrong Type: got {0} instead of {1}" \
               .format(got_str, instead_of_str)

    def __str__(self):
        return self.__repr__()
