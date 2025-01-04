import Parent_Example

class Fifth():
    
    def __init__(self):
        self.dad = Parent_Example.Parent_Example(5)
        pass
        
    def bar(self):
        return self.dad.speak()

    def boing(self):
        self.bar()
        if (4 + 4 == 3):
            self.ginkles()

    def baz(self):
        self.boing()

    def qux(self):
        self.boing()
    
    def ginkles(self):
        pass

    def foo(self):
        self.baz()
        self.qux()

jk = Fifth()

jk.bar()

jk.boing()

