class hi():
    def __init__(self,name):
        self.name=name
    def sayhi(self):
        print("hi,",self.name)

 

alist = [hi("bram")]
bram = alist[0]
alist.remove(alist[0])

print(bram)