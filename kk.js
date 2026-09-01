import {Carro} from './main.js'

export class Honda extends Carro{
    constructor(marca, modelo, ano){
        super(marca,modelo)

        this.ano = ano
    }

    mostrar(){
        console.log(`Dados do seu veículo ${this.marca}, ${this.modelo}, ${this.ano}`)
    }
}

const myCar = new Honda("honda", "civic", 2020)
console.log(myCar.mostrar())