import pandas as pd

INPUT_CSV = "estatistica.csv"
OUTPUT_CSV = "estatistica_resumo.csv"

df = pd.read_csv(INPUT_CSV, sep=";")
df.columns = df.columns.str.strip()

df["TIME"] = pd.to_numeric(df["TIME"], errors="raise")

df["INPUT_GROUP"] = df["INPUT"].str.replace(r"-\d+\.txt$", "", regex=True)

GROUP_COLS = ["CIPHER", "TYPE", "INPUT_GROUP"]

df["EXECUCAO"] = df.groupby(GROUP_COLS, sort=False).cumcount() + 1

df = df[df["EXECUCAO"] > 1]

resumo = (df.groupby(GROUP_COLS, sort=False)["TIME"].agg(EXECUCOES="count", MEDIA="mean", DESVIO_PADRAO="std").reset_index())

resumo = resumo.rename(columns={"INPUT_GROUP": "INPUT"})

resumo.to_csv(OUTPUT_CSV, sep=";", index=False, float_format="%.9f")

print(resumo.to_string(index=False))

