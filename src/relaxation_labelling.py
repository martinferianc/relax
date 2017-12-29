import math
import numpy as np
import scipy
import tabulate

DEBUG = False

#Defines the compatibility coefficients
def r(a,b,C):
    res = C[int(a),int(b)]
    if DEBUG:
        print("Calculating r for a={} and b={} result ={}".format(a,b,res))
    return res

#Defines the small q for a single iteration
def q_s(A,          #The input probability matrix
        i,          #The i coordinate of the result
        j,          #The j cooridnate of the result
        i_n,        #The i coordinate of the neighbour
        j_n,        #The j coordinate of the neighbour
        label_i,    #The label which we wish to check
        C           #Defines the compatibility matrix
        ):
    res = r(label_i,True,C)*A[i_n,j_n] + r(label_i,False,C)*(1-A[i_n,j_n])
    if DEBUG:
        print("Calculating q_s for i={} and j={}, i_n={} and j_n={} result ={}".format(i,j,i_n,j_n,res))
    return res

#Defines the compatibility function
def C(i,       #The i coordinate of the result
      j,       #The j cooridnate of the result
      i_n,     #The i coordinate of the neighbour
      j_n      #The j coordinate of the neighbour
      ):
      distance = math.sqrt(math.pow(i-i_n,2) + math.pow(j-j_n,2))
      if DEBUG:
          print("Calculating compatibility for i={} and j={}, i_n={} and j_n={} result ={}".format(i,j,i_n,j_n,distance))
      return distance>0

#Calculate the big Q for a single point
def Q_s(A,      #The input matrix of probabilities
        i,      #The x index for which to calculate
        j,      #The y index for which to caclulate
        label_i,#The label for which to calculate Q
        Comp,    #The compatibility matrix
        shape  # Number of pixels put under consideration
        ):
        Q = 0
        x,y = A.shape
        center = shape // 2
        for i_n in range(i-center,i+center+1):
            for j_n in range(j-center,j+center+1):
                if i_n>=0 and j_n>=0 and i_n<x and j_n<y:
                    temp = C(i,j,i_n,j_n)*q_s(A,i,j,i_n,j_n,label_i,Comp)
                    if DEBUG:
                        print("Calculating Q for i={} and j={}, i_n={} and j_n={} result ={}".format(i,j,i_n,j_n,temp))
                    Q+=temp
        return Q

#Calculate the next proability at position i,j
def P_s_next(A, #The input matrix of probabilities
             i, #The x index for which to calculate
             j, #The y intex for which to caclulate
             C,  #The compatibility matrix
             shape # Number of pixels put under consideration
             ):
    temp = Q_s(A,i,j,True,C,shape)*A[i,j]
    res = temp / (temp+(1-A[i,j])*Q_s(A,i,j,False,C,shape))
    if DEBUG:
        print("Calculating P_s_next for i={} and j={}, result ={}".format(i,j,res))
    return res

def P(A,    #The input matrix of probabilities
      C,    #Compatibility matrix
      shape, #Shape of the region
      ):
    x = y = shape
    w,h = A.shape
    if x > w or y > h:
        raise Exception("Error: the size is larger than the input matrix!")
    new_P = np.array(A, copy=True)
    for i in range(w):
        for j in range(h):
            A[i,j] = P_s_next(new_P,i,j,C,shape)
    return A


def relax(A,             #The input matrix for which to solve
          C,             #The compatibility matrix
          iterations = 3, #The number of iterations
          shape = 3 # Shape of the region
          ):
    A = np.array(A)
    C = np.array(C)
    print("Solving: ")
    print(A)
    for i in range(iterations):
        if DEBUG:
            print("Iteration {}:".format(i+1))
            print(tabulate.tabulate(A, tablefmt="latex", floatfmt=".4f"))
        A = P(A,C,shape)
    print("Done!")
    print(A)
    return A
