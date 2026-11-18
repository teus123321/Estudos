#include <stdio.h>

// Mesma ideia do exemplo CUDA, mas executada somente na CPU.
class Personagem {
private:
    int poder;

public:
    Personagem(int valor) : poder(valor) {}

    int getPoder() const {
        return poder;
    }

    virtual int atacar() const = 0;
    virtual ~Personagem() {}
};

class Guerreiro : public Personagem {
public:
    Guerreiro(int valor) : Personagem(valor) {}

    int atacar() const override {
        return getPoder() * 2;
    }
};

class Mago : public Personagem {
public:
    Mago(int valor) : Personagem(valor) {}

    int atacar() const override {
        return getPoder() + 10;
    }
};

// A mesma função funciona com Guerreiros ou Magos (polimorfismo).
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
