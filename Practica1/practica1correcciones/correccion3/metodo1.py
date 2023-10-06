# Victor Mulero Merino
# METODO 1 - Incluir un umbral c para utilizar quicksort/insertion sort en funcion de la longitud del problema de entrada
import math
import random
import time
import matplotlib.pyplot as plt


# Clase Punto para representar los puntos
class Punto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.distancia = 0

    def calcular_distancia(self, p):
        self.distancia = math.sqrt((p[0] - self.x) ** 2 + (p[1] - self.y) ** 2)


def quicksort(A, punto_ref, c):
    # Calculamos la distancia de cada punto al punto de referencia
    for punto in A:
        punto.calcular_distancia(punto_ref)

    # Aplicamos el algoritmo
    quicksort_recursivo(A, 0, len(A) - 1, c)


def quicksort_recursivo(A, lo, hi, c):
    if lo >= hi or lo < 0:
        return

    p = particion(A, lo, hi)

    # p divide la lista en dos partes, aplicamos quicksort o insertion sort a cada una de las partes dependiendo de la longitud y del umbral c
    if len(A[lo:p]) <= c:
        A[lo:p] = insertion_sort(A[lo:p])
    else:
        quicksort_recursivo(A, lo, p - 1, c)

    if len(A[p + 1:hi + 1]) <= c:
        A[p + 1:hi + 1] = insertion_sort(A[p + 1:hi + 1])
    else:
        quicksort_recursivo(A, p + 1, hi, c)


def particion(A, lo, hi):
    pivot = A[hi]

    i = lo
    for j in range(lo, hi):
        if A[j].distancia <= pivot.distancia:
            A[i], A[j] = A[j], A[i]
            i += 1

    A[i], A[hi] = A[hi], A[i]

    return i


def insertion_sort(A):
    i = 1
    while i < len(A):
        x = A[i]

        j = i - 1
        while j >= 0 and A[j].distancia > x.distancia:
            A[j + 1] = A[j]
            j = j - 1

        A[j + 1] = x
        i = i + 1

    return A


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
quicksort(puntos, (0, 0), 50)
distancias = [p.distancia for p in puntos]
print(distancias == sorted(distancias))
# Se obtiene True

# Probamos diferentes tamaños de vector y umbral c
n = 1000
umbrales = range(0, 1000, 100)
tiempos = []

# Usamos el mismo conjunto de puntos para todos los umbrales
puntos = generar_puntos(n)

punto_ref = (0, 0)  # Punto de referencia
for c in umbrales:
    p = puntos.copy()
    t0 = time.time()
    quicksort(p, (0, 0), c)
    tiempos.append(time.time() - t0)

# Podemos ver los resultados graficamente
plt.figure(figsize=(5, 5))
plt.plot(umbrales, tiempos)
plt.title('Tiempo (segundos) en funcion del umbral (c)')
plt.show()

# Podemos hacer esas pruebas muchas veces y ver el umbral que mas veces es el del tiempo minimo
n = 1000
umbrales = range(0, 200, 10)
punto_ref = (0, 0)

umbrales_min = []
for _ in range(10):
    tiempos = []
    puntos = generar_puntos(n)

    for c in umbrales:
        p = puntos.copy()
        t0 = time.time()
        quicksort(p, (0, 0), c)
        tiempos.append(time.time() - t0)

    i_min = tiempos.index(min(tiempos))
    umbrales_min.append(umbrales[i_min])

print(f'Se han obtenido los umbrales: {umbrales_min}')

# Umbral que mejor ha funcionado:
mejor_umbral = max(set(umbrales_min), key=umbrales_min.count)
print(f'El mejor umbral es {mejor_umbral}')







