class MissingKey(Exception):
    def __init__(self, key, data):
        self.error_name = "missing_key"
        self.key = key
        self.data = data

    def __eq__(self, other):
        return (other.key == self.key and other.data == self.data)

    def __cmp__(self, other):
        if type(other) != type(self):
            return -1
        if other.data > self.data:
            return -1
        elif other.data < self.data:
            return 1
        if other.key < self.key:
            return 1
        elif other.key > self.key:
            return -1
        return 0

    def __repr__(self):
        data_str = str(self.data)
        key_str = str(self.key)
        return "Missing Key: {0} => {1}" \
               .format(key_str, data_str)
