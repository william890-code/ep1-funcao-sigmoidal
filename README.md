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

## Propriedades da função

A sigmoide logística é definida por

\[
s(z) = \frac{1}{1 + e^{-z}}.
\]

Ela satisfaz as seguintes propriedades, desde que a função esteja definida:

- **Simetria:** \(s(-z) = 1 - s(z)\).
- **Derivada:** \(s'(z) = s(z)(1 - s(z))\).
- **Valor na origem:** \(s(0) = \frac{1}{2}\).

As propriedades foram verificadas numericamente para entradas reais e complexas. A derivada foi aproximada pela diferença central:

\[
s'(z) \approx \frac{s(z+h)-s(z-h)}{2h},
\qquad h=10^{-6}.
\]

### Resultados da verificação

| Entrada \(z\) | Erro da simetria | Erro da derivada |
|---|---:|---:|
| \(0{,}5\) | \(1{,}551\times10^{-17}\) | \(1{,}071\times10^{-11}\) |
| \(1+i\) | \(2{,}776\times10^{-17}\) | \(7{,}386\times10^{-11}\) |
| \(0{,}5+2i\) | \(3{,}331\times10^{-16}\) | \(1{,}439\times10^{-10}\) |

Os erros pequenos são compatíveis com arredondamentos numéricos e com a aproximação da derivada por diferença central.

## Testes com entradas complexas

A função e o polinômio de Taylor foram avaliados para as entradas abaixo. O erro é o módulo da diferença entre os resultados:

| Entrada \(z\) | Sigmoide logística | Taylor até grau 9 | Erro absoluto |
|---|---:|---:|---:|
| \(1+i\) | \(0{,}78204157+0{,}20194823i\) | \(0{,}78198854+0{,}20202822i\) | \(9{,}598\times10^{-5}\) |
| \(1-i\) | \(0{,}78204157-0{,}20194823i\) | \(0{,}78198854-0{,}20202822i\) | \(9{,}598\times10^{-5}\) |
| \(0{,}5+2i\) | \(0{,}86620562+0{,}63901905i\) | \(0{,}86496744+0{,}64842010i\) | \(9{,}482\times10^{-3}\) |

A série de Taylor é centrada em \(z=0\) e converge para \(|z|<\pi\). Embora os exemplos estejam dentro desse raio, o polinômio truncado no grau 9 pode apresentar erros maiores quanto mais distante a entrada estiver da origem.

## Como executar
Instruções de instalação e execução serão adicionadas aqui.

## Exemplos de entrada e saída
Serão adicionados após a implementação.

## Resultados
Tabelas e gráficos de erro e tempo de execução serão adicionados aqui.

## Apresentação
Link do vídeo no YouTube será adicionado aqui.
