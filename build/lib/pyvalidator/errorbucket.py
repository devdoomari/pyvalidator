from utils import OrderedList


class ErrorBucket:
    def __init__(self):
        self.errors = {}
        self.custom_errors = []

    def addError(self, var_name, err_obj):
        err_type = err_obj.error_name
        if err_type not in self.errors:
            self.errors[err_type] = {}
        if var_name in self.errors[err_type]:
            if type(self.errors[err_type][var_name]) != OrderedList:
                self.errors[err_type][var_name] = \
                    OrderedList(self.errors[err_type][var_name])
            self.errors[err_type][var_name].add(err_obj)
        else:
            self.errors[err_type][var_name] = err_obj

    def addCustomError(self, error):
        self.custom_errors.append(error)

    def mergeChildBucket(self, child, child_namespace):
        child_namespace = str(child_namespace)
        self.__mergeBucket__(child, child_namespace + '.')

    def mergeBucket(self, child):
        self.__mergeBucket__(child, '')

    def __mergeBucket__(self, child, append_ns):
        append_ns = str(append_ns)
        for err_type in child.errors:
            child_var_list = child.errors[err_type]
            if err_type not in self.errors:
                self.errors[err_type] = {}
            for child_var in child_var_list:
                new_var_name = append_ns + child_var
                storage = self.errors[err_type]
                to_store = child.errors[err_type][child_var]
                if new_var_name in storage:
                    if type(storage[new_var_name]) != OrderedList:
                        storage[new_var_name] = OrderedList(
                            storage[new_var_name])
                    storage[new_var_name].add(to_store)
                else:
                    storage[new_var_name] = to_store
        for child_custom_err in child.custom_errors:
            self.custom_errors.append(child_custom_err)

    def isEmpty(self):
        return self.errors == {} and self.custom_errors == []

    def countErrors(self):
        count = 0
        for err_type in self.errors:
            for var_name in self.errors[err_type]:
                var_err = self.errors[err_type][var_name]
                if type(var_err) == OrderedList:
                    count = count + len(var_err)
                else:
                    count = count + 1
        return count

    def countCustomErrors(self):
        return len(self.custom_errors)