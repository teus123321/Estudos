# Os quatro pilares da POO em CUDA C++

Um exemplo simples com personagens de jogo: **Guerreiro** causa o dobro do poder como dano; **Mago** causa o poder mais 10 de dano. Cada personagem é calculado por uma *thread* da GPU.

## Arquivos

- [`personagens.cu`](personagens.cu): programa em CUDA C++ que executa seis personagens em paralelo na GPU.
- [`versao_cpu.cpp`](versao_cpu.cpp): mesma lógica de POO em C++ comum, para testar mesmo sem NVIDIA.

## 1. Primeiro entenda o C++, depois o CUDA

**Ordem recomendada:** leia [`versao_cpu.cpp`](versao_cpu.cpp) antes de [`personagens.cu`](personagens.cu). A classe, os objetos e os quatro pilares são conceitos de **C++**. O CUDA acrescenta marcadores para dizer que algumas funções serão executadas na **GPU**.

### O que significa cada palavra estranha?

| No código | Linguagem | Explicação simples |
|---|---|---|
| `class Personagem` | C++ | Cria um modelo para objetos chamados personagens. |
| `private:` | C++ | Tudo que vem depois fica escondido de código externo à classe. |
| `public:` | C++ | Tudo que vem depois pode ser usado por código externo. |
| `Personagem(int valor)` | C++ | **Construtor**: prepara o objeto quando ele é criado. |
| `getPoder()` | C++ | Método que devolve o poder guardado no objeto. |
| `const` após o método | C++ | Promete não modificar os atributos daquele objeto. |
| `virtual` | C++ | Permite escolher o método da classe filha quando chamado por meio da classe pai. |
| `= 0` depois de `virtual` | C++ | Faz o método ser **abstrato**: não tem implementação na classe pai. Não é uma atribuição de zero. |
| `override` | C++ | Confirma que a classe filha está substituindo um método virtual da classe pai. |
| `~Personagem()` | C++ | **Destrutor**, usado no fim da vida do objeto. Pode deixar esse detalhe para depois. |
| `__device__` | CUDA | Indica função, construtor ou método que pode ser chamado na GPU. |
| `__global__` | CUDA | Indica uma função iniciada pela CPU que será executada na GPU (kernel). |
| `threadIdx.x` | CUDA | Número da thread **dentro do bloco**, começando em zero. |
| `blockIdx.x` | CUDA | Número do bloco. Não é o número da placa de vídeo. |

### O que significa `__device__ virtual`?

Não é um único comando. São **duas informações diferentes** escritas juntas:

```cpp
__device__ virtual int atacar() const = 0;
```

- `__device__` = o método pertence ao código que roda na GPU.
- `virtual` = permite que `Guerreiro` e `Mago` tenham versões diferentes do método.
- `int` = o método devolve um número inteiro.
- `atacar()` = nome do método; os parênteses estão vazios porque ele não recebe argumentos.
- `const` = não altera o personagem.
- `= 0` = a classe pai só define a regra; cada filha precisa implementar o ataque.

> **Atenção:** `__device__` não é um **device ID**. O *device ID* identifica qual GPU utilizar num computador com uma ou mais GPUs. Já `threadIdx.x` identifica uma thread dentro de um bloco.

## 2. Entendendo os dois-pontos (`:`)

Os dois-pontos aparecem com significados diferentes no C++:

**A) `private:` e `public:`** são rótulos de acesso:

```cpp
private:
    int poder;
public:
    int getPoder() const;
```

**B) `: poder(valor)`** inicializa um atributo no construtor:

```cpp
Personagem(int valor) : poder(valor) {}
```

Nesse exemplo simples, é equivalente a escrever o construtor assim (como deixamos nos arquivos):

```cpp
Personagem(int valor) {
    poder = valor;
}
```

Se você criar `Personagem(10)`, o atributo `poder` recebe **10**. A primeira escrita é chamada de **lista de inicialização**: ela inicializa o atributo antes de executar o corpo `{}` do construtor.

**C) `: public Personagem`** indica herança:

```cpp
class Guerreiro : public Personagem {
    // Guerreiro é um tipo de Personagem.
};
```

**D) `: Personagem(valor)`** no construtor do Guerreiro chama o construtor do pai:

```cpp
Guerreiro(int valor) : Personagem(valor) {}
```

Isso quer dizer: "antes de terminar de criar o Guerreiro, crie a parte `Personagem` dele usando `valor`". É por isso que o Guerreiro já tem um poder guardado, mesmo que o atributo pertença à classe pai.

## 3. Como a GPU usa essas classes?

1. A CPU coloca seis valores no array `poderes`.
2. `calcularDanos<<<1, 6>>>(...)` inicia **um bloco** com **seis threads** na GPU.
3. Cada thread calcula seu índice `i` e pega `poderes[i]`.
4. Se `i` é par, cria um `Guerreiro`; se `i` é ímpar, cria um `Mago`.
5. `realizarAtaque()` recebe esse objeto como `Personagem&` e chama o método `atacar()` da classe correta (**polimorfismo**).
6. Cada thread escreve um resultado em `danos[i]`; depois a CPU imprime os seis valores.

Se estiver estudando **somente POO**, ignore por enquanto `cudaMallocManaged`, `<<< >>>` e os índices das threads. Entenda primeiro `class`, `private`, `public`, construtores, `virtual`, `override` e `: Personagem(valor)`.

## 4. Identificando os quatro pilares no código

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

## 5. Como executar

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

## 6. Saída esperada (ambas as versões)

```text
Guerreiro | poder: 5 | dano: 10
Mago | poder: 10 | dano: 20
Guerreiro | poder: 15 | dano: 30
Mago | poder: 20 | dano: 30
Guerreiro | poder: 25 | dano: 50
Mago | poder: 30 | dano: 40
```

## 7. Exercícios para praticar

1. Altere o dano do Mago para `getPoder() * 3`.
2. Crie uma classe `Arqueiro` que herda de `Personagem` e causa `getPoder() + 5` de dano.
3. Modifique o código para ter nove personagens, revezando Guerreiro, Mago e Arqueiro.

> **Observação:** o exemplo existe para ensinar POO e CUDA; ele não é uma tarefa que precise de GPU na prática. GPU faz mais sentido em problemas muito maiores, com mais cálculos paralelos.
