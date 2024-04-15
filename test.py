class C:
    def __init__(self):
        self._x = 5

    @property
    def x(self): return self._x
    @x.setter
    def x(self, value): raise Exception("Fuck off!!!")

class D(C):
    @C.x.setter
    def x(self, value): print("hi")


c = D()
c.x = 4343


x = "hi"
print(x is "hi")