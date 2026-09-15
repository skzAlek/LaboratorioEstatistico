def media(valores):
    return sum(valores) / len(valores)
def mediana(valores):
    valores_ordenados = sorted(valores)
    quantidade = len(valores_ordenados)
    meio = quantidade // 2

    if quantidade % 2 == 1:
        return valores_ordenados[meio]
    else:
        return (valores_ordenados[meio - 1] + valores_ordenados[meio]) / 2
def moda(valores):
    frequencias = {}

    for valor in valores:
        if valor in frequencias:
            frequencias[valor] += 1
        else:
            frequencias[valor] = 1

    maior_frequencia = max(frequencias.values())

    modas = []

    for valor, frequencia in frequencias.items():
        if frequencia == maior_frequencia:
            modas.append(valor)

    return modas
def amplitude(valores):
    return max(valores) - min(valores)
def variancia(valores, amostral=True):
    media_valores = media(valores)
    soma = 0

    for valor in valores:
        soma += (valor - media_valores) ** 2

    if amostral:
        return soma / (len(valores) - 1)
    else:
        return soma / len(valores)
def desvio_padrao(valores, amostral=True):
    return variancia(valores, amostral) ** 0.5
def percentil(valores, p):
    valores_ordenados = sorted(valores)
    n = len(valores_ordenados)

    if p < 0 or p > 100:
        raise ValueError("O percentil deve estar entre 0 e 100.")

    posicao = (p / 100) * (n - 1)
    inferior = int(posicao)
    superior = inferior + 1

    if superior >= n:
        return valores_ordenados[inferior]

    parte_decimal = posicao - inferior

    return (
        valores_ordenados[inferior]
        + parte_decimal
        * (valores_ordenados[superior] - valores_ordenados[inferior])
    )


def quartis(valores):
    return (
        percentil(valores, 25),
        percentil(valores, 50),
        percentil(valores, 75)
    )
def coeficiente_variacao(valores, amostral=True):
    media_valores = media(valores)
    desvio = desvio_padrao(valores, amostral)

    if media_valores == 0:
        raise ValueError("A média não pode ser zero.")

    return (desvio / media_valores) * 100
def covariancia(x, y, amostral=True):
    if len(x) != len(y):
        raise ValueError("As listas devem ter o mesmo tamanho.")

    media_x = media(x)
    media_y = media(y)

    soma = 0

    for i in range(len(x)):
        soma += (x[i] - media_x) * (y[i] - media_y)

    if amostral:
        return soma / (len(x) - 1)
    else:
        return soma / len(x)
def correlacao_pearson(x, y):
    if len(x) != len(y):
        raise ValueError("As listas devem ter o mesmo tamanho.")

    media_x = media(x)
    media_y = media(y)

    numerador = 0
    soma_x = 0
    soma_y = 0

    for i in range(len(x)):
        diferenca_x = x[i] - media_x
        diferenca_y = y[i] - media_y

        numerador += diferenca_x * diferenca_y
        soma_x += diferenca_x ** 2
        soma_y += diferenca_y ** 2

    denominador = (soma_x * soma_y) ** 0.5

    if denominador == 0:
        raise ValueError("Não é possível calcular a correlação.")

    return numerador / denominador

def frequencia(valores):
    frequencias = {}

    for valor in valores:
        if valor in frequencias:
            frequencias[valor] += 1
        else:
            frequencias[valor] = 1

    return frequencias

def assimetria(valores):
    media_valores = media(valores)
    desvio = desvio_padrao(valores, amostral=False)

    if desvio == 0:
        raise ValueError("Não é possível calcular a assimetria.")

    soma = 0

    for valor in valores:
        soma += ((valor - media_valores) / desvio) ** 3

    return soma / len(valores)

def interpretar_assimetria(valor):
    if valor > 0.5:
        return "A distribuição apresenta assimetria positiva (cauda à direita)."
    elif valor < -0.5:
        return "A distribuição apresenta assimetria negativa (cauda à esquerda)."
    else:
        return "A distribuição é aproximadamente simétrica."

def tabela_frequencia_classes(valores, tamanho_classe=10):
    menor = min(valores)
    maior = max(valores)

    inicio = (menor // tamanho_classe) * tamanho_classe

    tabela = []

    while inicio <= maior:
        fim = inicio + tamanho_classe - 1

        frequencia = 0

        for valor in valores:
            if inicio <= valor <= fim:
                frequencia += 1

        faixa = f"{int(inicio)}–{int(fim)}"

        tabela.append(
            (faixa, frequencia)
        )

        inicio += tamanho_classe

    return tabela

def regressao_linear(x, y):
    if len(x) != len(y):
        raise ValueError("As listas devem ter o mesmo tamanho.")

    media_x = media(x)
    media_y = media(y)

    numerador = 0
    denominador = 0

    for i in range(len(x)):
        numerador += (x[i] - media_x) * (y[i] - media_y)
        denominador += (x[i] - media_x) ** 2

    if denominador == 0:
        raise ValueError("Não é possível calcular a regressão.")

    inclinacao = numerador / denominador
    intercepto = media_y - inclinacao * media_x

    return inclinacao, intercepto

def coeficiente_determinacao(valores_y, valores_previstos):
    media_y = media(valores_y)

    soma_total = 0
    soma_residuos = 0

    for i in range(len(valores_y)):
        soma_total += (valores_y[i] - media_y) ** 2
        soma_residuos += (valores_y[i] - valores_previstos[i]) ** 2

    if soma_total == 0:
        raise ValueError(
            "Não é possível calcular o coeficiente de determinação."
        )

    return 1 - (soma_residuos / soma_total)