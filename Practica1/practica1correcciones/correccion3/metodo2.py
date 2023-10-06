# Victor Mulero Merino
# METODO 2 - Eliminar la recursion final de quicksort
import math
import time
import tracemalloc
import random
import matplotlib.pyplot as plt


# Clase Punto para representar los puntos
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.distancia = 0

    def calcular_distancia(self, p):
        self.distancia = math.sqrt((p[0] - self.x) ** 2 + (p[1] - self.y) ** 2)


def quicksort(A, punto_ref, usar_metodo_2=True):
    # Calculamos la distancia de cada punto al punto de referencia
    for punto in A:
        punto.calcular_distancia(punto_ref)

    if usar_metodo_2:
        quicksort_metodo_2(A, 0, len(A) - 1)
    else:
        quicksort_recursivo(A, 0, len(A) - 1)


def quicksort_metodo_2(A, lo, hi):
    if lo >= hi or lo < 0:
        return

    p = particion(A, lo, hi)

    # La primera parte del quicksort la mantenemos igual (con recursion)
    quicksort_metodo_2(A, lo, p - 1)

    # La segunda parte la transformamos a un proceso iterativo en lugar de recursivo
    # Necesitamos usar una pila
    pila = [(p, hi)]
    while pila:  # Mientras que la pila no este vacia
        a, b = pila.pop()

        i = a
        for j in range(a, b):
            if A[j].distancia < A[b].distancia:
                A[i], A[j] = A[j], A[i]
                i += 1

        A[i], A[b] = A[b], A[i]

        if i > a + 1:
            pila.append((a, i - 1))
        if i < b - 1:
            pila.append((i + 1, b))


def quicksort_recursivo(A, lo, hi):
    if lo >= hi or lo < 0:
        return

    p = particion(A, lo, hi)

    quicksort_recursivo(A, lo, p - 1)
    quicksort_recursivo(A, p + 1, hi)


def particion(A, lo, hi):
    pivot = A[hi]

    i = lo
    for j in range(lo, hi):
        if A[j].distancia <= pivot.distancia:
            A[i], A[j] = A[j], A[i]
            i += 1

    A[i], A[hi] = A[hi], A[i]

    return i


def generar_puntos(n):
    puntos = []
    for _ in range(n):
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        puntos.append(Punto(x, y))

    return puntos


# Comprobamos que la funcion que hemos creado ordena correctamente los puntos
# Generamos una lista de puntos y la ordenamos con quicksort()
# Comprobamos que las distancias esten ordenadas
puntos = generar_puntos(100)
quicksort(puntos, (0, 0))
distancias = [p.distancia for p in puntos]
print(distancias == sorted(distancias))
# Se obtiene True

# Comprobamos si hay diferencia en cuanto al rendimiento
n_puntos = (50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000)
tiempos_metodo_2 = []
tiempos_quicksort_recursivo = []
memoria_metodo_2 = []
memoria_quicksort_recursivo = []

for n in n_puntos:
    # Generamos los puntos
    puntos = generar_puntos(n)

    # Usamos los mismos puntos para ambos algoritmos
    p1 = puntos.copy()
    p2 = puntos.copy()
    punto_ref = (0, 0)  # Punto de referencia

    # Quicksort con la mezcla (recursivo e iterativo)
    t0 = time.time()
    tracemalloc.start()
    quicksort(p1, punto_ref)
    tiempos_metodo_2.append(time.time() - t0)
    memoria_metodo_2.append(tracemalloc.get_traced_memory()[1])
    tracemalloc.stop()

    # Quicksort recursivo
    t0 = time.time()
    tracemalloc.start()
    quicksort(p2, punto_ref, usar_metodo_2=False)
    tiempos_quicksort_recursivo.append(time.time() - t0)
    memoria_quicksort_recursivo.append(tracemalloc.get_traced_memory()[1])
    tracemalloc.stop()

# Podemos ver los resultados graficamente
plt.figure(figsize=(5, 5))
plt.title('Tiempo de ejecución (segundos) en funcion de n')
plt.plot(n_puntos, tiempos_metodo_2, label='Sin recursion final')
plt.plot(n_puntos, tiempos_quicksort_recursivo, label='Con recursion final')
plt.legend(loc='upper left', prop={'size': 12})
plt.show()

# Podemos ver los resultados graficamente
plt.figure(figsize=(5, 5))
plt.title('Memoria usada en funcion de n')
plt.plot(n_puntos, memoria_metodo_2, label='Sin recursion final')
plt.plot(n_puntos, memoria_quicksort_recursivo, label='Con recursion final')
plt.legend(loc='upper left', prop={'size': 12})
plt.show()

# No hay grandes diferencias en la eficiencia de ambos algoritmos
# Para n bajo los tiempos son muy similares
# Cuando el n aumenta, hay una ligera mejoria al usar el quicksort sin recursion final con respecto al recursivo