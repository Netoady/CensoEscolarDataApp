import pandas as pd
import json
import os

INPUT_FILE = "data/censo_escolar2024.csv"
OUTPUT_FILE = "output/ies_paraiba.json"
TOP3_FILE = "output/top3_paraiba.json"

def gerar_json():
    df = pd.read_csv("data/censo_escolar2024.csv", sep=";", encoding="latin1", low_memory=False)
    print(df.columns.tolist())

    print("Colunas disponíveis:", df.columns.tolist())
    print("Quantidade total de registros:", len(df))
    print("Registros com CO_UF == 25:", len(df[df["CO_UF"].astype(str) == "25"]))

    # Filtra apenas Paraíba
    df_paraiba = df[df["CO_UF"].astype(str) == "25"]

    cols = [
        "CO_ENTIDADE","NO_ENTIDADE","NO_UF","SG_UF","CO_UF","NO_MUNICIPIO","CO_MUNICIPIO",
        "NO_MESORREGIAO","CO_MESORREGIAO","NO_MICRORREGIAO","CO_MICRORREGIAO",
        "NU_ANO_CENSO","NO_REGIAO","CO_REGIAO",
        "QT_MAT_BAS","QT_MAT_INF","QT_MAT_FUND","QT_MAT_MED",
        "QT_MAT_PROF","QT_MAT_EJA","QT_MAT_ESP"
    ]
    df_paraiba = df_paraiba[cols]

    # Calcula total de matrículas
    df_paraiba["TOTAL_MATRICULAS"] = (
        df_paraiba["QT_MAT_BAS"] + df_paraiba["QT_MAT_INF"] +
        df_paraiba["QT_MAT_FUND"] + df_paraiba["QT_MAT_MED"] +
        df_paraiba["QT_MAT_PROF"] + df_paraiba["QT_MAT_EJA"] +
        df_paraiba["QT_MAT_ESP"]
    )

    # Ordena por total de matrículas
    df_paraiba = df_paraiba.sort_values(by="TOTAL_MATRICULAS", ascending=False)

    # Converte tudo para JSON
    json_data = df_paraiba.to_dict(orient="records")

    # Cria diretório de saída se não existir
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    # Salva JSON completo
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    # Salva apenas o TOP 3
    top3 = df_paraiba.head(3).to_dict(orient="records")
    with open(TOP3_FILE, "w", encoding="utf-8") as f:
        json.dump(top3, f, ensure_ascii=False, indent=4)

    print(f"✅ Arquivo JSON da Paraíba gerado em {OUTPUT_FILE}")
    print(f"🏆 Ranking TOP 3 IEs gerado em {TOP3_FILE}")

if __name__ == "__main__":
    gerar_json()