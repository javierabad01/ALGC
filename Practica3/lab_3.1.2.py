import random
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import time
import sys
from SyncRNG import SyncRNG
sys.setrecursionlimit(10000)

#Tarea1: Laberinto y Grafo

class Nodo:
    #Constructor
    def __init__(self, i):
        self.id = i
        self.visitado = False
        self.vecinos = []

    def setVecino(self, n):
        if n not in self.vecinos:
            self.vecinos.append(n)

class Grafo: 
    #Constructor
    def __init__(self):
        self.nodos = {}
    
    def main(self):
        filas, columnas = 50,50
        semilla = SyncRNG(seed=30)
        pro = 0.6
        self.generaLaberinto(filas, columnas, semilla, pro)
        inicio = time.time()

        self.DFS(0)
        final = time.time()

        print("tiempo: ", str(final-inicio))

        m = self.traspasarGrafo(filas, columnas)

        sb.heatmap(m,cmap='inferno')
        plt.show()

    def creaArray(self,filas, columnas):
        id = 0
        self.array = np.full((filas, columnas),-100)
        for i in range(filas):
            for c in range(columnas):
                self.nodos[id] = Nodo(id) # tiene nodo y su id
                self.array[i][c] = id
                id += 1

    def DFS(self, nodo):
        
        self.nodos[nodo].visitado = True

        #vemos si los vecinos han sido visitados, de no serlo, se llama otra vez a dfs
        for n in self.nodos[nodo].vecinos:
            if not self.nodos[n].visitado:
                self.DFS(n) 

    
    def ide(self, fila, columna):
        return self.array[fila][columna]

    def generaLaberinto(self,filas, columnas, semilla, pro):
        self.creaArray(filas, columnas)
        random.seed(semilla)

        for i in range (filas):
            for j in range(columnas):
                if i > 0 and semilla.rand() < pro:
                    self.nodos[int(self.ide(i,j))].setVecino(int(self.ide(i-1,j)))
                    self.nodos[int(self.ide(i-1,j))].setVecino(int(self.ide(i,j)))


                if j > 0 and semilla.rand() < pro:
                    self.nodos[int(self.ide(i,j))].setVecino(int(self.ide(i,j-1)))
                    self.nodos[int(self.ide(i,j-1))].setVecino(int(self.ide(i,j)))



    def traspasarGrafo(self, filas, columnas):
        matriz = np.zeros((filas*2+1, columnas*2+1))
        for i in range(filas):
            for j in range(columnas):
                matriz[i*2+1][j*2+1] = 10

                if self.nodos[int(self.ide(i,j))].visitado == True:
                    matriz[i*2+1][j*2+1] = 20 

                lista_vecinos = self.nodos[int(self.ide(i,j))].vecinos
                
                if i < filas-1 and int(self.ide(i+1, j)) in lista_vecinos:
                    matriz[i*2+2][j*2+1] = 10
                    if self.nodos[ int(self.ide(i+1, j)) ].visitado == True:
                        matriz[i*2+2][j*2+1] = 20
                
                if j < columnas-1 and int(self.ide( i, j+1)) in lista_vecinos: 
                    matriz[i*2+1][j*2+2] = 10
                    if self.nodos[ int(self.ide(i,j+1)) ].visitado == True:
                        matriz[i*2+1][j*2+2] = 20

        return matriz



if __name__ == "__main__":
    main = Grafo()
    main.main()