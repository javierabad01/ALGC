
import numpy as np
import random
from SyncRNG import SyncRNG

import seaborn as sb
import matplotlib.pyplot as plt
import sys
import copy
from queue import PriorityQueue
import time
sys.setrecursionlimit(20000)

"""
REALIZADO POR JAVIER ABAD HERNÁNDEZ
Estan todos los algoritmos incluidos, a seleccionar.
"""


class Nodo:
    def __init__(self, id):
        self.id = id
        self.next = []
        self.prev = []
        self.eliminado = False
        self.distancia_tentativa = sys.maxsize
        self.distancia_tentativa_destino = sys.maxsize

    def setVecino(self, nodo, peso):
        if nodo not in self.next:
            self.next.append([nodo, peso])
    
   



class Grafo:

    # Constructor
    def __init__(self):
        self.nodos = {}

    def main(self):

        print("Implementacion lab 4.3 y anteriores")
        print()

        filas = columnas = 150

        s = 5
        s2 = 10
        s3 = 45
        semilla = SyncRNG(seed=s)
        semilla2 = SyncRNG(seed=s2)
        semilla3 = SyncRNG(seed=s3)

        prob = 0.8
        self.generaLaberinto(filas, columnas, semilla, semilla2, prob)
        
        random.seed(semilla3)
        num_identificadores = 0
        for v in self.nodos:
            num_identificadores += 1

        origen_punto = semilla3.randi() % num_identificadores
        destino_punto = semilla3.randi() % num_identificadores

        print("origen:", origen_punto)
        print("destino:", destino_punto)

        # Eleccion algoritmo
        version = 0
        while (version != 1 and version != 2 and version != 3 and version != 4 and version != 5):
            version = int(input(
            "Escoge version: (1)Dijkstra basico (2)Dijkstra Fronteras (3)A* (4)Dijkstra Bidireccional (5)A* Bidireccional "))
        if version == 1:
            t0 = time.time()
            camino, preve = self.Dijkstra(origen_punto, destino_punto, num_identificadores)
            t1 = time.time()
            print("Tiempos Dijkstra Clasico:", t1-t0)
            print("Camino mas corto:", camino)

            m = self.traspasarGrafo(
                filas, columnas, preve, None, camino, origen_punto, destino_punto)
            plt.title("Dijkstra clásico", fontsize=16)

        elif version == 2:
            t0 = time.time()
            camino, preve = self.Dijkstra_Frontera(origen_punto, destino_punto)
            t1 = time.time()
            print("Tiempos Dijsktra Frontera:", t1-t0)
            print("Camino mas corto:", camino)
            print("Coste")
            print(self.nodos[camino[-1]].distancia_tentativa)

            m = self.traspasarGrafo(
                filas, columnas, preve, None, camino, origen_punto, destino_punto)
            plt.title("Dijkstra Frontera", fontsize=16)

        elif version == 3:
            t0 = time.time()
            optimo, camino_astar = self.ASTAR(origen_punto, destino_punto, columnas)
            t1 = time.time()
            print("Tiempos A*", t1-t0)
            print("Camino mas corto:", optimo)
            print("Coste")
            print(self.nodos[optimo[-1]].distancia_tentativa)

            m = self.traspasarGrafo(
                filas, columnas, camino_astar, None, optimo, origen_punto, destino_punto)
            plt.title("A*", fontsize=16)
        elif version == 4:
            t0 = time.time()
            optimo, camino1, camino2, distancia = self.Dijkstra_Bidireccional(origen_punto, destino_punto)
            t1 = time.time()
            print("Tiempo Dijkstra Bidireccional:", t1-t0)
            print("Camino mas corto", optimo)
            print("Valor total de la ruta: ", self.nodos[distancia].distancia_tentativa + self.nodos[distancia].distancia_tentativa_destino)
            plt.title("Dijsktra Bidireccional", fontsize=16)

            """
            Implementacion Dibujar laberintos mediante un mapa de calor
            """
            #Obtenemos la matriz de mapa de calor
            m = self.traspasarGrafo(filas, columnas, camino1, camino2, optimo, origen_punto, destino_punto)
        
        elif version == 5:
            t0 = time.time()
            optimo, camino1, camino2, distancia = self.ASTAR_Bidireccional(origen_punto, destino_punto, columnas)
            t1 = time.time()
            print("Tiempos A* Bidireccional", t1-t0)
            print("Camino mas corto:", optimo)
            print("Coste")

            m = self.traspasarGrafo(
                filas, columnas, camino1, camino2, optimo, origen_punto, destino_punto)
            plt.title("A* Bidireccional", fontsize=16)

        cmap = copy.copy(plt.get_cmap("hot"))
        cmap.set_under('gray')  
        cmap.set_bad('blue')

        sb.heatmap(m,vmin=0,cmap=cmap,cbar_kws={'extend': 'min', 'extendrect': True}, annot=False, fmt="", mask=(m==-1))

        plt.show()


    
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


    def generaLaberinto(self,filas, columnas, semilla, semilla2, pro):
        self.creaArray(filas, columnas)
        random.seed(semilla)

        #Utilizamos una segunda semilla y secuencia pseudoaleatoria para generar los pesos
        random.seed(semilla2)

        for i in range (filas):
            for j in range(columnas):
                if i > 0 and semilla.rand() < pro:
                    peso = int(random.randint(1,12))

                    self.nodos[int(self.ide(i,j))].setVecino((int(self.ide(i-1,j))),peso)
                    self.nodos[int(self.ide(i-1,j))].setVecino((int(self.ide(i,j))),peso)


                if j > 0 and semilla.rand() < pro:
                    peso = int(random.randint(1,12))


                    self.nodos[int(self.ide(i,j))].setVecino((int(self.ide(i,j-1))),peso)
                    self.nodos[int(self.ide(i,j-1))].setVecino((int(self.ide(i,j))),peso)

        
   

    def traspasarGrafo(self, filas, columnas, camino, camino_destino, camino_optimo, origen, destino):
        matriz = np.full((filas*2+1, columnas*2+1), -100, dtype=np.int64)

        for i in range(filas):
            for j in range(columnas):

                nodoActual = int(self.ide(i,j))
                if nodoActual in camino or (camino_destino != None and nodoActual in camino_destino):

                    if nodoActual in camino_optimo:
                        if nodoActual == origen or nodoActual == destino:
                            matriz[i*2+1][j*2+1] = 1000 #Origen y destino 
                        else:
                            matriz[i*2+1][j*2+1] = 800 #Resto de nodos que componen el camino mas corto
                    else:
                        if nodoActual in camino:
                            matriz[i*2+1][j*2+1] = self.nodos[nodoActual].distancia_tentativa
                        else: 
                            matriz[i*2+1][j*2+1] = self.nodos[nodoActual].distancia_tentativa_destino

                
                else:
                    matriz[i*2+1][j*2+1] = -1 #Habitacion que no se encuentra en el camino mas corto


                lista_vecinos = []
                for z in range(len(self.nodos[nodoActual].next)):
                    lista_vecinos.append(
                        self.nodos[nodoActual].next[z][0])
                
                if i < filas-1 and int(self.ide(i+1, j)) in lista_vecinos:

                    if nodoActual in camino_optimo and int(self.ide(i+1, j)) in camino_optimo:
                        matriz[i*2+2][j*2+1] = 800

                    else:

                        if int(self.ide(i+1,j)) in camino:

                            if self.nodos[nodoActual].distancia_tentativa < self.nodos[int(self.ide(i+1, j))].distancia_tentativa:
                                matriz[i*2+2][j*2+1] = self.nodos[nodoActual].distancia_tentativa 
                            else:
                                matriz[i*2+2][j*2+1] = self.nodos[int(self.ide(i+1,j))].distancia_tentativa                
                        elif camino_destino != None and int(self.ide(i+1, j)) in camino_destino:
                            #El pasillo tendra el valor de la distancia tentativa mas pequeña de las 2 habitaciones que une
                            if self.nodos[nodoActual].distancia_tentativa_destino < self.nodos[int(self.ide(i+1, j))].distancia_tentativa_destino:
                                matriz[i*2+2][j*2+1] = self.nodos[nodoActual].distancia_tentativa_destino
                            else:
                                matriz[i*2+2][j*2+1] = self.nodos[int(self.ide(i+1, j))].distancia_tentativa_destino
                        else:
                            matriz[i*2+2][j*2+1] = -1


                    

                
                if j < columnas-1 and int(self.ide( i, j+1)) in lista_vecinos: 

                    if nodoActual in camino_optimo and int(self.ide(i, j+1)) in camino_optimo:
                        matriz[i*2+1][j*2+2] = 800

                    else:

                        if int(self.ide(i,j+1)) in camino:
                            if self.nodos[nodoActual].distancia_tentativa < self.nodos[int(self.ide(i, j+1))].distancia_tentativa:
                                matriz[i*2+1][j*2+2] = self.nodos[nodoActual].distancia_tentativa 
                            else:
                                matriz[i*2+1][j*2+2] = self.nodos[int(self.ide(i,j+1))].distancia_tentativa                
                        elif camino_destino != None and int(self.ide(i, j+1)) in camino_destino:
                            #El pasillo tendra el valor de la distancia tentativa mas pequeña de las 2 habitaciones que une
                            if self.nodos[nodoActual].distancia_tentativa_destino < self.nodos[int(self.ide(i, j+1))].distancia_tentativa_destino:
                                matriz[i*2+1][j*2+2] = self.nodos[nodoActual].distancia_tentativa_destino
                            else:
                                matriz[i*2+1][j*2+2] = self.nodos[int(self.ide(i, j+1))].distancia_tentativa_destino

                        else:
                            matriz[i*2+1][j*2+2] = -1

        return matriz


    
    # obtenemos el nodo con la distancia tentativa menor (4.1)
    def distanciaMinima(self):
        minima = sys.maxsize
        nodo_elegidomin = None
        for nodo in self.nodos:
            if not self.nodos[nodo].eliminado and self.nodos[nodo].distancia_tentativa < minima:
                minima = self.nodos[nodo].distancia_tentativa
                nodo_elegidomin = nodo

        return nodo_elegidomin
    
    
    def Dijkstra(self, origen, destino, num_nodos):
        """
        Implementacion de Dijkstra (4.1)
        """
        prev = {origen:None}

        self.nodos[origen].distancia_tentativa = 0

        for i in range(num_nodos):
            u = self.distanciaMinima()
            if u == None:
                break
            self.nodos[u].eliminado = True
            if u == destino:
                S = []
                u = destino
                if prev[u] is not None or u == origen:
                    while u is not None:
                        S.insert(0, u)
                        u = prev[u]
                return S, prev

            for vecino in self.nodos[u].next:
                if not self.nodos[vecino[0]].eliminado:
                    nueva_distancia = self.nodos[u].distancia_tentativa+vecino[1]

                    if nueva_distancia < self.nodos[vecino[0]].distancia_tentativa:
                        self.nodos[vecino[0]].distancia_tentativa = nueva_distancia
                        prev[vecino[0]] = u

        return [], []


    def Dijkstra_Frontera(self, origen, destino):
        """
        Implementacion de Dijkstra Frontera (4.1)
        """
        nodo = origen
        self.nodos[origen].distancia_tentativa = 0
        cola_prioridad = PriorityQueue()
        cola_prioridad.put((0, nodo))
        eliminado = set()
        camino = {nodo: None}
        while not cola_prioridad.empty():
            a, nodo = cola_prioridad.get()
            if nodo == destino:
                S = []
                if camino[nodo] is not None or nodo == origen:
                    while nodo is not None:
                        S.insert(0, nodo)
                        nodo = camino[nodo]
                return S, camino

            eliminado.add(nodo)

            for vecino, peso in self.nodos[nodo].next:
                if vecino not in eliminado:
                    nueva_distancia = self.nodos[nodo].distancia_tentativa+peso
                    if nueva_distancia < self.nodos[vecino].distancia_tentativa:
                        cola_prioridad.put((nueva_distancia, vecino))
                        self.nodos[vecino].distancia_tentativa = nueva_distancia
                        camino[vecino] = nodo

   
    def Dijkstra_Bidireccional(self, origen, destino):
        """
        Implementacion de Dijkstra Bidireccional utilizando 2 colas de prioridades (4.3)
        """

        #Establecemos la distancia tentativa del origen y del destino a 0
        self.nodos[origen].distancia_tentativa = 0
        self.nodos[destino].distancia_tentativa_destino = 0
        

        frontera_origen = PriorityQueue()
        frontera_origen.put((0, origen)) #Contiene al principio solo el nodo origen

        frontera_destino = PriorityQueue()
        frontera_destino.put((0, destino)) #Contiene al principio solo el nodo destino
        
        #Utilizo un set en el que voy guardando los nodos explorados duarante la busqueda
        visitado = set()

        #Diccionarios en el que guardo los nodos y los padres de estos durante la busqueda
        solucion_delante = {origen: None}
        solucion_reverso = {destino: None}

        n = None

        while frontera_origen:
        
            if frontera_origen.empty() or frontera_destino.empty():
                return -1 #Return Fallo

            #Obtenemos los 2 nodos con mayor prioridad de cada cola
            a, node_origen = frontera_origen.get()
            a, node_destino = frontera_destino.get()


            #Condicion de Parada
            if self.nodos[node_origen].distancia_tentativa_destino != sys.maxsize:
                n = node_origen

            elif self.nodos[node_destino].distancia_tentativa != sys.maxsize:
                n = node_destino
        
            if n != None:
                print("Punto de interseccion:", n)
                nodo = n
                inter = n
                S1 = [] #Camino mas corto desde el origen hasta n
                S2 = [] #Camino mas corto desde n hasta el destino


                if solucion_delante[n] is not None or n == origen:
                    while n is not None:
                        S1.insert(0, n)
                        n = solucion_delante[n]


                if solucion_reverso[nodo] is not None or nodo == n:
                    while nodo is not None:
                        S2.insert(0, nodo)
                        nodo = solucion_reverso[nodo]


                S2 = S2[::-1] #Giramos la cadena para obtener el camino en el orden correcto
                S2.pop(0) #Eliminamos el primer elemento para que no aparezca 2 veces el nodo interseccion en el camino mas corto

                #Concatenamos las 2 listas para tener el camino optimo de ambas direcciones
                camino_corto = S1 + S2

                return camino_corto, solucion_delante, solucion_reverso, inter #Return Solucion

                
            visitado.add(node_origen)
            visitado.add(node_destino)

            #Visitamos los nodos de la primera lista --> forward
            for vecino, distancia in self.nodos[node_origen].next:
                if vecino not in visitado:

                    coste_anterior = self.nodos[vecino].distancia_tentativa
                    nuevo_coste = self.nodos[node_origen].distancia_tentativa + distancia

                    if nuevo_coste < coste_anterior:
                        frontera_origen.put((nuevo_coste, vecino))
                        self.nodos[vecino].distancia_tentativa = nuevo_coste
                        solucion_delante[vecino] = node_origen

                
            #Visitamos los nodos de la segunda lista --> backward
            for vecino, distancia in self.nodos[node_destino].next:
                if vecino not in visitado:

                    coste_anterior = self.nodos[vecino].distancia_tentativa_destino
                    nuevo_coste = self.nodos[node_destino].distancia_tentativa_destino + distancia

                    if nuevo_coste < coste_anterior:
                        frontera_destino.put((nuevo_coste, vecino))
                        self.nodos[vecino].distancia_tentativa_destino = nuevo_coste
                        solucion_reverso[vecino] = node_destino


 


    def dManhattan(self, nodo, destino, colum):
        """
        Funcion que implementa la heuristica: distancia de Manhattan (4.2)
        """

        #Obtenemos las coordenadas del nodo y del destino
        nodo_x = int(nodo/colum)
        nodo_y = int(nodo % colum)

        destino_x = int(destino/colum)
        destino_y = int(destino % colum)

        return (abs(nodo_x - destino_x) + abs(nodo_y - destino_y)) * 3 
        #Al multiplicar el valor de la heuristica por 2 o 3, reducimos las habitaciones
        #que tiene que hacer A* para llegar hasta el destino, por lo cual nos queda mas ovalada y dirigido hacia ese destino


    def ASTAR(self, origen, destino, colum):
        """
        Implementacion de A* (4.2)
        """
        node = origen
        self.nodos[origen].distancia_tentativa = 0 #Coste
        frontera = PriorityQueue()
        frontera.put((0, node)) #Contiene al principio solo el nodo origen  
        explorado = set() #Al utilizar set(), como se indica en wikipedia, obtengo un rendimiento mucho mejor
        solucion = {node: None} #Parent
        while not frontera.empty():
            a, node = frontera.get()
            if node == destino:
                S = [] #Lista en la que guardo el camino mas corto
                if solucion[node] is not None or node == origen:
                    while node is not None:
                        S.insert(0, node)
                        node = solucion[node]
                return S, solucion #Return Solucion
            explorado.add(node)
            for vecino, distancia in self.nodos[node].next:
                if vecino not in explorado:
                    coste_anterior = self.nodos[vecino].distancia_tentativa
                    nuevo_coste = self.nodos[node].distancia_tentativa + distancia
                    if nuevo_coste < coste_anterior:
                        #Establecemos la distancia tentativa del vecino 
                        self.nodos[vecino].distancia_tentativa = nuevo_coste
                        #Ahora guardamos en la cola, el nodo con el valor que toma de la funcion f(n) = d(n) + h(n), tomando como Heuristica la distancia de Manhattan
                        prioridad = nuevo_coste + self.dManhattan(vecino, destino, colum)
                        frontera.put((prioridad, vecino))
                        solucion[vecino] = node
    
    def ASTAR_Bidireccional(self, origen, destino, colum):
        """"
        Funcion que implementa la Busqueda A* Bidireccional utilizando 2 colas de prioridad (4.3)
        """

        self.nodos[origen].distancia_tentativa = 0
        self.nodos[destino].distancia_tentativa_destino = 0

        frontera_origen = PriorityQueue()
        frontera_origen.put((0, origen)) #Contiene al principio solo el nodo origen

        frontera_destino = PriorityQueue()
        frontera_destino.put((0, destino)) #Contiene al principio solo el nodo origen
        
        #Utilizo un set en el que voy guardando los nodos explorados duarante la busqueda
        explorado = set()

        #Diccionarios en el que guardo los nodos y los padres de estos durante la busqueda
        solucion_delante = {origen: None}
        solucion_reverso = {destino: None}

        n = None

        while not frontera_origen.empty():

            a, node_inicial = frontera_origen.get() #Obtenemos el nodo con mayor prioridad por el origen
            a, node_destino = frontera_destino.get() #Obtenemos el nodo con mayor prioridad por el destino


            if self.nodos[node_inicial].distancia_tentativa_destino != sys.maxsize:
                n = node_inicial

            elif self.nodos[node_destino].distancia_tentativa != sys.maxsize:
                n = node_destino

            if n != None:
                print("Punto de interseccion:", n)
                nodo = n
                inter = n
                S1 = [] #Camino mas corto desde el origen hasta n
                S2 = [] #Camino mas corto desde n hasta el destino


                if solucion_delante[n] is not None or n == origen:
                    while n is not None:
                        S1.insert(0, n)
                        n = solucion_delante[n]


                if solucion_reverso[nodo] is not None or nodo == n:
                    while nodo is not None:
                        S2.insert(0, nodo)
                        nodo = solucion_reverso[nodo]


                S2 = S2[::-1] #Giramos la cadena para obtener el camino en el orden correcto
                S2.pop(0) #Eliminamos el primer elemento para que no aparezca 2 veces el nodo interseccion en el camino mas corto

                #Concatenamos las 2 listas para tener el camino optimo de ambas direcciones
                camino_corto = S1 + S2

                return camino_corto, solucion_delante, solucion_reverso, inter #Return Solucion


            explorado.add(node_inicial)
            explorado.add(node_destino)


            for vecino, distancia in self.nodos[node_inicial].next:
                if vecino not in explorado:

                    coste_anterior = self.nodos[vecino].distancia_tentativa
                    nuevo_coste = self.nodos[node_inicial].distancia_tentativa + distancia

                    if nuevo_coste < coste_anterior:

                        #Establecemos la distancia tentativa del vecino 
                        self.nodos[vecino].distancia_tentativa = nuevo_coste

                        #Ahora guardamos en la cola, el nodo con el valor que toma de la funcion f(n) = d(n) + h(n), tomando como Heuristica la distancia de Manhattan
                        prioridad = nuevo_coste + self.dManhattan(vecino, destino, colum)
                        frontera_origen.put((prioridad, vecino))

                        solucion_delante[vecino] = node_inicial

            
            for vecino, distancia in self.nodos[node_destino].next:
                if vecino not in explorado:

                    coste_anterior = self.nodos[vecino].distancia_tentativa_destino
                    nuevo_coste = self.nodos[node_destino].distancia_tentativa_destino + distancia

                    if nuevo_coste < coste_anterior:

                        #Establecemos la distancia tentativa del vecino 
                        self.nodos[vecino].distancia_tentativa_destino = nuevo_coste

                        #Ahora guardamos en la cola, el nodo con el valor que toma de la funcion f(n) = d(n) + h(n), tomando como Heuristica la distancia de Manhattan
                        prioridad = nuevo_coste + self.dManhattan(vecino, origen, colum)
                        frontera_destino.put((prioridad, vecino))

                        solucion_reverso[vecino] = node_destino

    



if __name__ == "__main__":
    # Programa principal.
    principal = Grafo()
    principal.main()
