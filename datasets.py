import pandas as pd


def get_ed_basica() -> "pd.DataFrame":

    df = pd.read_csv(
        "datasets/microdados_censo_escolar_2021/2021/dados/microdados_ed_basica_2021.csv",
        encoding="iso-8859-1",
        sep=";",
    )

    return df


def treatment_ed_basica(df):

    interest_columns = [
        "CO_MUNICIPIO",
        "TP_DEPENDENCIA",
        "TP_LOCALIZACAO",
        "IN_AGUA_POTAVEL",
        "IN_ENERGIA_INEXISTENTE",
        "IN_ESGOTO_REDE_PUBLICA",
        "IN_BIBLIOTECA_SALA_LEITURA",
        "IN_QUADRA_ESPORTES",
        "IN_SALA_ESTUDIO_DANCA",
        "QT_SALAS_UTILIZADAS",
        "QT_DESKTOP_ALUNO",
        "QT_COMP_PORTATIL_ALUNO",
        "IN_INTERNET",
        "TP_ATIVIDADE_COMPLEMENTAR",  # prestar atenção nesse caso, pois é 0,1,2
    ]
    # dependencia administrativa
    df = df.loc[:, interest_columns]
    df["TP_DEPENDENCIA"] = df["TP_DEPENDENCIA"].map(
        {1: "publico", 2: "publico", 3: "publico", 4: "privado"}
    )
    # retirando escolas com mais de 60 salas, outliers
    df = df[df["QT_SALAS_UTILIZADAS"] <= 60]

    # retirando escolas com mais de 50 desktops por aluno
    df = df[df["QT_DESKTOP_ALUNO"] <= 50]

    # retirando escola com mais de 50 computadores portáteis por aluno
    df = df[df["QT_COMP_PORTATIL_ALUNO"] <= 50]

    # localizacao
    df["TP_LOCALIZACAO"] = df["TP_LOCALIZACAO"].map({1: "urbana", 2: "rural"})

    # no caso dessa variável, considerei como ter a atividade, já como sim
    # 0 - Não oferece
    # 1 - Não exclusivamente
    # 2 - Exclusivamente

    df["TP_ATIVIDADE_COMPLEMENTAR"] = df["TP_ATIVIDADE_COMPLEMENTAR"].map(
        {0: "nao", 1: "sim", 2: "sim"}
    )
    df["TP_ATIVIDADE_COMPLEMENTAR"] = df["TP_ATIVIDADE_COMPLEMENTAR"].fillna("nao")

    return df


def get_unique_municipios(ed_basica):

    df = ed_basica[["CO_MUNICIPIO"]].drop_duplicates()
    df = df.reset_index(drop=True)
    return df
