#!/bin/python
import math, random

# todos os dados 'começam' aproximadamente aos 25 min
NOISE_LIMIT = 5

defaultScale = 25
periodUpper = 500
periodLower = 300

def u(t):
    return 1 if (t >= 0) else 0

class MockDataset:
    def __init__(self):
        self.period = 1
        self.scale = 1
        self.yDelta = 0
        self.noiseLimit = 0
        self.function = lambda t: t

    def at(self, T):
        t = T -  math.floor(T / self.period) * self.period
        return random.randrange(self.noiseLimit) + self.yDelta + (u(t) - u(t - self.period)) * self.scale * self.function(t)

    def setPeriod(self, p):
        if (p >= 0):
            self.period = p

        return self

    def setScale(self, scale):
        if (scale > 0):
            self.scale = scale

        return self

    def setFunction(self, function):
        self.function = function

        return self

    def setYDelta(self, yDelta):
        self.yDelta = yDelta

        return self

    def setNoiseLimit(self, limit):
        self.noiseLimit = limit

        return self

    def __str__ (self):
        return "T="+str(self.period)+",Scl="+str(self.scale)

dataset = [
    MockDataset()
    .setPeriod(random.randrange(periodLower, periodUpper))
    .setScale(defaultScale)
    .setYDelta(random.randrange(30))
    .setNoiseLimit(random.randrange(2,5))
    .setFunction(lambda t: math.exp(-0.001*t))
    for i in range(10)
]

header = "t"

for j in range(len(dataset)):
    header += "," + str(j)

print(header)

for i in range(0,10080,5):
    strAcc = str(i)

    for j in range(len(dataset)):
        strAcc += "," + str(dataset[j].at(i))

    print(strAcc)

