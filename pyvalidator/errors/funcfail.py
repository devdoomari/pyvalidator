class FuncFail(Exception):
    def __init__(self, func, var):
        self.error_name = "func_fail"
        self.func = func
        self.var = var

    def __cmp__(self, other):
        if self.__eq__(other):
            return 0
        elif self.__lt__(other):
            return -1
        else:
            return 1

    def __hash__(self):
        return (hash(self.error_name) ^ hash(self.func) ^ hash(self.var))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (
            other.func.__name__ == self.func.__name__ and other.var == self.var
        )

    def __gt__(self, other):
        return (self.func.__name__ < other.func.__name__ or
                self.var < other.var)

    def __lt__(self, other):
        return (not self.__gt__(other)) and (not self.__eq__(other))

    def __repr__(self):
        func_name = self.func.__name__
        return "'{0}'' failed on validation function '{1}'" \
               .format(self.var, func_name)

    def __str__(self):
        return self.__repr__()
