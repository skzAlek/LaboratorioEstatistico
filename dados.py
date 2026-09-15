import pandas as pd


def carregar_dados():
    caminho = "data/Crash_Data.csv"

    dados = pd.read_csv(caminho, low_memory=False)

    # Transformamos o limite de velocidade em número.
    # Valores que não são números viram valores ausentes.
    dados["Speed Limit"] = pd.to_numeric(
        dados["Speed Limit"],
        errors="coerce"
    )

    # No dataset, -9 representa informação desconhecida.
    dados["Speed Limit"] = dados["Speed Limit"].replace(
        -9,
        float("nan")
    )

    dados["Age"] = dados["Age"].replace(
        -9,
        float("nan")
    )

    return dados

def obter_colunas_numericas(dados):
    return ["Month", "Year", "Speed Limit", "Age"]


def obter_colunas_categoricas(dados):
    return ["State", "Gender", "Crash Type", "Road User"]