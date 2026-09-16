import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from distribuicoes import distribuicao_normal, distribuicao_poisson
import numpy as np

from minhastats import (
    media,
    mediana,
    moda,
    amplitude,
    variancia,
    desvio_padrao, 
    quartis,
    coeficiente_variacao,
    frequencia,
    assimetria,
    interpretar_assimetria,
    tabela_frequencia_classes,
    correlacao_pearson,
    regressao_linear,
    coeficiente_determinacao,
)

from simulacoes import (
    simular_moeda,
    acompanhar_proporcao_caras, 
    simular_medias_amostrais
)

from dados import (
    carregar_dados,
    obter_colunas_numericas,
    obter_colunas_categoricas
)


st.title("Laboratório Estatístico Interativo")

st.write(
    "Explore os dados de acidentes rodoviários da Austrália "
    "por meio de diferentes ferramentas estatísticas."
)

dados = carregar_dados()

st.subheader("Visão geral dos dados")

st.write(f"Quantidade de registros: {len(dados)}")

st.write("Variáveis numéricas:")
st.write(obter_colunas_numericas(dados))

st.write("Variáveis categóricas:")
st.write(obter_colunas_categoricas(dados))

st.subheader("Análise de uma variável numérica")

variavel_escolhida = st.selectbox(
    "Variável:",
    obter_colunas_numericas(dados)
)

valores = dados[variavel_escolhida].dropna().tolist()

if variavel_escolhida in ["Age", "Speed Limit"]:

    media_normal = media(valores)
    desvio_normal = desvio_padrao(valores)

    menor_valor = min(valores)
    maior_valor = max(valores)

    x_normal = np.linspace(
        menor_valor,
        maior_valor,
        100
    )

    y_normal = []

    for x in x_normal:
        y = distribuicao_normal(
            x,
            media_normal,
            desvio_normal
        )

        y_normal.append(y)

    st.subheader("Distribuição Normal")

    fig, ax = plt.subplots()

    ax.hist(
        valores,
        bins=10,
        density=True,
        alpha=0.6,
        label="Dados"
    )

    ax.plot(
        x_normal,
        y_normal,
        label="Distribuição Normal"
    )

    ax.set_xlabel(variavel_escolhida)
    ax.set_ylabel("Densidade")
    ax.set_title(
        f"{variavel_escolhida} e distribuição Normal"
    )

    ax.legend()

    st.pyplot(fig)

    valor_assimetria_normal = assimetria(valores)

    if abs(valor_assimetria_normal) < 0.5:
        st.success(
            "A distribuição dos dados apresenta pouca assimetria, "
            "então a curva Normal apresenta um ajuste visual razoável."
        )

    elif abs(valor_assimetria_normal) < 1:
        st.info(
            "A distribuição dos dados apresenta assimetria moderada. "
            "A curva Normal serve como aproximação, mas não representa "
            "perfeitamente o formato dos dados."
        )

    else:
        st.warning(
            "A distribuição dos dados apresenta assimetria elevada. "
            "A curva Normal apresenta um ajuste visual fraco aos dados."
        )

else:

    st.subheader("Distribuição Normal")

    st.info(
        "A distribuição Normal não foi aplicada a esta variável "
        "porque ela representa um período de tempo discreto."
    )

resultado_media = media(valores)

st.write("Média:", f"{resultado_media:.2f}")

resultado_mediana = mediana(valores)

st.write("Mediana:", f"{resultado_mediana:.2f}")

resultado_moda = moda(valores)

st.write("Moda:", resultado_moda)

resultado_amplitude = amplitude(valores)

st.write("Amplitude:", f"{resultado_amplitude:.2f}")
tipo_variancia = st.radio(
    "Tipo de cálculo da variância e do desvio padrão:",
    ["Amostral", "Populacional"],
    horizontal=True
)

amostral = tipo_variancia == "Amostral"

resultado_variancia = variancia(
    valores,
    amostral=amostral
)

