class FuncFail(Exception):
    def __init__(self, func, var):
        self.error_name = "func_fail"
        self.func = func
        self.var = var

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
        return (other.func == self.func and other.var == self.var)

    def __repr__(self):
        func_name = self.func.func_name
        return "'{0}'' failed on validation function '{1}'" \
               .format(self.var, func_name)
