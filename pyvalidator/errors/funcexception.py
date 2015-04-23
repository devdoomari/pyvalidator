class FuncException(Exception):
    def __init__(self, func, var, exception):
        self.error_name = "func_exception"
        self.func = func
        self.var = var
        self.exception = exception

    def __cmp__(self, other):
        if type(other) != type(self):
            return -1
        if other.func > self.func:
            return -1
        elif other.func < self.func:
            return 1
        if other.var < self.var:
            return 1
        elif other.var > self.var:
            return -1
        return 0

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (other.func == self.func and other.var == self.var and
                other.exception == self.exception)

    def __repr__(self):
        func_name = self.func.func_name
        return "Exception '{0}'' from function '{1}' ({2}) " \
            .format(self.exception, func_name, self.var)