st.write(
    "Variância:",
    f"{resultado_variancia:.4f}"
)

resultado_desvio = desvio_padrao(
    valores,
    amostral=amostral
)

st.write(
    "Desvio padrão:",
    f"{resultado_desvio:.4f}"
)

resultado_quartis = quartis(valores)

st.write(
    "Quartis:",
    tuple(round(valor, 2) for valor in resultado_quartis)
)

resultado_cv = coeficiente_variacao(
    valores,
    amostral=amostral
)

st.write(
    "Coeficiente de variação:",
    f"{resultado_cv:.4f}%"
)

valor_assimetria = assimetria(valores)

st.write("Assimetria:", f"{valor_assimetria:.2f}")

st.write(
    "Interpretação da assimetria:",
    interpretar_assimetria(valor_assimetria)
)

if resultado_media > resultado_mediana:
    st.write(
        "Interpretação geral: a média é maior que a mediana, "
        "indicando influência de valores mais altos na distribuição."
    )

elif resultado_media < resultado_mediana:
    st.write(
        "Interpretação geral: a média é menor que a mediana, "
        "indicando influência de valores mais baixos na distribuição."
    )

else:
    st.write(
        "Interpretação geral: a média e a mediana são iguais, "
        "indicando equilíbrio entre os valores."
    )

st.subheader("Tabela de frequência")

if variavel_escolhida in ["Age", "Speed Limit"]:
    frequencias = tabela_frequencia_classes(valores)

    tabela_frequencia = pd.DataFrame(
    frequencias,
    columns=["Faixa", "Frequência"]

    )

else:
    frequencias = frequencia(valores)

    tabela_frequencia = pd.DataFrame(
        list(frequencias.items()),
        columns=["Valor", "Frequência"]
    )

tabela_frequencia.index = range(1, len(tabela_frequencia) + 1)

st.dataframe(tabela_frequencia)

q1, q2, q3 = quartis(valores)

iqr = q3 - q1

st.write("IQR:", iqr)

limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

outliers = [
    valor for valor in valores
    if valor < limite_inferior or valor > limite_superior
]

st.write("Limite inferior:", limite_inferior)
st.write("Limite superior:", limite_superior)
st.write("Quantidade de outliers:", len(outliers))

st.subheader("Histograma")

fig, ax = plt.subplots()

ax.hist(valores, bins=10)

ax.set_xlabel(variavel_escolhida)
ax.set_ylabel("Frequência")
ax.set_title(f"Distribuição de {variavel_escolhida}")

st.pyplot(fig)

st.subheader("Boxplot")

fig, ax = plt.subplots()

ax.boxplot(valores)

ax.set_ylabel(variavel_escolhida)
ax.set_title(f"Distribuição de {variavel_escolhida}")

st.pyplot(fig)

st.subheader("Análise de uma variável categórica")

variavel_categorica = st.selectbox(
    "Variável categórica:",
    obter_colunas_categoricas(dados)
)

valores_categoricos = dados[variavel_categorica].dropna().tolist()

frequencias_categoricas = frequencia(valores_categoricos)

tabela_categorica = pd.DataFrame(
    list(frequencias_categoricas.items()),
    columns=["Categoria", "Frequência"]
)

tabela_categorica.index = range(1, len(tabela_categorica) + 1)

st.dataframe(tabela_categorica)

st.subheader("Gráfico de frequência")

st.bar_chart(
    tabela_categorica.set_index("Categoria")["Frequência"]
)

st.subheader("Lei dos Grandes Números")

repeticoes = st.slider(
    "Quantidade de lançamentos:",
    min_value=10,
    max_value=10000,
    value=1000,
    step=10
)

resultados_moeda = simular_moeda(repeticoes)

proporcoes = acompanhar_proporcao_caras(resultados_moeda)

fig, ax = plt.subplots()

ax.plot(range(1, len(proporcoes) + 1), proporcoes)

ax.axhline(
    0.5,
    linestyle="--"
)

