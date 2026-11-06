export function palindromo(palavra) {
    let aux = []
    for (let i = 0; i < palavra.length; i++) {
        aux.push(palavra[i])
        if (palavra[i] !== palavra[palavra.length - 1 - i]) {
            return false
        } 
    }
    return true
}


console.log(palindromo("arara"))
console.log(palindromo("Mateus"))