class OrderedList(object):
    def __init__(self, *args):
        self.data = []
        for i in args:
            self.data.append(i)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        other.data.sort()
        self.data.sort()
        for i in range(len(self)):
            if other.data[i] != self.data[i]:
                return False
        return True

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        self.data.sort()
        return self.data[index]

    def __repr__(self):
        self.data.sort()
        return "OrderedList({0})".format(self.data)

    def add(self, *args):
        for i in args:
            self.data.append(i)

    def append(self, *args):
        self.add(*args)
