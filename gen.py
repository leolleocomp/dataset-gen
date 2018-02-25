#!/bin/python
import math, random
from datetime import datetime, timedelta

# these lines show laziness
# todos os dados 'começam' aproximadamente aos 25 ºC
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

var = [
    'sys_temperature',
    'temperature',
    'tcf',
    'tsf',
    'umidity'
]

uuids = [
    '3db7224e-7304-46d5-bb9c-1b3f7d938077',
    '45f7f5c7-2745-439e-8405-98f1a1747ce5',
    '5f3de777-b6bb-4b32-9281-3524d9817a76',
    '6a775843-20e0-44af-87a7-3a4611ba934d',
    '771fb54e-f7ef-4563-891d-ebbc1e640e8c',
    '80a9ae0f-60e4-478a-984e-199f8c8f3382',
    '8abc1549-44e2-4e29-b661-1bbcac412bc1',
    'e72d4648-71b7-444f-9a86-b1ddcebefbe7'
]

dataset = [];

for i in range(len(uuids)):
    dataset.append({});
    dataset[i]['uuid'] = uuids[i]

    for v in var:
        dataset[i][v] = MockDataset() \
            .setPeriod(random.randrange(periodLower, periodUpper)) \
            .setScale(defaultScale) \
            .setYDelta(random.randrange(30)) \
            .setNoiseLimit(random.randrange(2,5)) \
            .setFunction(lambda t: math.exp(-0.001*t))

print("INSERT INTO readings VALUES ")
now = datetime.now() - timedelta(minutes=10080);

for i in range(len(dataset)):
    for t in range(0,10081, 5):

        currTime = now + timedelta(minutes=t)
        print('("' + dataset[i]['uuid'] + '", "' + currTime.isoformat() + '"', end="")

        for v in var:
            print(',' + str(dataset[i][v].at(t)), end="")

        print(")", end= "\n" if (i == len(dataset)-1 and t == 10080) else ",\n")
