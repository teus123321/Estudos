def imprimir_vetor(vetor) :
    for i in range(len(vetor)):
        print(vetor[i])

def merge(vetor, inicio, meio, fim) :
    fim1, fim2 = 0,0
    tamanho = fim-inicio + 1
    temp = [0] * tamanho
    p1 = inicio
    p2 = meio + 1
    for i in range(tamanho) :
        if not fim1 and not fim2:
            if vetor[p1] < vetor[p2] :
                temp[i] = vetor[p1]
                p1 += 1
            else :
                temp[i] = vetor[p2]
                p2 += 1
            if p1>meio :
                fim1 = 1
            if p2>fim :
                fim2 = 1

        else :
            if not fim1:
                temp[i] = vetor[p1]
                p1 += 1
            else :
                temp[i] = vetor[p2]
                p2 +=1
    for k in range(tamanho):
        vetor[inicio + k] = temp[k]


def mergeSort(vetor, inicio, fim):
    if(inicio < fim):
        meio = (inicio+fim) // 2
        mergeSort(vetor, inicio, meio)
        mergeSort(vetor, meio+1, fim)
        merge(vetor, inicio, meio, fim)


if __name__ == "__main__" :
    vetor = [2,5,6,7,2,4]
    n = 6
    imprimir_vetor(vetor)
    mergeSort(vetor, 0, n-1)
    print(vetor)
