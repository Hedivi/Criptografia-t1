import pandas as pd

INPUT_CSV = "estatistica.csv"
OUTPUT_CSV = "estatistica_resumo.csv"

df = pd.read_csv(INPUT_CSV, sep=";")
df.columns = df.columns.str.strip()

df["TIME"] = pd.to_numeric(df["TIME"], errors="raise")

# Normaliza o INPUT.
# Exemplo:
# cifras/rsa-1-musa_consolatrix.txt-21.txt
# ->
# cifras/rsa-1-musa_consolatrix.txt
df["INPUT_GROUP"] = df["INPUT"].str.replace(
    r"-\d+\.txt$",
    "",
    regex=True
)

GROUP_COLS = ["CIPHER", "TYPE", "INPUT_GROUP"]

# Número da execução dentro de cada grupo
df["EXECUCAO"] = df.groupby(
    GROUP_COLS,
    sort=False
).cumcount() + 1

# Exclui a primeira execução de cada grupo
df = df[df["EXECUCAO"] > 1]

# Calcula estatísticas
resumo = (
    df.groupby(GROUP_COLS, sort=False)["TIME"]
    .agg(
        EXECUCOES="count",
        MEDIA="mean",
        DESVIO_PADRAO="std"
    )
    .reset_index()
)

resumo = resumo.rename(
    columns={"INPUT_GROUP": "INPUT"}
)

resumo.to_csv(
    OUTPUT_CSV,
    sep=";",
    index=False,
    float_format="%.9f"
)

print(resumo.to_string(index=False))

print(f"\nResultado salvo em: {OUTPUT_CSV}")
