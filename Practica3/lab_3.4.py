import random
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
import copy
import sys
from SyncRNG import SyncRNG
sys.setrecursionlimit(10**6)


class Nodo:
   
    def __init__(self, i):
        
        self.id = i
        self.visitado = False
        self.vecinos = []
        self.profundidad = 0
        self.ciclo = []
        self.etiqueta = 0

    def setVecino(self, n): 
        if n not in self.vecinos:
            self.vecinos.append(n)

    def setCiclo(self, nodo):
        if nodo not in self.ciclo:
            self.ciclo.append(nodo)


class Grafo: 

    def __init__(self):
        self.nodos = {}

    def main(self):
        
        print("BUSQUEDA: ABAJO-DERECHA-IZQUIERDA-ARRIBA")
        print()

        filas, columnas = 15,15
        s = 5
        semilla = SyncRNG(seed=s)

        #Probabilidad entre 0 y 1
        pro = 0.5

        self.generaLaberinto(filas, columnas, semilla, pro)

        self.RecorridoDFS()
        self.DetectaCiclo()       
        #self.BFS(0,1)
        self.ComponentesConexas()
       
        matriz = np.full((filas*2+1, columnas*2+1), -100)
        numeros = self.traspasarGrafo(filas, columnas, matriz)

        cmap=copy.copy(plt.get_cmap("Paired_r"))
        cmap.set_under("blue")
        cmap.set_bad("green")

        anotar = np.vectorize(lambda x: '' if x <= 0 else str(round(x)))(numeros)        
        sb.heatmap(matriz,vmin=0,cmap=cmap,cbar_kws={'extend': 'min', 'extendrect': True}, annot=anotar, fmt="", mask=(matriz==100))
        plt.show()


    

    def DFS(self, nodo, profundidad):        
        self.nodos[nodo].visitado = True
        self.nodos[nodo].profundidad = profundidad

        for n in self.nodos[nodo].vecinos:
            if not self.nodos[n].visitado:
                self.DFS(n, profundidad+1) 

    def RecorridoDFS(self):
        for n in self.nodos:
            if not self.nodos[n].visitado:
                self.DFS(n, profundidad=1)


    def BusquedaCiclo(self, nodo, padre, visitados):
        visitados[nodo] = True

        for vecino in self.nodos[nodo].vecinos:
            if vecino != padre:
                if visitados[vecino] or self.BusquedaCiclo(vecino, nodo, visitados):
                    self.nodos[vecino].setCiclo(nodo)
        return False

    def DetectaCiclo(self):
        visitados = [False for v in self.nodos]

        for nodo in self.nodos:
            if self.nodos[nodo].visitado:
                if not visitados[nodo]:
                    self.BusquedaCiclo(nodo, None, visitados)

    def BFS(self, nodo, profundidad):
        if not self.nodos[nodo].visitado:
            cola = []
            cola.append(nodo)
            self.nodos[nodo].visitado = True
            self.nodos[nodo].profundidad = profundidad
 
            while cola: 
                nodo = cola.pop(0) 
                for n in self.nodos[nodo].vecinos:
                    if not self.nodos[n].visitado:
                        cola.append(n)
                        self.nodos[n].visitado = True
                        profundidad += 1
                        self.nodos[n].profundidad = profundidad


    def EtiquetandoComponentes(self, nodo, etiqueta, visitado):
    
        if visitado[nodo] == 0:
            visitado[nodo] = etiqueta
            self.nodos[nodo].etiqueta = etiqueta
            for vecino in self.nodos[nodo].vecinos:
                self.EtiquetandoComponentes(vecino, etiqueta, visitado)


    def ComponentesConexas(self):
        visitado = [0 for nodo in self.nodos]
        etiqueta = 0

        for nodo in self.nodos:
            if visitado[nodo] == 0:
                etiqueta += 1
                self.EtiquetandoComponentes(nodo, etiqueta, visitado)


    def creaArray(self,filas, columnas):
        id = 0
        self.array = np.full((filas, columnas),-100)
        for i in range(filas):
            for c in range(columnas):
                self.nodos[id] = Nodo(id) 
                self.array[i][c] = id
                id += 1


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

        for v in self.nodos:
            self.nodos[v].vecinos.reverse()

    
    def traspasarGrafo(self, filas, columnas, matriz):
        for i in range(filas):
            for j in range(columnas):
                nodoActual = int(self.ide(i,j))
                if self.nodos[nodoActual].visitado == True:
                    matriz[i*2+1][j*2+1] = self.nodos[nodoActual].etiqueta #guardamos el valor de la etiqueta del nodo
                else:
                    matriz[i*2+1][j*2+1] = 0 

                lista_vecinos = self.nodos[nodoActual].vecinos
                
                if i < filas-1 and int(self.ide(i+1, j)) in lista_vecinos:
                    if self.nodos[ int(self.ide(i+1, j)) ].visitado == True:
                        if int(self.ide(i+1, j)) in self.nodos[nodoActual].ciclo:
                            matriz[i*2+2][j*2+1] = -100 
                        else:
                            matriz[i*2+2][j*2+1] = self.nodos[int(self.ide(i,j))].etiqueta  #pasillo = la habitacion que sale
                    else:
                        matriz[i*2+2][j*2+1] = 0 

                else:  # NO SE HA RECORRIDO EL PASILLO, ES DECIR, NO HAY EJE, ESTO SIGNIFICA POSIBLE COSTURA.
                    if(i < (filas-1) and self.nodos[self.ide(i+1, j)].etiqueta != self.nodos[int(self.ide(i, j))].etiqueta):
                        matriz[i*2+2][j*2+1] = 100   

                
                if j < columnas-1 and int(self.ide( i, j+1)) in lista_vecinos: 
                    if self.nodos[ int(self.ide(i,j+1)) ].visitado == True:
                        if int(self.ide(i, j+1)) in self.nodos[nodoActual].ciclo:
                            matriz[i*2+1][j*2+2] = -100
                        else:
                            matriz[i*2+1][j*2+2] = self.nodos[int(self.ide(i,j))].etiqueta                
                    else:
                        matriz[i*2+1][j*2+2] = 0 
                else:  # NO SE HA RECORRIDO EL PASILLO, ES DECIR, NO HAY EJE, ESTO SIGNIFICA POSIBLE COSTURA.
                    if(j < (columnas-1) and self.nodos[int(self.ide(i, j+1))].etiqueta != self.nodos[self.ide(i, j)].etiqueta):
                        matriz[2*i+1][2*j+2] = 100

        return matriz


if __name__ == "__main__":
    main = Grafo()
    main.main()