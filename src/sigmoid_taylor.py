"""
Sigmoide  y = sig(x) = 1 / (1 + e^-x)  e sua série de Taylor (Maclaurin) em x0 = 0.

Derivadas feitas "à mão": usamos  sig' = sig * (1 - sig)  e a regra da cadeia
para obter cada derivada como um POLINÔMIO em s = sig(x):
        d^n sig / dx^n = P_n(s),    P_{n+1}(s) = P_n'(s) * s * (1 - s)
Nenhuma biblioteca simbólica foi usada (só Fraction, da biblioteca padrão).
"""
import math
from fractions import Fraction

# ---------------------------------------------------------------- derivadas
def derivada_polinomio(p):
    """Derivada de um polinômio (lista de coeficientes, índice = grau)."""
    return [i * p[i] for i in range(1, len(p))] or [Fraction(0)]

def multi_polinomio(a, b):
    r = [Fraction(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            r[i + j] += ai * bj
    return r

def derivadas_polinomiais(n_max):
    "Gerando os polinômios que permitem calcular derivadas sucessivas da sigmoide usando apenas a própria sigmoide."
    polys = [[Fraction(0), Fraction(1)]]            # P_0(s) = s
    s_1ms = [Fraction(0), Fraction(1), Fraction(-1)]  # s(1-s) = s - s^2
    for _ in range(n_max):
        polys.append(multi_polinomio(derivada_polinomio(polys[-1]), s_1ms))
    return polys

def coeficientes_taylor(n_max):
    """c_n = sig^(n)(0) / n!  com sig(0) = 1/2 (exato, em Fraction)."""
    half = Fraction(1, 2)
    coefs = []
    for n, p in enumerate(derivadas_polinomiais(n_max)):
        value = sum(c * half**k for k, c in enumerate(p))   # P_n(1/2)
        coefs.append(value / math.factorial(n))
    return coefs

# --------------------------------------------------------------- aproximações
def sigmoid_exata(x):
    """Referência: versão numericamente estável (evita overflow de exp)."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)

def fazer_sigmoid_taylor(N):
    """
    Gera sig_N(x) = polinômio de Taylor de grau N, OTIMIZADO:
      1) só coeficientes ímpares != 0 (sig - 1/2 é função ímpar) -> metade das contas
      2) Maior grau em u = x^2 -> sem pow(), N/2 multiplicações
      3) simetria sig(-x) = 1 - sig(x)  -> não depende do sinal de x
      4) coeficientes pré-calculados em float -> nada é recalculado por chamada
    """
    c = coeficientes_taylor(N)
    odd = [float(c[k]) for k in range(1, N + 1, 2)]   # c1, c3, c5, ...
    odd.reverse()                                    
    head, tail = odd[0], odd[1:]

    def sig_n(x):
        u = x * x
        acc = head
        for a in tail:
            acc = acc * u + a
        return 0.5 + x * acc
    return sig_n

def fazer_sigmoide_hibrida(N, x_max):
    """Taylor para |x| <= x_max (onde converge bem); fora, forma exata."""
    taylor = fazer_sigmoid_taylor(N)
    def sig(x):
        if -x_max <= x <= x_max:
            return taylor(x)
        return sigmoid_exata(x)
    return sig
