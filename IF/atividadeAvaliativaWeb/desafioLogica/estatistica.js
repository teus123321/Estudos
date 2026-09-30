/*export function estatistica(lista) {
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
*/

const estatistica = (lista) => {
    let aux = 0
    lista.forEach((lista,index) => {
        if (lista < 0) {
            console.log(`Inválido ${lista}`)
        }
        else if (lista < 6) {
            console.log(`O aluno com essa nota foi reprovado ${lista}`)
        } else {
            console.log(`O aluno com essa nota foi aprovado ${lista}`)
        }
        aux += lista
    });
    console.log(aux / lista.length)
}

estatistica([1,2,8,4])