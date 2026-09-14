export function estatistica(lista) {
    let soma = 0

    for (let indice = 0; indice < lista.length; indice++) {
        soma += lista[indice]
    }

    console.log(`A média das notas é: ${soma / lista.length}`)

    lista.forEach((item) => {
        if(item >= 6) {
            console.log({"nota" : item, status: 'Aprovado'})
        } else {
            console.log({"nota" : item, status: 'Reprovado'})
        }
        
    })
}

const lista = [6,10,8,3]
estatistica(lista)
