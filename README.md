# EP 1 — Cálculos Complexos com Séries de Taylor

## Tema
Função sigmoidal: y = sig(x)

## Integrantes
- Henry Sant Anna Meneses
- William Silva Guimaraes
- Bruno Oliveira Alves

## Objetivo
Implementar em Python o cálculo da função sigmoidal por meio de uma série de Taylor
e comparar a aproximação com valores de referência, analisando o erro e o tempo de execução.

## Função escolhida
A função escolhida é a sigmoide logística:
s(x) = 1 / (1 + e^(-x)).

## Série de Taylor em torno de x = 0

A função sigmoide logística é

s(x) = 1 / (1 + e^(-x)).

Ela satisfaz s'(x) = s(x)(1 - s(x)) e s(0) = 1/2.
Escrevendo s(x) = a_0 + a_1*x + a_2*x^2 + ..., os coeficientes
podem ser calculados pela recorrência:

(n + 1)*a_(n+1) = a_n - soma(a_k * a_(n-k), para k de 0 até n).

Os primeiros coeficientes são:
a_0 = 1/2, a_1 = 1/4, a_2 = 0, a_3 = -1/48, a_4 = 0,
a_5 = 1/480, a_6 = 0, a_7 = -17/80640, a_8 = 0,
a_9 = 31/1451520.

Logo, até o grau 9:

s(x) ≈ 1/2 + x/4 - x^3/48 + x^5/480
       - 17*x^7/80640 + 31*x^9/1451520.

A série centrada em zero converge para |x| < pi.
Por isso, essa aproximação não é adequada para x = 5 ou x = -5.

## Como executar
Instruções de instalação e execução serão adicionadas aqui.

## Exemplos de entrada e saída
Serão adicionados após a implementação.

## Resultados
Tabelas e gráficos de erro e tempo de execução serão adicionados aqui.

## Apresentação
Link do vídeo no YouTube será adicionado aqui.
