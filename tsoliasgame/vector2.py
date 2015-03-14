import math
def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def substract(a, b):
    return a[0] - b[0], a[1] - b[1]

def multiply(lamda, a):
    return lamda * a[0], lamda * a[1]

def get_length(x):
    return math.sqrt(x[0] * x[0] + x[1] * x[1])

def get_angle(x):
    return math.atan2(x[1], x[0])

def topolar(x):
    return get_length(x), get_angle(x)

def frompolar(x):
    return x[0] * math.cos(x[1]), -x[0] * math.sin(x[1])