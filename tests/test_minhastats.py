import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from minhastats import (
    media,
    mediana,
    moda,
    amplitude,
    variancia,
    desvio_padrao,
    percentil,
    quartis,
    coeficiente_variacao,
    covariancia,
    correlacao_pearson,
    regressao_linear,
    coeficiente_determinacao,
)

import numpy as np

TOLERANCIA = 1e-9


def test_media():
    resultado = media([10, 20, 30])
    assert resultado == 20


def test_mediana():
    resultado = mediana([10, 20, 30])
    assert resultado == 20


def test_moda():
    resultado = moda([2, 5, 5, 7, 9])
    assert resultado == [5]


def test_amplitude():
    resultado = amplitude([10, 20, 35, 50])
    assert resultado == 40


def test_variancia():
    resultado = variancia([10, 20, 30])
    assert resultado == 100


def test_desvio_padrao():
    resultado = desvio_padrao([10, 20, 30])
    assert resultado == 10


def test_percentil():
    resultado = percentil([10, 20, 30, 40, 50], 25)
    assert resultado == 20


def test_quartis():
    resultado = quartis([10, 20, 30, 40, 50])
    assert resultado == (20, 30, 40)


def test_coeficiente_variacao():
    resultado = coeficiente_variacao([10, 20, 30])
    assert resultado == 50


def test_covariancia():
    resultado = covariancia([10, 20, 30], [20, 40, 60])
    assert resultado == 200


def test_correlacao_pearson():
    resultado = correlacao_pearson([1, 2, 3, 4], [2, 4, 6, 8])
    assert resultado == 1


def test_mediana_com_numpy():
    valores = [10, 20, 30, 40, 50]

    resultado_nosso = mediana(valores)
    resultado_numpy = np.median(valores)

    assert abs(resultado_nosso - resultado_numpy) < TOLERANCIA


def test_variancia_com_numpy():
    valores = [10, 20, 30, 40, 50]

    resultado_nosso = variancia(valores)
    resultado_numpy = np.var(valores, ddof=1)

    assert abs(resultado_nosso - resultado_numpy) < TOLERANCIA


def test_desvio_padrao_com_numpy():
    valores = [10, 20, 30, 40, 50]

    resultado_nosso = desvio_padrao(valores)
    resultado_numpy = np.std(valores, ddof=1)

    assert abs(resultado_nosso - resultado_numpy) < TOLERANCIA


def test_percentil_com_numpy():
    valores = [10, 20, 30, 40, 50]

    resultado_nosso = percentil(valores, 25)
    resultado_numpy = np.percentile(valores, 25)

    assert abs(resultado_nosso - resultado_numpy) < TOLERANCIA


def test_quartis_com_numpy():
    valores = [10, 20, 30, 40, 50]

    resultado_nosso = quartis(valores)

    q1_numpy = np.percentile(valores, 25)
    q2_numpy = np.percentile(valores, 50)
    q3_numpy = np.percentile(valores, 75)

    assert abs(resultado_nosso[0] - q1_numpy) < TOLERANCIA
    assert abs(resultado_nosso[1] - q2_numpy) < TOLERANCIA
    assert abs(resultado_nosso[2] - q3_numpy) < TOLERANCIA


def test_media_com_numpy():
    valores = [10, 20, 30, 40, 50]

    resultado_nosso = media(valores)
    resultado_numpy = np.mean(valores)

    assert abs(resultado_nosso - resultado_numpy) < TOLERANCIA


def test_coeficiente_variacao_com_numpy():
    valores = [10, 20, 30, 40, 50]

    resultado_nosso = coeficiente_variacao(valores)

    media_numpy = np.mean(valores)
    desvio_numpy = np.std(valores, ddof=1)
    resultado_numpy = (desvio_numpy / media_numpy) * 100

    assert abs(resultado_nosso - resultado_numpy) < TOLERANCIA


def test_covariancia_com_numpy():
    x = [10, 20, 30, 40, 50]
    y = [20, 40, 60, 80, 100]

    resultado_nosso = covariancia(x, y)
    resultado_numpy = np.cov(x, y, ddof=1)[0, 1]

    assert abs(resultado_nosso - resultado_numpy) < TOLERANCIA


def test_correlacao_pearson_com_numpy():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    resultado_nosso = correlacao_pearson(x, y)
    resultado_numpy = np.corrcoef(x, y)[0, 1]

    assert abs(resultado_nosso - resultado_numpy) < TOLERANCIA


def test_regressao_linear():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]

    inclinacao, intercepto = regressao_linear(x, y)

    assert abs(inclinacao - 2) < TOLERANCIA
    assert abs(intercepto - 0) < TOLERANCIA


def test_coeficiente_determinacao():
    valores_y = [2, 4, 6, 8, 10]
    valores_previstos = [2, 4, 6, 8, 10]

    resultado = coeficiente_determinacao(
        valores_y,
        valores_previstos
    )

    assert abs(resultado - 1) < TOLERANCIA