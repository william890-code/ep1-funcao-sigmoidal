from math import exp
from timeit import repeat
from cmath import exp as complex_exp
import matplotlib.pyplot as plt


def sigmoide(x: float | complex) -> float | complex:
    """Calcula a sigmoide logística para uma entrada real ou complexa."""
    if isinstance(x, complex):
        return 1.0 / (1.0 + complex_exp(-x))

    if x >= 0:
        return 1.0 / (1.0 + exp(-x))

    exp_x = exp(x)
    return exp_x / (1.0 + exp_x)


def sigmoide_taylor(x: float | complex) -> float | complex:
    """Calcula a aproximação de Taylor até o grau 9."""
    return (
        0.5 + x / 4 - x**3 / 48 + x**5 / 480 - 17 * x**7 / 80640 + 31 * x**9 / 1451520
    )

    """passo a passo"""


def sigmoide_taylor_passo_a_passo(x: float | complex) -> float | complex:
    termos = [
        ("termo constante: 1/2", 0.5),
        ("termo x/4", x / 4),
        ("termo -x³/48", -(x**3) / 48),
        ("termo x⁵/480", x**5 / 480),
        ("termo -17x⁷/80640", -17 * x**7 / 80640),
        ("termo 31x⁹/1451520", 31 * x**9 / 1451520),
    ]

    soma = 0
    print("\nPasso a passo da série de Taylor:")

    for nome, valor in termos:
        soma += valor
        print(
            f"{nome} = {formatar_numero(valor)}"
            f" | soma parcial = {formatar_numero(soma)}"
        )

    return soma


def formatar_numero(valor: float | complex) -> str:
    if isinstance(valor, complex):
        return f"{valor.real:.8f}{valor.imag:+.8f}j"
    return f"{valor:.8f}"


if __name__ == "__main__":
    while True:
        entrada = input(
            "Digite um número real ou complexo " "(ex.: 2, -1.5, 1+1j): "
        ).strip()

        try:
            z = complex(entrada.replace("i", "j"))
            x = z.real if z.imag == 0 else z
            break
        except ValueError:
            print("Entrada inválida. Tente, por exemplo, 2 ou 1+1j.")

    exata = sigmoide(x)
    aproximada = sigmoide_taylor_passo_a_passo(x)
    erro = abs(exata - aproximada)

    print(f"\nEntrada: {formatar_numero(x)}")
    print(f"Sigmoide: {formatar_numero(exata)}")
    print(f"Taylor grau 9: {formatar_numero(aproximada)}")
    print(f"Erro absoluto: {erro:.6e}")

    # Erro da aproximação para entradas reais entre -3 e 3
    xs = [i / 20 for i in range(-60, 61)]
    erros = [abs(sigmoide(valor) - sigmoide_taylor(valor)) for valor in xs]

    # Benchmark feito sem imprimir os tempos no terminal
    numero_de_chamadas = 100_000
    repeticoes = 5

    tempo_exata = (
        min(
            repeat(
                lambda: sigmoide(1.0),
                repeat=repeticoes,
                number=numero_de_chamadas,
            )
        )
        / numero_de_chamadas
    )

    tempo_taylor = (
        min(
            repeat(
                lambda: sigmoide_taylor(1.0),
                repeat=repeticoes,
                number=numero_de_chamadas,
            )
        )
        / numero_de_chamadas
    )

    print("\nTempo médio por chamada:")
    print(f"Sigmoide logística: {tempo_exata * 1e9:.1f} ns")
    print(f"Taylor grau 9: {tempo_taylor * 1e9:.1f} ns")

    # Gráfico do erro
    plt.figure(figsize=(8, 5))
    plt.plot(xs, erros)
    plt.xlabel("x real")
    plt.ylabel("Erro absoluto")
    plt.title("Erro da aproximação de Taylor de grau 9")
    plt.grid(True)
    plt.tight_layout()

    # Gráfico do tempo de execução
    plt.figure(figsize=(7, 5))
    plt.bar(
        ["Sigmoide logística", "Taylor grau 9"],
        [tempo_exata * 1e9, tempo_taylor * 1e9],
    )
    plt.ylabel("Tempo por chamada (ns)")
    plt.title("Tempo médio de execução")
    plt.tight_layout()

    plt.show()
