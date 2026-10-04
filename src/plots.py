"""
Gráficos da sigmoide e da série de Taylor (matplotlib).

Uso:
    python plots.py             # salva os PNGs e abre as janelas
    python plots.py --no-show   # só salva os PNGs
"""
import sys
import time
import math
import matplotlib

if "--no-show" in sys.argv:
    matplotlib.use("Agg")          # sem janela, só arquivo
import matplotlib.pyplot as plt

from sigmoid_taylor import sigmoid_exata, fazer_sigmoid_taylor, fazer_sigmoide_hibrida

N_ESCOLHIDO = 11
X_MAX = 1.0


def linspace(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


# ------------------------------------------------ 1. Taylor x sigmoide exata
def grafico_taylor_vs_exata():
    xs = linspace(-4, 4, 401)
    plt.figure(figsize=(8, 5))
    plt.plot(xs, [sigmoid_exata(x) for x in xs], "k", linewidth=2.5, label="sig(x) exata")
    for N in (1, 3, 5, 11):
        f = fazer_sigmoid_taylor(N)
        plt.plot(xs, [f(x) for x in xs], label=f"Taylor N = {N}")
    plt.axvline(math.pi, color="gray", linestyle=":", label="x = ±π")
    plt.axvline(-math.pi, color="gray", linestyle=":")
    plt.ylim(-0.5, 1.5)           # sem isso o polinômio "explode" e achata o resto
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Sigmoide x polinômios de Taylor")
    plt.legend(loc="upper left")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("grafico_1_taylor_vs_exata.png", dpi=200)


# ------------------------------------------------ 2. Erro absoluto x x
def grafico_erro_vs_x():
    xs = linspace(-3, 3, 601)
    plt.figure(figsize=(8, 5))
    for N in (3, 5, 7, 9, 11):
        f = fazer_sigmoid_taylor(N)
        erros = [max(abs(f(x) - sigmoid_exata(x)), 1e-18) for x in xs]  # evita log(0)
        plt.semilogy(xs, erros, label=f"N = {N}")
    plt.axvline(X_MAX, color="gray", linestyle=":")
    plt.axvline(-X_MAX, color="gray", linestyle=":", label="|x| = 1 (limite do Taylor)")
    plt.xlabel("x")
    plt.ylabel("Erro absoluto (escala log)")
    plt.title("Erro da aproximação de Taylor")
    plt.legend()
    plt.grid(True, which="both", alpha=0.4)
    plt.tight_layout()
    plt.savefig("grafico_2_erro_vs_x.png", dpi=200)


# ------------------------------------------------ 3. Erro máximo x N
def grafico_erro_vs_N():
    xs = linspace(-X_MAX, X_MAX, 2001)
    Ns = list(range(1, 22, 2))
    erros = []
    for N in Ns:
        f = fazer_sigmoid_taylor(N)
        erros.append(max(abs(f(x) - sigmoid_exata(x)) for x in xs))
    plt.figure(figsize=(8, 5))
    plt.semilogy(Ns, erros, "o-", color="teal")
    plt.axvline(N_ESCOLHIDO, color="coral", linestyle="--", label=f"N escolhido = {N_ESCOLHIDO}")
    plt.xticks(Ns)
    plt.xlabel("N (grau do polinômio)")
    plt.ylabel("Erro máximo em [−1, 1]")
    plt.title("Erro máximo x grau N")
    plt.legend()
    plt.grid(True, which="both", alpha=0.4)
    plt.tight_layout()
    plt.savefig("grafico_3_erro_vs_N.png", dpi=200)


# ------------------------------------------------ 4. Erro x tempo
def medir_us(f, dados, repeticoes=5):
    melhor = float("inf")
    for _ in range(repeticoes):
        t = time.perf_counter()
        for x in dados:
            f(x)
        melhor = min(melhor, time.perf_counter() - t)
    return melhor / len(dados) * 1e6


def grafico_erro_vs_tempo():
    import random
    random.seed(1)
    dados = [random.uniform(-1, 1) for _ in range(100_000)]
    Ns = list(range(1, 16, 2))
    tempos, erros = [], []
    for N in Ns:
        f = fazer_sigmoid_taylor(N)
        tempos.append(medir_us(f, dados))
        erros.append(max(abs(f(x) - sigmoid_exata(x)) for x in dados))
    t_exata = medir_us(sigmoid_exata, dados)

    plt.figure(figsize=(8, 5))
    plt.semilogy(tempos, erros, "o-", color="teal", label="Taylor")
    for N, t, e in zip(Ns, tempos, erros):
        plt.annotate(f"N={N}", (t, e), textcoords="offset points", xytext=(6, 6), fontsize=8)
    plt.axvline(t_exata, color="coral", linestyle="--", label=f"math.exp ({t_exata:.3f} µs)")
    plt.xlabel("Tempo por chamada (µs)")
    plt.ylabel("Erro máximo em [−1, 1]")
    plt.title("Erro x tempo de execução")
    plt.legend()
    plt.grid(True, which="both", alpha=0.4)
    plt.tight_layout()
    plt.savefig("grafico_4_erro_vs_tempo.png", dpi=200)


if __name__ == "__main__":
    grafico_taylor_vs_exata()
    grafico_erro_vs_x()
    grafico_erro_vs_N()
    grafico_erro_vs_tempo()
    print("PNGs salvos: grafico_1..4_*.png")
    if "--no-show" not in sys.argv:
        plt.show()
