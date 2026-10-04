from math import exp


def sigmoide(x: float) -> float:
    """Calcula a função sigmoide logística para um número real."""
    if x >= 0:
        return 1.0 / (1.0 + exp(-x))

    exp_x = exp(x)
    return exp_x / (1.0 + exp_x)


if __name__ == "__main__":
    for x in (-5, -2, 0, 2, 5):
        print(f"x={x:>2}  sigmoide(x)={sigmoide(x):.8f}")
