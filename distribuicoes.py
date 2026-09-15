import math


def distribuicao_normal(x, media_valores, desvio):
    parte_1 = 1 / (desvio * math.sqrt(2 * math.pi))

    parte_2 = math.exp(
        -((x - media_valores) ** 2) / (2 * desvio ** 2)
    )

    return parte_1 * parte_2

def distribuicao_poisson(k, lamb):
    log_probabilidade = (
        -lamb
        + k * math.log(lamb)
        - math.lgamma(k + 1)
    )

    return math.exp(log_probabilidade)

