class C:
    def __init__(self):
        self._x = 5

    def set_x(self, x):
        self._x = x

class D():
    def __init__(self) -> None:
        self.y = C()
    
    def get_y(self): return self.y
    

temp = D()

temp.get_y().set_x(10)
print(temp.get_y()._x)






