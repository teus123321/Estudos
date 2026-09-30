/*export function contadorVogais(frase) { 
    const vogais = ['a', 'e', 'i', 'o', 'u']

    let contador = 0

    for (let i = 0; i < frase.length; i++) {
        let letra = frase[i].toLowerCase()

        for (let j = 0; j < vogais.length; j++) {
            if (letra === vogais[j]) {
                contador++
                break
            }
        }
        
    }
    return contador
}

console.log(contadorVogais("Mateus"))*/

const contador = (name) => {
    const vogais = ['a', 'e', 'i', 'o', 'u'];
    const nome = name.split("");
    const aux = 0;
    nome.forEach(nome => {
        for (let i = 0; i<name.length; i++) {
            if (vogais[i] === nome){
                console.log("k")
            }
        }
    });
}
contador("Mateus");
