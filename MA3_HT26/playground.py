import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def montec(n):
    xlist = []
    ylist = []
    for i in range(n):
        xlist.append(random.uniform(-1, 1))
        ylist.append(random.uniform(-1, 1))
    coord = list(zip(xlist, ylist))
    ins = [tup for tup in coord if m.sqrt(tup[0]**2 + tup[1]**2) <= 1]
    outs = [tup for tup in coord if m.sqrt(tup[0]**2 + tup[1]**2) > 1]


    fig, ax = plt.subplots()
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    if ins:
        ax.scatter(*zip(*ins), color='green', s=10)
    if outs:
        ax.scatter(*zip(*outs), color="red", s=10)

    fig.savefig(f"montecarlo_{n}.png")
    plt.show()
    plt.close(fig)
    return print(n, 4*len(ins)/(len(coord)))

def spunkt(d):
    return [random.uniform(-1, 1) for _ in range(d)]

def kvadrera(x):
    return x * x

def summa(p):
    return sum(map(kvadrera, p))

def insidefilter(s):
    if s <= 1:
        return True
    else:
        return False


def hsphere(n, d):
    slumppunkter = [spunkt(d) for _ in range(n)]
    avstånd = map(summa, slumppunkter)
    inne = list(filter(insidefilter, avstånd))
    return 2**d*len(inne)/n
        
    


