export class Carro {
    constructor(marca, modelo){
        this.marca = marca
        this.modelo = modelo
    }

    marcaCarro(){
        console.log(`A marca desse carro é ${this.marca}`)
    }

    modeloCarro(){
        console.log(`O modelo desse carro é ${this.modelo}`)
    }
}

const carro = new Carro()
console.log(carro.marcaCarro)