from simulacoes import simular_moeda
from simulacoes import calcular_proporcao_caras
from simulacoes import acompanhar_proporcao_caras
from simulacoes import simular_medias_amostrais


def test_simular_moeda():
    resultados = simular_moeda(10)

    assert len(resultados) == 10

    for resultado in resultados:
        assert resultado in [0, 1]


def test_calcular_proporcao_caras():
    resultados = [1, 0, 1, 1, 0]

    resultado = calcular_proporcao_caras(resultados)

    assert resultado == 0.6


def test_acompanhar_proporcao_caras():
    resultados = [1, 0, 1, 1, 0]

    proporcoes = acompanhar_proporcao_caras(resultados)

    assert proporcoes == [
        1.0,
        0.5,
        0.6666666666666666,
        0.75,
        0.6
    ]


def test_simular_medias_amostrais():
    valores = [10, 20, 30, 40, 50]

    medias = simular_medias_amostrais(
        valores,
        tamanho_amostra=3,
        repeticoes=10
    )

    assert len(medias) == 10

    for resultado in medias:
        assert 10 <= resultado <= 50