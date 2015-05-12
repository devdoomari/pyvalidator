class MissingKey(Exception):
    def __init__(self, key, data):
        self.error_name = "missing_key"
        self.key = key
        self.data = data

    def __eq__(self, other):
        return (other.key == self.key and other.data == self.data)

    def __gt__(self, other):
        return (self.key < other.key or self.data < other.data)

    def __lt__(self, other):
        return (not self.__gt__(other)) and (not self.__eq__(other))

    def __hash__(self):
        return (hash(self.error_name) ^ hash(self.key) ^ hash(self.data))

    def __cmp__(self, other):
        if self.__eq__(other):
            return 0
        elif self.__lt__(other):
            return -1
        else:
            return 1

    def __repr__(self):
        data_str = str(self.data)
        key_str = str(self.key)
        return "Missing Key: {0} => {1}" \
               .format(key_str, data_str)

    def __str__(self):
        return self.__repr__()