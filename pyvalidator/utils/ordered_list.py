try:
    from hashable_dict import HashableDict
except:
    from .hashable_dict import HashableDict

class OrderedList(object):
    def __init__(self, *args):
        self.data = set()
        self.add(*args)

    def __eq__(self, other):
        return type(self)==type(other) and self.data==other.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def __repr__(self):
        return "OrderedList({0})".format(self.data)

    def add(self, *args):
        for i in args:
            if type(i) == dict:
                i = HashableDict(i)
            self.data.add(i)

    def append(self, *args):
        self.add(*args)

    def __compare_type__(self, item):
        return str(type(item))
