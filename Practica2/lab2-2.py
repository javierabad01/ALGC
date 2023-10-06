from numpy import random
import numpy as np
from pandas.core.frame import DataFrame
import seaborn as sb
import matplotlib.pyplot as plt
import math

import time


def main():
    n = 100
    m = 100
    matriz = np.empty((n, m), float)
    generar_matriz(matriz)
    sb.heatmap(matriz, cmap="hot")
    
    inicio = time.time()
    
    fin = time.time()
    print(fin-inicio)

    

    intentos = 100

    np.random.seed(0)

    for z in range(intentos):

        # MONTECARLO
        trayectoria_X = []
        trayectoria_Y = []

        paracaidistas = 7

        
        for i in range(paracaidistas):
            random_x = random.randint(n)
            random_y = random.randint(m)
            punto_aleatorio = matriz[random_x][random_y]
            trayectoria_X, trayectoria_Y = hill_climbingIterativo(matriz, random_x, random_y, punto_aleatorio, [random_x], [random_y])
            
            primer_x = trayectoria_X[0]
            primer_yy = trayectoria_Y[0]
            ultimo_x = trayectoria_X[len(trayectoria_X)-1]
            ultimo_y = trayectoria_Y[len(trayectoria_Y)-1]
            primer_punto = {"x": [primer_x, primer_x + 0.0001], "y": [primer_yy, primer_yy+0.0001]}
            ultimo_punto = {"x": [ultimo_x+0.0001, ultimo_x], "y": [ultimo_y+0.0001, ultimo_y]}
            df1 = DataFrame(data=primer_punto)
            df2 = DataFrame(data=ultimo_punto)
            
            if(z == intentos-1):
                sb.lineplot(x=trayectoria_X, y=trayectoria_Y, color="black", linewidth=6, markersize=12, markers=True, estimator=None, palette="hls")
                sb.lineplot(x="x", y="y", data=df2, color="red", linewidth=6)
                sb.lineplot(x="x", y="y", data=df1, color="green", linewidth=6)
    plt.show()

def valorMatriz(x,y):
    return y + math.sin(math.pi * math.sqrt(x*x + y*y))
def f1(x,y): 
    return math.sin(x) + math.cos(y) + math.sin(x) * math.cos(y) + math.sin(x*2)
def f2(x,y):
    return 2 * math.sin(x) * math.cos(y/2) + x +  math.log(abs(y-math.pi/2))
def f3(x,y):
    return math.sin(x) * math.cos(y) + abs(math.sqrt(x*y))
def f4(x,y):
    return math.sin(x*7) + math.cos((y+math.pi/4)*4 ) + (x+y)
def g(x,y):
    return math.cos((x*x+y*y)*12)/(2*((x*x+y*y)*3.14+1)) 
def generar_matriz(matriz):
    for i in range(matriz.shape[0]): #[-1.5:2.5]
        x = i * math.pi / (matriz.shape[0]-1)
        for j in range(matriz.shape[1]):
            y = math.pi + j * (0 - math.pi) / (matriz.shape[1]-1)
            # matriz[j][i] = valorMatriz(x,y)
            # matriz[j][i] = f1(x,y)
            # matriz[j][i] = f2(x,y)
            # matriz[j][i] = f3(x,y)
            matriz[j][i] = f4(x,y)
    return matriz

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
