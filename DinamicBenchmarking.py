import random
import copy
import timeit

mina = []
profundidad = None
ancho = None
memoize = None
content = "" #contenido del archivo
maxWeight = 0
weightsAndValues = []

def GenRandomMatrix(nrows,ncolumns,minval,maxval):
    mat = []
    for i in range(0,nrows):
        mat += [[]]
        for j in range(0,ncolumns):
            mat[i] += [random.randint(minval, maxval)]
    return mat

def GenRandomPairArray(ncolumns,minval1,maxval1,minval2,maxval2):
    arr1 = GenRandomMatrix(1,ncolumns,minval1,maxval1)
    arr2 = GenRandomMatrix(1,ncolumns,minval2,maxval2)
    arr = []
    for i in range(0,ncolumns):
        arr += [(arr1[i],arr2[i])]
    return arr

def KnapsackBruteForce(weightsAndValues, maxWeight):
    return KnapsackBruteForceAux(weightsAndValues, maxWeight, maxWeight,len(weightsAndValues)-1)

def KnapsackBruteForceAux(weightsAndValues, maxWeight, weight, item):
    if(weight < 0):
        return -1000
    if(weight == 0):
        return 0
    if(item == 0): 
        if (weightsAndValues[item][0] <= weight):
            return weightsAndValues[item][1]
        return 0
    return max(weightsAndValues[item][1] + KnapsackBruteForceAux(weightsAndValues, maxWeight, weight - weightsAndValues[item][0], item-1),KnapsackBruteForceAux(weightsAndValues, maxWeight, weight, item-1))

def knapSackDinamic(weightsAndValues, maxWeight):
    if maxWeight == 0 or len(weightsAndValues) == 0:
        return 0

    matrix = [[-1 for j in range(0,len(weightsAndValues))] for i in range(0,maxWeight + 1)]

    return knapSackDinamicAux(weightsAndValues, maxWeight, matrix, maxWeight, len(weightsAndValues)-1)

def knapSackDinamicAux(weightsAndValues, maxWeight, matrix, weight, item):
    if(weight < 0):
        return -1000
    if(weight == 0):
        return 0
    if(item == 0): 
        if (weightsAndValues[item][0] <= weight):
            return weightsAndValues[item][1]
        return 0
    if (matrix[weight][item] != -1):
        return matrix[weight][item]
    matrix[weight][item] = max(weightsAndValues[item][1] + knapSackDinamicAux(weightsAndValues, maxWeight, matrix, weight - weightsAndValues[item][0], item-1),knapSackDinamicAux(weightsAndValues, maxWeight, matrix, weight, item-1))

    return matrix[weight][item]


def leer_archivo(nombre_archivo):
    global mina
    global ancho
    global profundidad
    global memoize
    archivo = open(nombre_archivo, "r")
    contenido = archivo.read().splitlines()
    for linea in contenido:
        camino = linea.split(",")
        mina.append(camino)
    for i in range(0, len(mina)):
        for j in range(0, len(mina[0])):
            mina[i][j] = int(mina[i][j])
    profundidad = len(mina[0]) - 1
    ancho = len(mina)
    memoize = [[-1 for j in range(profundidad+1)] for i in range(ancho)]

def leer_archivo_mochila(nombre_archivo):
    global content
    global maxWeight
    global weightsAndValues

    archivo = open(nombre_archivo, "r")
    content = archivo.read().splitlines()
    maxWeight = int(content[0])
    lineaPesos = content[1].split(',')

    weightsAndValues = []
    for e in lineaPesos:
        peso = int(e)
        weightsAndValues += [(peso,0)]
    lineaBeneficios = content[2].split(',')
    for e in range(0,len(lineaBeneficios)):
        weightsAndValues[e] = (weightsAndValues[e][0],int(lineaBeneficios[e]))
    print(weightsAndValues)

def minaOroPD(fila, columna):
    if columna == profundidad:
        return mina[fila][columna]
    elif memoize[fila][columna] != -1:
        return memoize[fila][columna]
    else:
        if fila == 0:
            memoize[fila][columna] = mina[fila][
                columna] + max(minaOroPD(fila, columna + 1), minaOroPD(fila + 1, columna + 1))
        elif fila == (ancho - 1):
            memoize[fila][columna] = mina[fila][
                columna] + max(minaOroPD(fila - 1, columna + 1), minaOroPD(fila, columna + 1))
        else:
            memoize[fila][columna] = mina[fila][columna] + max(minaOroPD(fila - 1, columna + 1), max(
                minaOroPD(fila, columna + 1), minaOroPD(fila + 1, columna + 1)))
        return memoize[fila][columna]

def minaOroFB(fila, columna):
    if columna == profundidad:
        return mina[fila][columna]
    else:
        if fila == 0:
            mejor = mina[fila][
                columna] + max(minaOroFB(fila, columna + 1), minaOroFB(fila + 1, columna + 1))
        elif fila == (ancho - 1):
            mejor = mina[fila][
                columna] + max(minaOroFB(fila - 1, columna + 1), minaOroFB(fila, columna + 1))
        else:
            mejor = mina[fila][columna] + max(minaOroFB(fila - 1, columna + 1), max(
                minaOroFB(fila, columna + 1), minaOroFB(fila + 1, columna + 1)))
        return mejor


def main():
    start_time = timeit.default_timer()
    leer_archivo("ejemplo2.txt")
    camino = -1
    for i in range(0, ancho):
        aux = minaOroPD(i, 0)
        if aux > camino:
            camino = aux
    print(camino)

    leer_archivo_mochila("ejemplo.txt")
    print(KnapsackBruteForce(weightsAndValues, maxWeight))
    print(timeit.default_timer() - start_time)


main()