ax.set_xlabel("Número de lançamentos")
ax.set_ylabel("Proporção de caras")
ax.set_title("Lei dos Grandes Números")

st.pyplot(fig)

st.subheader("Teorema do Limite Central")

tamanho_amostra = st.slider(
    "Tamanho de cada amostra:",
    min_value=5,
    max_value=100,
    value=30,
    step=5
)

repeticoes_tlc = st.slider(
    "Quantidade de repetições:",
    min_value=10,
    max_value=1000,
    value=100,
    step=10
)

idades = dados["Age"].dropna().tolist()

medias_tlc = simular_medias_amostrais(
    idades,
    tamanho_amostra,
    repeticoes_tlc
)

st.write("Quantidade de médias calculadas:", len(medias_tlc))

st.subheader("Distribuição das médias amostrais")

fig, ax = plt.subplots()

ax.hist(medias_tlc, bins=20)

ax.set_xlabel("Média das amostras")
ax.set_ylabel("Frequência")
ax.set_title("Teorema do Limite Central")

st.pyplot(fig)

st.subheader("Distribuição de Poisson")

acidentes_por_mes = (
    dados
    .groupby(["Year", "Month"])["Crash ID"]
    .nunique()
)

todos_os_meses = pd.MultiIndex.from_product(
    [
        range(dados["Year"].min(), dados["Year"].max() + 1),
        range(1, 13)
    ],
    names=["Year", "Month"]
)

acidentes_por_mes = (
    acidentes_por_mes
    .reindex(todos_os_meses, fill_value=0)
    .tolist()
)
st.write("Quantidade de meses:", len(acidentes_por_mes))

lambda_poisson = media(acidentes_por_mes)

variancia_acidentes = variancia(acidentes_por_mes)

st.write(
    "Média de acidentes por mês (λ):",
    f"{lambda_poisson:.2f}"
)

st.write(
    "Variância dos acidentes por mês:",
    f"{variancia_acidentes:.2f}"
)

razao_variancia_media = variancia_acidentes / lambda_poisson

st.write(
    "Razão entre variância e média:",
    f"{razao_variancia_media:.2f}"
)

if abs(variancia_acidentes - lambda_poisson) < lambda_poisson * 0.2:
    st.success(
        "A média e a variância são relativamente próximas, "
        "o que indica um ajuste razoável à distribuição de Poisson."
    )
else:
   st.warning(
    f"A variância ({variancia_acidentes:.2f}) é aproximadamente "
    f"{razao_variancia_media:.2f} vezes maior que a média "
    f"({lambda_poisson:.2f}). Isso indica sobredispersão, "
    "ou seja, os acidentes mensais apresentam uma variabilidade "
    "maior do que a esperada por uma distribuição de Poisson."
)

valor_minimo = min(acidentes_por_mes)
valor_maximo = max(acidentes_por_mes)

k_poisson = range(
    0,
    valor_maximo + 1
)

probabilidades_poisson = []

for k in k_poisson:
    probabilidade = distribuicao_poisson(
        k,
        lambda_poisson
    )

    probabilidades_poisson.append(probabilidade)

fig, ax = plt.subplots()

# Frequência relativa dos dados reais
frequencias = {}

for valor in acidentes_por_mes:
    if valor in frequencias:
        frequencias[valor] += 1
    else:
        frequencias[valor] = 1

frequencias_reais = []

for k in k_poisson:
    quantidade = frequencias.get(k, 0)
    frequencia = quantidade / len(acidentes_por_mes)
    frequencias_reais.append(frequencia)
ax.bar(
    list(k_poisson),
    frequencias_reais,
    alpha=0.6,
    label="Dados reais"
)

ax.plot(
    list(k_poisson),
    probabilidades_poisson,
    "o-",
    label="Distribuição de Poisson"
)

ax.set_xlabel("Quantidade de acidentes no mês")
ax.set_ylabel("Probabilidade / frequência relativa")
ax.set_title("Acidentes mensais e distribuição de Poisson")

