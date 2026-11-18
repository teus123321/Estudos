# Os quatro pilares da POO em CUDA C++

Um exemplo simples com personagens de jogo: **Guerreiro** causa o dobro do poder como dano; **Mago** causa o poder mais 10 de dano. Cada personagem é calculado por uma *thread* da GPU.

## Arquivos

- [`personagens.cu`](personagens.cu): programa em CUDA C++ que executa seis personagens em paralelo na GPU.
- [`versao_cpu.cpp`](versao_cpu.cpp): mesma lógica de POO em C++ comum, para testar mesmo sem NVIDIA.

## Identificando os quatro pilares no código

| Pilar | Onde está? | O que significa neste exemplo? |
|---|---|---|
| **Encapsulamento** | `private: int poder` | O atributo fica protegido; consultamos seu valor pelo método `getPoder()`. |
| **Abstração** | `class Personagem` e `virtual int atacar() = 0` | A classe base define que todo personagem sabe atacar, sem escolher a fórmula. |
| **Herança** | `class Guerreiro : public Personagem` e `class Mago : public Personagem` | Guerreiro e Mago reaproveitam os dados e a interface de Personagem. |
| **Polimorfismo** | `realizarAtaque(const Personagem &personagem)` | A chamada `personagem.atacar()` usa a implementação de Guerreiro ou de Mago, conforme o objeto recebido. |

### O que é especial no CUDA?

- `__device__`: marca métodos e construtores que podem ser chamados pela GPU.
- `__global__`: marca a função `calcularDanos()`, iniciada pela CPU e executada na GPU.
- `<<<1, quantidade>>>`: inicia um bloco com seis *threads* (uma por personagem).
- `threadIdx.x` e `blockIdx.x`: ajudam cada *thread* a descobrir qual personagem processar.
- `cudaMallocManaged()`: aloca os arrays acessíveis pela CPU e GPU.
- `cudaDeviceSynchronize()`: espera a GPU terminar antes de imprimir os danos.

**Atenção:** os objetos `Guerreiro` e `Mago` são criados dentro da função executada na GPU. Isso é importante porque objetos com métodos `virtual` não devem ser construídos na CPU e depois copiados para a GPU.

## Como executar

### Com uma GPU NVIDIA e CUDA Toolkit instalado

No terminal, dentro desta pasta:

```bash
nvcc -std=c++17 personagens.cu -o personagens
./personagens
```

No Windows, após compilar, execute `personagens.exe` (ou `./personagens.exe` no PowerShell). O `nvcc` precisa estar instalado e configurado.

### Sem uma GPU NVIDIA

Você pode estudar primeiro a versão C++ comum:

```bash
g++ -std=c++17 versao_cpu.cpp -o versao_cpu
./versao_cpu
```

No Windows, execute `versao_cpu.exe` após compilar.

## Saída esperada (ambas as versões)

```text
Guerreiro | poder: 5 | dano: 10
Mago | poder: 10 | dano: 20
Guerreiro | poder: 15 | dano: 30
Mago | poder: 20 | dano: 30
Guerreiro | poder: 25 | dano: 50
Mago | poder: 30 | dano: 40
```

## Exercícios para praticar

1. Altere o dano do Mago para `getPoder() * 3`.
2. Crie uma classe `Arqueiro` que herda de `Personagem` e causa `getPoder() + 5` de dano.
3. Modifique o código para ter nove personagens, revezando Guerreiro, Mago e Arqueiro.

> **Observação:** o exemplo existe para ensinar POO e CUDA; ele não é uma tarefa que precise de GPU na prática. GPU faz mais sentido em problemas muito maiores, com mais cálculos paralelos.
