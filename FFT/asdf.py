class Number:
    def __init__(self, x: int) -> None:
        self.x = x
        self.minus = lambda y: self.x - y # we'll come back to this
    def plus(self, y: int) -> int:
        return self.x + y
one = Number(1)

Number.times = lambda self, y: self.x * y
print(one.times(2)) # automatically valid2