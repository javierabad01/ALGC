import ast
from timeit import default_timer
import math
def quicksort(a, b, izquierda, derecha):
    while izquierda < derecha:
        indiceParticion = particion(a, b, izquierda, derecha)
        quicksort(a, b, izquierda, indiceParticion-1)
        izquierda = indiceParticion+1


def particion(a, b, izquierda, derecha):
    pivote = b[izquierda]
    while True:
        while b[izquierda] < pivote:
            izquierda += 1
        while b[derecha] > pivote:
            derecha -= 1

        if izquierda >= derecha:

            return derecha
        else:
 
            b[izquierda], b[derecha] = b[derecha], b[izquierda]
            a[izquierda], a[derecha] = a[derecha], a[izquierda]
           
            izquierda += 1
            derecha -= 1

#Programa Principal
puntorefc = input("Introduce el punto de referencia p(u,v): ")
listapuntosc = input("Introduce la lista de puntos: ")
puntoref = list(ast.literal_eval(puntorefc))
listapuntos = list(ast.literal_eval(listapuntosc))
#puntoref = (1,2)
x = puntoref[0]
y = puntoref[1]
listadistancias = []
#listapuntos = [(4,6),(5,3),(3,3),(7,9), (1,4),(2,2),(7,6),(8,2),(9,3)]
for i in range(len(listapuntos)):
    distancia = math.sqrt(pow(x -listapuntos[i][0],2)+pow(y - listapuntos[i][1],2))
    listadistancias.append(distancia)
t0 = default_timer()
quicksort(listapuntos, listadistancias, 0, len(listadistancias) - 1)
t1 = default_timer()
print("Después de ordenarlo: ")
print(listapuntos)
print("Tiempo de ejecución:", round(t1-t0, 5), "seg.")