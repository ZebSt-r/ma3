""" MA3.py

Student: Zeb Strömberg
Mail:
Reviewed by:
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from numba import njit
from statistics import mean 
from time import perf_counter as pc



# Exc1
def approximate_pi(n):
    # n is the number of points
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
    plt.close(fig)
    print(n)
    return (4*len(ins)/(len(coord)))
    # Write your code here
    

# Exc2, approximation
def sphere_volume(n, d): 
    # n is the number of points
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
    # d is the number of dimensions of the sphere 

    slumppunkter = [spunkt(d) for _ in range(n)]
    avstand = map(summa, slumppunkter)
    inne = list(filter(insidefilter, avstand))
    return 2**d*len(inne)/n
    

#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points
    return (m.pi**(d/2))/(m.gamma((d/2)+1))
    # d is the number of dimensions of the sphere 

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float:
    # n is the number of points
    # d is the number of dimensions of the sphere
    inne = 0
    for _ in range(n):
        summan = 0.0
        for _ in range(d):
            x = random.uniform(-1, 1)
            summan += x*x
        if summan <= 1:
            inne +=1

    #np is the number of processes
    return 2.0**d*inne/n

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np=4):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    #fungerar bara om n är delbart med np
    ppp = [n//np for i in range(np)]
    with future.ProcessPoolExecutor(max_workers=np) as x:
        delvolymer = list(x.map(sphere_volume, ppp, [d]*np))
    return mean(delvolymer)
    
def main():
    # Exc1
    # Exc2
    n = 100000
    d = 2
    print(sphere_volume(n, d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    print(sphere_volume(n, d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start}")
    print("What is numba time?")

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

#def main():
    #for n in [1000, 10000, 100000]:
        #approximate_pi(n)

if __name__ == '__main__':
	main()

