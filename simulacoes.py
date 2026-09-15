import random

from minhastats import media

def simular_moeda(repeticoes):
    resultados = []

    for _ in range(repeticoes):
        resultado = random.randint(0, 1)
        resultados.append(resultado)

    return resultados

def calcular_proporcao_caras(resultados):
    quantidade_caras = sum(resultados)
    quantidade_lancamentos = len(resultados)

    return quantidade_caras / quantidade_lancamentos

def acompanhar_proporcao_caras(resultados):
    proporcoes = []
    quantidade_caras = 0

    for i in range(len(resultados)):
        if resultados[i] == 1:
            quantidade_caras += 1

        proporcao = quantidade_caras / (i + 1)
        proporcoes.append(proporcao)

    return proporcoes

def simular_medias_amostrais(valores, tamanho_amostra, repeticoes):
    medias = []

    for _ in range(repeticoes):
        amostra = random.choices(valores, k=tamanho_amostra)
        media_amostra = media(amostra)
        medias.append(media_amostra)

    return medias