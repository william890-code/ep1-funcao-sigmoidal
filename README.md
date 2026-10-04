# Função Sigmoide — Série de Taylor, Aproximações e Propriedades

**Tema:** `y = sig(x) = 1 / (1 + e^(-x))` (função sigmoide / logística)

**Integrantes do grupo:**
- Henry Sant Anna Meneses
- Bruno Oliveira Alves
- William Silva Guimaraes

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `sigmoid_taylor.py` | Derivadas manuais, coeficientes de Taylor e função otimizada |
| `experimentos.py` | Polinômios das derivadas, escolha de N, tabela de valores |
| `erro_vs_tempo.py` | Erro × tempo de execução e tabela final |
| `main.py` | Programa de entrada/saída (`python main.py 0.7`) |
| `plots.py` | Gráficos com matplotlib (seção 5) |
| `grafico_1_taylor_vs_exata.png` ... `grafico_4_erro_vs_tempo.png` | Gráficos gerados pelo `plots.py` |

## Instalação e execução

Requer **Python 3.8+**. Os cálculos (derivadas, Taylor, benchmark) usam só a biblioteca padrão (`math`, `fractions`, `time`), sem NumPy nem SymPy. Apenas os **gráficos** precisam de uma biblioteca extra:

```bash
pip install matplotlib
```

Se der erro de "pip não encontrado", use `python -m pip install matplotlib`.

```bash
python experimentos.py      # derivadas, coeficientes, erro por N, tabela
python erro_vs_tempo.py     # erro x tempo
python main.py 0.7 -4 2.5   # entrada: valores de x
python plots.py             # gráficos (salva PNGs e abre as janelas)
python plots.py --no-show   # só salva os PNGs, sem abrir janelas
```

**Exemplo de input / output:**

```
$ python main.py 0.7 -4
x=0.7      taylor=0.6681877701 exata=0.6681877722 erro=2.02e-09
x=-4.0     taylor=0.0179862100 exata=0.0179862100 erro=0.00e+00
```

---

## 1. Cálculo de Taylor para a função

### 1.1 Derivadas (feitas manualmente)

Seja `s = sig(x)`. Como `e^-x = (1-s)/s`, temos

```
sig'(x) = e^-x / (1+e^-x)^2 = s(1 - s)
```

Pela regra da cadeia, se `sig^(n)(x) = P_n(s)`, então

```
P_(n+1)(s) = P_n'(s) · s(1 - s)
```

Resultado (conferido em `experimentos.py`):

| n | sig^(n)(x) em função de s | valor em x = 0 (s = 1/2) |
|---|---|---|
| 0 | s | 1/2 |
| 1 | s − s² | 1/4 |
| 2 | s − 3s² + 2s³ | 0 |
| 3 | s − 7s² + 12s³ − 6s⁴ | −1/8 |
| 4 | s − 15s² + 50s³ − 60s⁴ + 24s⁵ | 0 |
| 5 | s − 31s² + 180s³ − 390s⁴ + 360s⁵ − 120s⁶ | 1/4 |
| 6 | s − 63s² + 602s³ − 2100s⁴ + 3360s⁵ − 2520s⁶ + 720s⁷ | 0 |

Os coeficientes `c_n = sig^(n)(0)/n!` são:

```
sig(x) = 1/2 + x/4 − x³/48 + x⁵/480 − 17x⁷/80640 + 31x⁹/1451520 − 691x¹¹/319334400 + ...
```

Observação: `sig(x) − 1/2` é **função ímpar**, por isso todas as derivadas pares (n ≥ 2) valem 0 em x = 0. Só os termos ímpares existem.

### 1.2 Qual o valor de N? Por quê?

**Escolhemos N = 11, com Taylor usada apenas em |x| ≤ 1.**

Motivos:

