class hi():
    def __init__(self,name):
        self.name=name
    def sayhi(self):
        print("hi,",self.name)

class hi1(hi):
    def __init__(self, name):
        super().__init__(name)
        self.lol = 'lol'


bram = hi1('bram')


print(type(bram) == hi1)