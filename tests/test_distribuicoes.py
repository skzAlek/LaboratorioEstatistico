import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from distribuicoes import distribuicao_normal, distribuicao_poisson


def test_distribuicao_normal():
    resultado = distribuicao_normal(30, 30, 5)

    assert abs(resultado - 0.07978845608028654) < 1e-9

def test_distribuicao_poisson():
    resultado = distribuicao_poisson(3, 4)

    assert abs(resultado - 0.19536681481316456) < 1e-9

from scipy.stats import norm


def test_distribuicao_normal_com_scipy():
    resultado = distribuicao_normal(30, 30, 5)

    esperado = norm.pdf(
        30,
        loc=30,
        scale=5
    )

    assert abs(resultado - esperado) < 1e-9

from scipy.stats import poisson


def test_distribuicao_poisson_com_scipy():
    resultado = distribuicao_poisson(3, 4)

    esperado = poisson.pmf(
        3,
        mu=4
    )

    assert abs(resultado - esperado) < 1e-9