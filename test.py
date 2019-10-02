class Foo:
  num = -100
  def __init__(self, num, name):
    self.num = num
    self.name = name
    return

  def test1():
    print(123)
    return

  def test(self, a, b):
    print(self.name, self.num)
    return 

def test(a, b, c):
  print(a,b,c)

def test(a):
  print(a)



x=  { 1: 3, 2 : 4}
for key in x:
  print(x.get(key))
