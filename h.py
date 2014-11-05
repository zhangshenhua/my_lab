import math

def pdf(msg):
    d = dict()
    for c in msg:
        d[c] = d.get(c, 0) + 1
    return d


def h(msg):
    l = len(msg)
    return -sum([math.log(count/float(l),2) for count in pdf(msg).values() ])


def unittest():
    s = str(math.factorial(10000))
    print pdf(s)
    print h(s)

if __name__ == '__main__':
    unittest()
