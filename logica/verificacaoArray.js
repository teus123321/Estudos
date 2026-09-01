arrayA = [1, 2, 3, 4, 5]; // Array A com elementos iniciais
arrayN = [5, 7, 8, 9, 10]; // Array N com elementos a serem adicionados

// Função para verificar se o array N está vazio e adicionar seus elementos ao array A
const verificarArray = (array) => {
    if (array.length > 0) {
        for (let i = 0; i < array.length; i++) {
            if (arrayA.includes(array[i])) {
                console.log(`O elemento ${array[i]} já existe no array A.`);
            } else {
                console.log(`O elemento ${array[i]} será adicionado ao array A.`);
                arrayA.push(array[i]);
            }
        }
        console.log("Elementos adicionados ao array A.");
        console.log("Array A atualizado:", arrayA);
    } else {
        console.log("O array está vazio.");
    }
};

// Chamada da função para verificar e adicionar elementos
verificarArray(arrayN);