ax.legend()

st.pyplot(fig)

st.subheader("Correlação e Regressão")

variavel_x = st.selectbox(
    "Variável X:",
    obter_colunas_numericas(dados)
)

variavel_y = st.selectbox(
    "Variável Y:",
    obter_colunas_numericas(dados)
)

if variavel_x == variavel_y:
    st.warning(
        "Escolha duas variáveis diferentes para realizar a análise."
    )

else:
    dados_regressao = dados[[variavel_x, variavel_y]].dropna()

    valores_x = dados_regressao[variavel_x].tolist()
    valores_y = dados_regressao[variavel_y].tolist()

    correlacao = correlacao_pearson(
        valores_x,
        valores_y
    )

    st.write(
        "Correlação de Pearson:",
        f"{correlacao:.3f}"
    )

    inclinacao, intercepto = regressao_linear(
        valores_x,
        valores_y
    )

    st.write(
        "Inclinação da reta:",
        f"{inclinacao:.4f}"
    )

    st.write(
        "Intercepto:",
        f"{intercepto:.4f}"
    )

    st.write(
        f"Equação da reta: y = {inclinacao:.4f}x + {intercepto:.4f}"
    )

    valores_previstos = [
        intercepto + inclinacao * x
        for x in valores_x
    ]

    r2 = coeficiente_determinacao(
        valores_y,
        valores_previstos
    )

    st.write(
        "R²:",
        f"{r2:.3f}"
    )

    st.subheader("Previsão")

    valor_x = st.number_input(
        f"Digite um valor de {variavel_x}:",
        min_value=int(min(valores_x)),
        max_value=int(max(valores_x)),
        value=int(media(valores_x)),
        step=1
    )

    previsao = intercepto + inclinacao * valor_x

    st.write(
        f"Valor previsto de {variavel_y}: {previsao:.0f}"
    )

    st.subheader("Interpretação")

    if abs(correlacao) < 0.2:
        intensidade = "muito fraca"
    elif abs(correlacao) < 0.5:
        intensidade = "moderada"
    else:
        intensidade = "forte"

    if correlacao > 0:
        direcao = "positiva"
    elif correlacao < 0:
        direcao = "negativa"
    else:
        direcao = "nula"

    st.write(
        f"A correlação indica uma relação linear {direcao} "
        f"{intensidade} entre as variáveis."
    )

    if inclinacao > 0:
        st.write(
            f"Interpretação da inclinação: para cada aumento de 1 unidade "
            f"em {variavel_x}, o modelo prevê um aumento médio de "
            f"{inclinacao:.4f} unidades em {variavel_y}."
        )
    elif inclinacao < 0:
        st.write(
            f"Interpretação da inclinação: para cada aumento de 1 unidade "
            f"em {variavel_x}, o modelo prevê uma redução média de "
            f"{abs(inclinacao):.4f} unidades em {variavel_y}."
        )
    else:
        st.write(
            f"Interpretação da inclinação: o modelo não indica mudança "
            f"linear em {variavel_y} quando {variavel_x} aumenta."
        )

    st.write(
        f"Interpretação do intercepto: quando {variavel_x} é igual a 0, "
        f"o modelo prevê {intercepto:.4f} para {variavel_y}. "
        "Dependendo das variáveis escolhidas, esse valor pode não ter "
        "uma interpretação prática."
    )

    st.write(
        f"O modelo explica aproximadamente {r2 * 100:.2f}% "
        "da variação da variável Y."
    )

    st.info(
        "A correlação e a regressão mostram apenas uma associação "
        "linear entre as variáveis. Isso não significa que uma variável "
        "cause a outra."
    )

    st.subheader("Gráfico de dispersão")

    fig, ax = plt.subplots()

    ax.scatter(
        valores_x,
        valores_y,
        alpha=0.3
    )

    x_linha = sorted(valores_x)

    y_linha = [
        intercepto + inclinacao * x
        for x in x_linha
    ]

    ax.plot(
        x_linha,
        y_linha,
        label="Regressão linear"
    )

    ax.set_xlabel(variavel_x)
    ax.set_ylabel(variavel_y)
    ax.set_title(
        f"{variavel_x} × {variavel_y}"
    )

    ax.legend()

    st.pyplot(fig)


