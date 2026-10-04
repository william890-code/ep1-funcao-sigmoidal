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

É necessário ter Python 3 instalado. A biblioteca Matplotlib é usada para exibir os gráficos.

Instale a dependência:

python -m pip install matplotlib.

Na pasta principal do repositório, execute:
python src/sigmoidal.py

## TABELA DE VALORES DE REFERÊNCIA

| x | Sigmoide logística |
|---:|---:|
| -5 | 0,00669285 |
| -2 | 0,11920292 |
| 0 | 0,50000000 |
| 2 | 0,88079708 |
| 5 | 0,99330715 |

Esses valores são da sigmoide logística calculada diretamente. A série de Taylor de grau 9 é uma aproximação centrada em zero; como \(x=\pm5\) está fora do seu raio de convergência \(|x|<\pi\), não use esses pontos para sugerir que o polinômio funciona bem ali.

## Exemplos de entrada e saída
O programa calcula a sigmoide logística e sua aproximação de Taylor de grau 9.

Exemplo de entrada real: x = 2

sigmoide(x) = 0.88079708
Taylor grau 9 = 0.88395062
erro absoluto = 3.154e-03

Exemplo de entrada complexa: z = 1 + 1j

sigmoide(z) = 0.78204157+0.20194823j
Taylor grau 9 = 0.78198854+0.20202822j
erro absoluto = 9.598e-05

- **Sigmoide logística: é a função que queremos calcular. Para números reais, transforma qualquer entrada em um resultado entre 0 e 1. Por exemplo, \(s(0)=0{,}5\).
- **Taylor de grau 9: é uma fórmula polinomial usada para aproximar a sigmoide. Ela inclui termos até \(x^9\). Perto de zero, costuma dar um valor muito próximo da função original; mais longe, pode ficar menos precisa.
- **Erro absoluto: mede a distância entre o resultado aproximado e o resultado da sigmoide:
\[
\text{erro} = |\text{sigmoide} - \text{Taylor}|.
\]
Quanto menor o erro, mais próxima está a aproximação. Se o erro for zero, os dois resultados coincidem naquele valor de entrada.

## Resultados

O tempo médio foi medido com 100.000 chamadas por rodada, repetindo a medição 5 vezes. Foi registrado o menor tempo por chamada. Os valores abaixo correspondem a uma execução e podem variar conforme o computador e os processos em execução.

| Implementação | Tempo médio por chamada |
|---|---:|
| Sigmoide logística | 277,3 ns |
| Taylor de grau 9 | 507,2 ns |

Nesta execução, a implementação logística foi mais rápida que o polinômio de Taylor. O gráfico de tempo de execução apresenta essa comparação.

<img width="682" height="493" alt="image" src="https://github.com/user-attachments/assets/15c0777d-4168-4a7b-9e4c-555cf006f4ee" />

## Apresentação
Link do vídeo no YouTube será adicionado aqui.
