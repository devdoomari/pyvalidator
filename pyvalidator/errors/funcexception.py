class FuncException(Exception):
    def __init__(self, func, var, exception):
        self.error_name = "func_exception"
        self.func = func
        self.var = var
        self.exception = exception

    def __cmp__(self, other):
        if self.__eq__(other):
            return 0
        elif self.__lt__(other):
            return -1
        else:
            return 1

    def __hash__(self):
        return hash(self.error_name) ^ hash(self.func) ^ hash(self.var) ^ hash(
            self.exception)

    def __gt__(self, other):
        return (self.func < other.func or self.var < other.var or
                self.exception < other.exception)

    def __lt__(self, other):
        return (not self.__gt__(other)) and (not self.__eq__(other))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (other.func == self.func and other.var == self.var and
                other.exception == self.exception)

    def __repr__(self):
        func_name = self.func.__name__
        return "Exception '{0}'' from function '{1}' ({2}) " \
            .format(self.exception, func_name, self.var)

    def __str__(self):
        return self.__repr__()
