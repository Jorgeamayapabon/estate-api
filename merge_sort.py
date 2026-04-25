def mergesort(lista):
    if len(lista) == 0:
        return lista
    elif len(lista) == 1:
        return [str(lista[0])]

    medio = len(lista) // 2
    izquierda = mergesort(lista[:medio])
    derecha = mergesort(lista[medio:])

    return merge(izquierda, derecha)


def merge(izq, der):
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):
        if izq[i] < der[j]:
            resultado.append(str(izq[i]))
            i += 1
        else:
            resultado.append(str(der[j]))
            j += 1

    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


def procesar_arreglo(arr):
    bloques = []
    actual = []

    for num in arr:
        if num == 0:
            bloques.append(actual)
            actual = []
        else:
            actual.append(num)

    # último bloque
    bloques.append(actual)

    resultado = []

    for bloque in bloques:
        if not bloque:
            resultado.append("X")
        else:
            ordenado = mergesort(bloque)
            resultado.append("".join(ordenado))

    return " ".join(resultado)


if __name__ == "__main__":
    list_input_1 = [3, 1, 2, 0, 9, 7, 0, 0, 5]
    print(procesar_arreglo(list_input_1))
    list_input_2 = [1, 3, 2, 0, 7, 8, 1, 3, 0, 6, 7, 1]
    print(procesar_arreglo(list_input_2))
    list_input_3 = [2, 1, 0, 0, 3, 4]
    print(procesar_arreglo(list_input_3))