st.header("Descobertas Estatísticas")

st.write(
    "Nesta seção são apresentadas três descobertas "
    "estatísticas interessantes encontradas no conjunto de dados."
)

st.subheader(
    "1. Registros fatais envolvendo homens são mais que o dobro dos envolvendo mulheres"
)

quantidade_homens = (dados["Gender"] == "Male").sum()
quantidade_mulheres = (dados["Gender"] == "Female").sum()

razao_genero = quantidade_homens / quantidade_mulheres

st.write(
    "Foram registrados "
    + f"{quantidade_homens:,}".replace(",", ".")
    + " casos envolvendo homens e "
    + f"{quantidade_mulheres:,}".replace(",", ".")
    + " envolvendo mulheres."
)

st.write(
    f"Isso representa aproximadamente {razao_genero:.2f}".replace(".", ",")
    + " registros envolvendo homens para cada registro envolvendo mulheres."
)

fig, ax = plt.subplots(figsize=(2, 3))

ax.pie(
    [quantidade_homens, quantidade_mulheres],
    labels=["Homens", "Mulheres"],
    autopct="%1.1f%%"
)

ax.set_title("Registros fatais por gênero")

st.pyplot(fig)

st.subheader(
    "2. A quantidade de registros varia muito entre os estados"
)

quantidade_por_estado = dados["State"].value_counts()

estado_maior = quantidade_por_estado.idxmax()
quantidade_maior = quantidade_por_estado.max()

estado_menor = quantidade_por_estado.idxmin()
quantidade_menor = quantidade_por_estado.min()

razao_estados = quantidade_maior / quantidade_menor

st.write(
    f"O estado com mais registros foi {estado_maior}, "
    f"com {quantidade_maior:,}".replace(",", ".")
    + " registros."
)

st.write(
    f"O estado com menos registros foi {estado_menor}, "
    f"com {quantidade_menor:,}".replace(",", ".")
    + " registros."
)

st.write(
    f"Isso representa uma diferença de aproximadamente "
    f"{razao_estados:.2f}".replace(".", ",")
    + " vezes entre os dois estados."
)

fig, ax = plt.subplots(figsize=(7, 4))

ax.bar(
    quantidade_por_estado.index,
    quantidade_por_estado.values
)

ax.set_xlabel("Estado")
ax.set_ylabel("Quantidade de registros")
ax.set_title("Registros fatais por estado")

st.pyplot(fig)


st.subheader(
    "3. A faixa etária mais comum nos registros fatais"
)

quantidade_por_idade = dados["Age Group"].value_counts()

faixa_mais_comum = quantidade_por_idade.idxmax()
quantidade_mais_comum = quantidade_por_idade.max()

nomes_faixas = {
    "0_to_16": "0–16",
    "17_to_25": "17–25",
    "26_to_39": "26–39",
    "40_to_64": "40–64",
    "65_to_74": "65–74",
    "75_or_older": "75+"
}

faixas_formatadas = [
    nomes_faixas.get(faixa, faixa)
    for faixa in quantidade_por_idade.index
]

st.write(
    f"A faixa etária com mais registros foi "
    f"{nomes_faixas.get(faixa_mais_comum, faixa_mais_comum)}, "
    f"com {quantidade_mais_comum:,}".replace(",", ".")
    + " registros."
)

fig, ax = plt.subplots(figsize=(7, 4))

ax.bar(
    faixas_formatadas,
    quantidade_por_idade.values
)

ax.set_xlabel("Faixa etária")
ax.set_ylabel("Quantidade de registros")
ax.set_title("Registros fatais por faixa etária")

st.pyplot(fig)