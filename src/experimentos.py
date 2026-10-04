import math, time
from sigmoid_taylor import *

print("=== Polinomios P_n(s) das derivadas (coef. de s^0, s^1, ...) ===")
for n, p in enumerate(derivadas_polinomiais(6)):
    print(n, [str(c) for c in p])

print("\n=== Coeficientes de Taylor em x0=0 ===")
for n, c in enumerate(coeficientes_taylor(11)):
    print(n, c, float(c))

def max_err(f, a, b, pts=4001):
    return max(abs(f(a + (b - a) * i / (pts - 1)) - sigmoid_exata(a + (b - a) * i / (pts - 1))) for i in range(pts))

print("\n=== Erro máximo absoluto  N x intervalo [-X, X] ===")
Xs = [0.5, 1, 2, 3]
print("N   " + "  ".join(f"X={X:<8}" for X in Xs))
for N in [1, 3, 5, 7, 9, 11, 13, 15, 17, 21]:
    f = fazer_sigmoid_taylor(N)
    print(f"{N:<3} " + "  ".join(f"{max_err(f,-X,X):<10.2e}" for X in Xs))

print("\n=== Tempo (µs/chamada) ===")
import random
random.seed(0)
data = [random.uniform(-2, 2) for _ in range(200000)]

def bench(f):
    melhor = 1e9
    for _ in range(5):
        t = time.perf_counter()
        for x in data: f(x)
        melhor = min(melhor, time.perf_counter() - t)
    return melhor / len(data) * 1e6

print("exata (math.exp)   ", f"{bench(sigmoid_exata):.3f}")

for N in [3, 5, 7, 9, 11, 13]:
    f = fazer_sigmoid_taylor(N)
    print(f"Taylor N={N:<3}       ", f"{bench(f):.3f}", f"  erro max [-2,2] = {max_err(f,-2,2):.2e}")

def ingenua(N):
    c = [float(v) for v in coeficientes_taylor(N)]
    return lambda x: sum(c[k] * x**k for k in range(N + 1))

print("ingênua N=9 (pow)  ", f"{bench(ingenua(9)):.3f}")

print("\n=== Tabela de valores fixos ===")

f9 = fazer_sigmoid_taylor(9)

print(" x     sig(x) exato      Taylor N=9        erro abs")

for x in [-6,-5,-4,-3,-2,-1,-0.5,0,0.5,1,2,3,4,5,6]:
    e, t = sigmoid_exata(x), f9(x)
    print(f"{x:>5}  {e:.12f}   {t:.12f}   {abs(e-t):.2e}")