1. **Raio de convergência = π.** Os polos de `1/(1+e^-x)` estão em `x = ±iπ` (onde `e^-x = −1`). Fora de |x| < π a série **diverge**, e perto de π converge muito devagar. Isso aparece na tabela: com N = 9, `x = 3` tem erro 0,2 e `x = 4` tem erro 3,5.
2. **Erro por N e intervalo** (erro máximo absoluto, medido contra `1/(1+e^-x)`):

| N | X = 0,5 | X = 1 | X = 2 | X = 3 |
|---|---|---|---|---|
| 1 | 2,5e-03 | 1,9e-02 | 1,2e-01 | 3,0e-01 |
| 3 | 6,4e-05 | 1,9e-03 | 4,8e-02 | 2,7e-01 |
| 5 | 1,6e-06 | 1,9e-04 | 1,9e-02 | 2,4e-01 |
| 7 | 4,1e-08 | 1,9e-05 | 7,8e-03 | 2,2e-01 |
| 9 | 1,0e-09 | 2,0e-06 | 3,2e-03 | 2,0e-01 |
| **11** | 2,6e-11 | **2,0e-07** | 1,3e-03 | 1,8e-01 |
| 13 | 6,6e-13 | 2,0e-08 | 5,2e-04 | 1,7e-01 |
| 15 | 1,7e-14 | 2,0e-09 | 2,1e-04 | 1,5e-01 |

3. **Custo × precisão.** Cada +2 em N reduz o erro em ~10× em [−1, 1] e custa ~0,02 µs a mais. N = 11 dá erro < 2,1e-7 (precisão de `float32`, ~7 dígitos). Passar disso exigiria N grande demais fora de |x| ≤ 1 (em X = 2, N = 21 ainda dá 1,4e-05), então é mais barato **trocar o método** fora do intervalo.
4. **Fora de |x| ≤ 1** usamos a forma fechada com `exp`, que é exata e estável.

### 1.3 Código da função otimizada

Está em `sigmoid_taylor.py` (`make_taylor_sigmoid` e `make_hybrid_sigmoid`). Otimizações:

- **Só termos ímpares**: metade dos coeficientes (os pares são zero).
- **Horner em u = x²**: `sig ≈ 1/2 + x·(c1 + u(c3 + u(c5 + ...)))`, sem `pow`, só ~N/2 multiplicações e somas.
- **Coeficientes pré-calculados** em `Fraction` (exatos) e convertidos a `float` uma única vez.
- **Simetria** `sig(−x) = 1 − sig(x)`: o polinômio ímpar já a respeita automaticamente.
- **Estabilidade fora do intervalo**: para x < 0 usa `e^x/(1+e^x)`, evitando overflow de `exp(-x)`.

```python
def sig_n(x):          # N = 11  ->  c1, c3, c5, c7, c9, c11
    u = x * x
    acc = head
    for a in tail:
        acc = acc * u + a
    return 0.5 + x * acc
```

Ganho medido: a versão ingênua (`sum(c[k]*x**k)`, N = 9) leva **1,24 µs**; a otimizada (N = 9) leva **0,18 µs**, ou seja ~**7× mais rápida**.

---

## 2. Aproximações e propriedades da função

**Propriedades:**

- Domínio ℝ, imagem (0, 1), estritamente crescente.
- `sig(0) = 1/2`; `lim x→+∞ = 1`, `lim x→−∞ = 0` (assíntotas horizontais).
- **Simetria:** `sig(−x) = 1 − sig(x)`, logo `sig(x) − 1/2` é ímpar.
- **Derivada:** `sig' = sig(1 − sig)`, máxima em x = 0 com valor 1/4 e sempre positiva.
- **Relação com tanh:** `sig(x) = 1/2 + (1/2)·tanh(x/2)`.
- **Inversa (logit):** `sig⁻¹(y) = ln(y/(1−y))`.
- **Ponto de inflexão** em x = 0 (`sig'' = 0`; muda de convexa para côncava).
- **Raio de convergência da série de Taylor:** π.

