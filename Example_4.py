
def bar():
    pass

def boing():
    bar()
    if (4 + 4 == 3):
        ginkle()

def baz():
    boing()

def qux():
    boing()
 
def ginkle():
    pass

def foo():
    baz()
    qux()
