import random
import time
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from SyncRNG import SyncRNG

def main():
    filas = 15
    columnas = 15
    semilla = SyncRNG(seed=5)
    pro = 0.5

    matrizAdyacencia, nodos = generaLaberinto(filas, columnas, semilla, pro)
    inicio = time.time()

    DFS(0, filas, columnas, matrizAdyacencia, [])
    final = time.time()

    print("tiempo: ", str(final-inicio))
    m = traspasarGrafo(filas, columnas, matrizAdyacencia, nodos)

    sb.heatmap(m,cmap='inferno')
    plt.show()


def creaArray(filas, columnas):
    id = 0
    array = np.zeros((filas, columnas))
   
    for i in range(filas):
        for c in range(columnas):
            array[i][c] = id
            id += 1        

    return array

def DFS(id, filas, columnas, matriz_adyacencia, lista):
    if(id not in lista):
        for i in range((filas*columnas)):
            if(matriz_adyacencia[id][i] == 1.0):
                lista.append(id)
                matriz_adyacencia[id][i] = 2.0
                DFS(i, filas, columnas, matriz_adyacencia, lista)
            matriz_adyacencia[id][id] = 2.0

def ide(matriz, f, c):
    return matriz[f][c]


def generaLaberinto(filas, columnas, semilla, pro):
    nodos = creaArray(filas, columnas)

    n = filas*columnas 
    matrizAdyacencia = np.zeros((n,n))

    random.seed(semilla)

    for i in range (filas):
        for j in range(columnas):
            if i > 0 and semilla.rand() < pro:
                matrizAdyacencia[int(nodos[i][j])][int(nodos[i-1][j])] = 1.0
                matrizAdyacencia[int(nodos[i-1][j])][int(nodos[i][j])] = 1.0
            if j > 0 and semilla.rand() < pro:
                matrizAdyacencia[int(nodos[i][j])][int(nodos[i][j-1])] = 1.0
                matrizAdyacencia[int(nodos[i][j-1])][int(nodos[i][j])] = 1.0

    return matrizAdyacencia, nodos


def traspasarGrafo(filas, columnas, matrizAdyacencia, nodos):
    #el 0 representa pared
    matriz = np.zeros((filas*2+1, columnas*2+1))

    for i in range(filas):
        for j in range(columnas):
            #marcamos habitacion sin recorrer con el 10 y recorrida con el 20
            matriz[i*2+1][j*2+1] = 10
            relacion = False
            if i < filas-1:
                if matrizAdyacencia[int(ide(nodos, i, j))][int(ide(nodos, i+1, j))] == 1.0:
                    matriz[i*2+2][j*2+1] = 10
                if matrizAdyacencia[int(ide(nodos, i, j))][int(ide(nodos, i+1, j))] == 2.0:
                    matriz[i*2+2][j*2+1] = 20
                    relacion = True

            if j < columnas-1:
                if matrizAdyacencia[int(ide(nodos, i, j))][int(ide(nodos, i, j+1))] == 1.0:
                    matriz[i*2+1][j*2+2] = 10
                if matrizAdyacencia[int(ide(nodos, i, j))][int(ide(nodos, i, j+1))] == 2.0:
                    matriz[i*2+1][j*2+2] = 20
                    relacion = True

            if(relacion):
                matriz[2*i+1][2*j+1] = 20
            if(matrizAdyacencia[i*columnas+j][i*columnas+j] == 2.0):
                matriz[2*i+1][2*j+1] = 20

    return matriz


if __name__ == "__main__":
    main()