**Aproximações:**

| Região | Aproximação | Observação |
|---|---|---|
| x ≈ 0 | `1/2 + x/4` (N = 1) | erro 1,9e-02 em [−1, 1] |
| \|x\| ≤ 1 | Taylor N = 11 | erro < 2,1e-7 |
| x grande | `1 − e^-x` | erro ≈ e^(−2x) |
| x muito negativo | `e^x` | erro ≈ e^(2x) |
| \|x\| > ~37 | 0 ou 1 | satura em `float64` |

---

## 3. Tabela de valores fixos

Função híbrida (Taylor N = 11 em |x| ≤ 1, forma exata fora):

| x | sig(x) exata | Aproximação | Erro absoluto |
|---|---|---|---|
| −10 | 0,0000453979 | 0,0000453979 | 0 |
| −6 | 0,0024726232 | 0,0024726232 | 0 |
| −4 | 0,0179862100 | 0,0179862100 | 0 |
| −3 | 0,0474258732 | 0,0474258732 | 0 |
| −2 | 0,1192029220 | 0,1192029220 | 0 |
| −1 | 0,2689414214 | 0,2689416204 | 2,0e-07 |
| −0,5 | 0,3775406688 | 0,3775406688 | 2,6e-11 |
| 0 | 0,5000000000 | 0,5000000000 | 0 |
| 0,5 | 0,6224593312 | 0,6224593312 | 2,6e-11 |
| 1 | 0,7310585786 | 0,7310583796 | 2,0e-07 |
| 2 | 0,8807970780 | 0,8807970780 | 0 |
| 3 | 0,9525741268 | 0,9525741268 | 0 |
| 4 | 0,9820137900 | 0,9820137900 | 0 |
| 6 | 0,9975273768 | 0,9975273768 | 0 |
| 10 | 0,9999546021 | 0,9999546021 | 0 |

---

## 4. Erros da função × Tempo de execução

Medido com 200.000 pontos aleatórios em [−1, 1] (melhor de 5 execuções, Python 3, `erro_vs_tempo.py`; os tempos variam por máquina):

| N | Erro máx. | Erro médio | µs / chamada |
|---|---|---|---|
| 1 | 1,89e-02 | 4,89e-03 | 0,094 |
| 3 | 1,89e-03 | 3,23e-04 | 0,121 |
| 5 | 1,91e-04 | 2,44e-05 | 0,142 |
| 7 | 1,94e-05 | 1,97e-06 | 0,158 |
| 9 | 1,96e-06 | 1,66e-07 | 0,181 |
| **11** | **1,99e-07** | **1,44e-08** | **0,200** |
| 13 | 2,02e-08 | 1,27e-09 | 0,224 |
| 15 | 2,04e-09 | 1,15e-10 | 0,256 |
| exata (`math.exp`) | ~1e-16 | n/a | 0,118 |

**Conclusões:**

- Cada +2 em N: erro cai ~10× e o tempo sobe ~0,02 µs (custo linear, ganho exponencial).
- **Em Python, a função exata é mais rápida** que o Taylor, pois `math.exp` é código C compilado e o laço de Horner roda no interpretador. O Taylor compensa em contextos em que `exp` é caro (hardware sem FPU, FPGA, microcontroladores, SIMD, GPU), onde só multiplicações e somas estão disponíveis. Essa limitação precisa ser dita na apresentação.
- Em N ≥ 15 o erro de truncamento (~2e-9) já está longe do erro de arredondamento do `float64` (~1e-16), então N maior só vale a pena em intervalos menores.

---

## 5. Gráficos (`plots.py`)

O `plots.py` usa as funções do `sigmoid_taylor.py` e gera 4 gráficos com **matplotlib**, salvos como PNG na pasta onde o comando é executado. Precisa estar na mesma pasta do `sigmoid_taylor.py`.

```bash
python plots.py
```