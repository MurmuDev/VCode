import abc
from x import y
#This is a demo class

class A:
     x=''
     y=''

     def getx(self):
        method1('hello')
        return self.x

     def gety(self):
        return self.y

     def __init__(self,x, y):
        self.x = x
        self.y = y
        return x


def method1(x,y):
    return(y)

x  = 20
y = A(1,2)
z = A(3,4)
method1(x,y)
y.getx()
print(y)
