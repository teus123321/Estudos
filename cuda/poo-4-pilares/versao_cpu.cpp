#include <stdio.h>

// PRIMEIRO ESTUDE ESTE ARQUIVO: POO em C++ comum, sem termos do CUDA.
// Depois compare com personagens.cu e observe os marcadores __device__.

// ABSTRAÇÃO: define a ideia geral de um personagem.
class Personagem {
private:
    int poder; // ENCAPSULAMENTO: atributo privado.

public:
    // Construtor: recebe o valor e guarda no atributo poder.
    Personagem(int valor) {
        poder = valor;
    }

    // const: este método não modifica o objeto.
    int getPoder() const {
        return poder;
    }

    // virtual: permite que as classes filhas mudem o comportamento.
    // = 0: toda classe filha deve implementar este método.
    virtual int atacar() const = 0;

    // Destrutor da classe base (virtual por segurança com polimorfismo).
    virtual ~Personagem() {}
};

// HERANÇA: Guerreiro é um Personagem.
class Guerreiro : public Personagem {
public:
    // ": Personagem(valor)" chama o construtor da classe pai.
    Guerreiro(int valor) : Personagem(valor) {}

    // override: escreve a versão de atacar() do Guerreiro.
    int atacar() const override {
        return getPoder() * 2;
    }
};

// HERANÇA: Mago também é um Personagem.
class Mago : public Personagem {
public:
    // Também chama o construtor da classe pai.
    Mago(int valor) : Personagem(valor) {}

    int atacar() const override {
        return getPoder() + 10;
    }
};

// A mesma função funciona com Guerreiros ou Magos (polimorfismo).
// O & significa que a função recebe o objeto por referência.
int realizarAtaque(const Personagem &personagem) {
    return personagem.atacar();
}

int main() {
    const int quantidade = 6;
    int poderes[quantidade] = {5, 10, 15, 20, 25, 30};

    for (int i = 0; i < quantidade; i++) {
        if (i % 2 == 0) {
            Guerreiro guerreiro(poderes[i]);
            printf("Guerreiro | poder: %d | dano: %d\n", poderes[i], realizarAtaque(guerreiro));
        } else {
            Mago mago(poderes[i]);
            printf("Mago | poder: %d | dano: %d\n", poderes[i], realizarAtaque(mago));
        }
    }
    return 0;
}
