import sys
from sigmoid_taylor import fazer_sigmoide_hibrida, sigmoid_exata

N, X_MAX = 11, 1.0  #escolhidos no "arquivo inicial" (erro < 2.1e-7 em [-1,1])
sig = fazer_sigmoide_hibrida(N, X_MAX)

for arg in sys.argv[1:]:
    x = float(arg)
    print(f"x={x:<8} taylor={sig(x):.10f} exata={sigmoid_exata(x):.10f} erro={abs(sig(x)-sigmoid_exata(x)):.2e}")
