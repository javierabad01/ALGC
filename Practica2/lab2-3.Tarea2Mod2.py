import sys
from numpy import random
import numpy as np
from pandas.core.frame import DataFrame
import seaborn as sb
import matplotlib.pyplot as plt
import math
import time

sys.setrecursionlimit(2000)


def main():
    n = 2000
    m = 2000
    t0=time.time()
    matriz=np.empty((n,m), float)
    crear_matriz(matriz)
    np.random.seed(0)
    t1=time.time()
    max_value = monte_carlo(matriz, n, m)
    t2 = time.time()
    print("Tiempo de inicializacion valores matriz:", t1-t0)
    print("Busqueda Monte-Carlo:", t2-t1)
    print("El valor maximo es: "+str(max_value))
    
def valorMatriz(x,y):
    return y + math.sin(math.pi * math.sqrt(x*x + y*y))
def f1(x,y): 
    return math.sin(x) + math.cos(y) + math.sin(x) * math.cos(y) + math.sin(x*2)
def f2(x,y):
    return 2 * math.sin(x) * math.cos(y/2) + x +  math.log(abs(y-math.pi/2))
def f3(x,y):
    return math.sin(x) * math.cos(y) + abs(math.sqrt(x*y))
def f4(x,y):
    return math.sin(x*7) + math.cos( (y+math.pi/4)*4 ) + (x+y)
def g(x,y):
    return math.cos((x*x+y*y)*12)/(2*((x*x+y*y)*3.14+1)) 
def h(x,y):
    return 2*(-math.sqrt(x*x+y*y)+(math.cos(y)+math.sin(x))*math.sin(y+x)) + 15*(math.sqrt((x+1)*(x+1)+y*y)-1)/((math.sqrt((x+1)*(x+1)+y*y)-1)*(math.sqrt(x*x+y*y)-1)+1)


def crear_matriz(matriz):
    for i in range(matriz.shape[0]): #[-1.5:2.5]
        x = -4 + i * 12 / (matriz.shape[0]-1)
        for j in range(matriz.shape[1]):
            y = 8 + j * -12  / (matriz.shape[1]-1)
            matriz[j][i] = h(x,y)
    return matriz


def monte_carlo(matriz, n, m):
        # MONTECARLO
    trayectoria_X = []
    trayectoria_Y = []
    coor_X = []
    coor_Y = []
    ya_esta = []
    max_value = -2147483648
    paracaidistas = 249

    for i in range(paracaidistas):
        numero = np.random.randint(n)
        coor_X.append(int(numero))

    for i in range(paracaidistas):
        numero = np.random.randint(m)
        coor_Y.append(int(numero))

    for i in range(paracaidistas):
        random_x = coor_X[i]
        random_y = coor_Y[i]
        punto_aleatorio = matriz[random_x][random_y]

        if [random_x,random_y] in ya_esta:
            pass
        else:
            ya_esta.append([random_x,random_y])

            trayectoria_X, trayectoria_Y = hill_climbingIterativo(matriz, random_x, random_y, punto_aleatorio, [random_x], [random_y])
            ultimo_x = trayectoria_X[len(trayectoria_X)-1]
            ultimo_y = trayectoria_Y[len(trayectoria_Y)-1]
        valor = matriz[ultimo_x][ultimo_y]
        if(valor > max_value):  # COMPARAMOS CON EL MAXIMO AL QUE HABIA LLEGADO EL MEJOR PARACAIDISTA
                max_value = valor
    return max_value




def hill_climbingRecursivo(matriz, x, y, punto, puntos_X, puntos_Y):
    
    array_colindantes = getColindantes(matriz, x, y)
    max_lista = np.max(list(array_colindantes.keys()))
    max_coor = array_colindantes[max_lista]

    if(punto < max_lista):
        puntos_X.append(max_coor[0])
        puntos_Y.append(max_coor[1])
        hill_climbingRecursivo(
            matriz, max_coor[0], max_coor[1], max_lista, puntos_X, puntos_Y)

    return puntos_X, puntos_Y

def hill_climbingIterativo(matriz, x, y, punto, puntos_X, puntos_Y):
    while(True):
        array_colindantes = getColindantes(matriz, x, y)
        max_lista = np.max(list(array_colindantes.keys()))
        max_coor = array_colindantes[max_lista]

        if(punto < max_lista):
            puntos_X.append(max_coor[0])
            puntos_Y.append(max_coor[1])
            x=max_coor[0]
            y=max_coor[1]
            punto=max_lista
        else:
            break
            
    return puntos_X, puntos_Y

    
def getColindantes(matriz ,x,y):
    dict = {}
    n = matriz.shape[0]
    m = matriz.shape[1]
    iterator = 0
    x_orig = x
    x -= 1

    while(iterator<2):
        if(0<=x<n):
            dict[matriz[x][y]] = [x,y]
        x += 2
        iterator += 1

    y -= 1
    iterator = 0
    while(iterator<2):
        if(0<=y<m):
            dict[matriz[x_orig][y]] = [x_orig,y]
        y += 2
        iterator += 1

    return dict


if __name__ == "__main__":
    # Programa principal.
    main()
