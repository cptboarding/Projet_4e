

def func(arg1: int, arg2: "MyObject"):
    pass


class MyObject:
    def __init__(self):
        self.some_var = 1

class Adrien:
    pass

c = MyObject()
a = Adrien()

func(1, a)