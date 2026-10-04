import random, time
from sigmoid_taylor import *

random.seed(1)
data = [random.uniform(-1, 1) for _ in range(200000)]
ref = [sigmoid_exata(x) for x in data]

def bench(f):
    best = 1e9
    for _ in range(5):
        t = time.perf_counter()
        for x in data: f(x)
        best = min(best, time.perf_counter() - t)
    return best / len(data) * 1e6

print(" N | erro max [-1,1] | erro médio | µs/chamada")

for N in [1,3,5,7,9,11,13,15]:
    f = fazer_sigmoid_taylor(N)
    errs = [abs(f(x)-r) for x, r in zip(data, ref)]
    print(f"{N:>2} | {max(errs):.2e}        | {sum(errs)/len(errs):.2e}   | {bench(f):.3f}")

print(f"exata math.exp: {bench(sigmoid_exata):.3f} µs")

f = fazer_sigmoide_hibrida(11, 1.0)

print("\nTabela final (híbrida N=11, |x|<=1 Taylor):")

for x in [-10,-6,-4,-3,-2,-1,-0.5,0,0.5,1,2,3,4,6,10]:
    e = sigmoid_exata(x); t = f(x)
    print(f"{x:>5} | {e:.10f} | {t:.10f} | {abs(e-t):.1e}")
