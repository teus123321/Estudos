# Aprendizado de máquina

## Primeira prática · Reconhecer dígitos

O [exercício em Python](classificar_digitos.py) usa imagens de dígitos manuscritos de 0 a 9 que já vêm com o scikit-learn. Cada imagem tem 8 × 8 pixels. O modelo recebe os 64 valores dos pixels e tenta prever o dígito.

Com um ambiente virtual ativo, execute nesta pasta:

```bash
python -m pip install scikit-learn
python classificar_digitos.py
```

## Para experimentar

1. Rode o exemplo e anote a acurácia. Ela mede a fração de imagens de teste em que o modelo acertou o dígito.
2. Na matriz de confusão, cada linha é o dígito real e cada coluna é o previsto. Procure o maior valor fora da diagonal. Quais dígitos o modelo mais confundiu?
3. Troque apenas `n_neighbors` de 3 para 5. Mantenha a divisão de dados fixa e compare os erros. Se for escolher o melhor valor de forma sistemática, faça essa escolha por validação dentro do conjunto de treino e reserve o teste para a avaliação final.

Para aproximar a prática do OCR de chassi e motor, registre a diferença entre acertar um caractere isolado e acertar uma sequência inteira.
