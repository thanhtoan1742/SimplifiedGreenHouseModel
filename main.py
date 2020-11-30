# x' = f(x, t) = a(x, t) + b(x, t)
# a(x, t) = x*t
# b(x, t) = x + t

class dxGen:
    def __init__(x = 0, t = 0, c):
        self.x = x
        self.t = t
        self.c = c

    def f():
        return self.a() + self.b()

    def a():
        return self.x * self.t + self.c

    def b():
        return self.x + self.t

    def call(x, t):
        self.x = x
        self.t = t

        return f()

def rk4(dx, t, x0):
    return dx.call(x0, t)


dx = dxGen(0, 0, 10)
dx.call(x, t)


rk4(dx, 0, 0)  

