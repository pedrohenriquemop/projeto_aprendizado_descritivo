import argparse
import unicodedata
import pandas as pd
import numpy as np
import pysubgroup as ps
from dataclasses import dataclass
from typing import List, Tuple

# ==========================================
# CONFIGURATION & DATA STRUCTURES
# ==========================================


@dataclass
class MinerConfig:
    """Stores the hyperparameters and configuration for the mining task."""

    datasets: List[str]
    depth: int
    result_size: int
    candidate: str  # <--- Novo campo para o candidato
    panorama_path: str = "dados_municipios_panorama.csv"
    elections_path: str = "votacao_candidato-municipio_presidente_2022_-1.csv"
    birthdays_path: str = "aniversariantes.csv"


# ==========================================
# DATA PROCESSING FUNCTIONS
# ==========================================


def standardize_text(text: str) -> str:
    """Removes accents and capitalizes text to ensure robust table merging."""
    if pd.isna(text):
        return text
    text = str(text).upper().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn"
    )


def process_panorama(filepath: str) -> pd.DataFrame:
    print("[*] Processing Panorama dataset...")
    df = pd.read_csv(filepath, low_memory=False)
    df.replace(["-", "Sem dados"], np.nan, inplace=True)

    numeric_cols = [
        "Densidade demográfica",
        "PIB per capita",
        "Índice de Desenvolvimento Humano Municipal (IDHM)",
        "Mortalidade Infantil",
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Índice de Desenvolvimento Humano Municipal (IDHM)" in df.columns:
        df["Target_IDHM_Alto"] = (
            df["Índice de Desenvolvimento Humano Municipal (IDHM)"] >= 0.700
        )

    col_muni = "municipio" if "municipio" in df.columns else df.columns[0]
    df["nm_municipio_padrao"] = df[col_muni].apply(standardize_text)

    keep_cols = numeric_cols + [
        "nm_municipio_padrao",
        "Bioma predominante",
        "Hierarquia urbana",
        "Target_IDHM_Alto",
    ]
    return df[[c for c in keep_cols if c in df.columns]]


def process_elections(filepath: str, target_candidate: str) -> Tuple[pd.DataFrame, str]:
    print(f"[*] Processing Elections dataset... (Targeting: {target_candidate})")
    df = pd.read_csv(filepath, sep=";", encoding="latin1", low_memory=False)

    if "pc_votos_validos" in df.columns:
        df["pc_votos_validos"] = (
            df["pc_votos_validos"].astype(str).str.replace(",", ".").astype(float)
        )

    col_muni = "nm_municipio" if "nm_municipio" in df.columns else df.columns[1]
    df["nm_municipio_padrao"] = df[col_muni].apply(standardize_text)

    # Sort and drop duplicates to get the winning candidate per municipality
    winners = df.sort_values(
        ["sg_uf", "nm_municipio_padrao", "pc_votos_validos"],
        ascending=[True, True, False],
    )
    winners = winners.drop_duplicates(
        subset=["sg_uf", "nm_municipio_padrao"], keep="first"
    )

    winners = winners[["nm_municipio_padrao", "nm_urna_candidato", "pc_votos_validos"]]
    winners.rename(
        columns={
            "nm_urna_candidato": "Candidato_Vencedor",
            "pc_votos_validos": "Percentual_Vencedor",
        },
        inplace=True,
    )

    # Avaliação dinâmica do alvo com suporte a correspondência parcial (ex: "Bolsonaro" acha "Jair Bolsonaro")
    candidate_std = standardize_text(target_candidate)
    target_col_name = f"Target_Venceu_{candidate_std.replace(' ', '_')}"

    # Padroniza a coluna de vencedores para garantir o match
    winners["Candidato_Vencedor_Padrao"] = winners["Candidato_Vencedor"].apply(
        standardize_text
    )
    winners[target_col_name] = winners["Candidato_Vencedor_Padrao"].str.contains(
        candidate_std, na=False
    )
    winners.drop(columns=["Candidato_Vencedor_Padrao"], inplace=True)

    return winners, target_col_name


def process_birthdays(filepath: str) -> pd.DataFrame:
    print("[*] Processing Birthdays dataset...")
    try:
        df = pd.read_csv(filepath, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="latin1", low_memory=False)

    col_muni = "municipio" if "municipio" in df.columns else df.columns[0]
    df["nm_municipio_padrao"] = df[col_muni].apply(standardize_text)

    keep_cols = [
        c for c in df.columns if c.lower() not in ["uf", "estado", col_muni.lower()]
    ]
    return df[keep_cols]


def merge_datasets(config: MinerConfig) -> Tuple[pd.DataFrame, str]:
    """Dynamically loads and merges the user-selected datasets."""
    dataframes = []
    target_col = ""

    if "panorama" in config.datasets:
        dataframes.append(process_panorama(config.panorama_path))
        target_col = "Target_IDHM_Alto"

    if "elections" in config.datasets:
        df_elec, elec_target = process_elections(
            config.elections_path, config.candidate
        )
        dataframes.append(df_elec)
        target_col = elec_target  # Overrides panorama target

    if "birthdays" in config.datasets:
        dataframes.append(process_birthdays(config.birthdays_path))

    print("[*] Merging datasets...")
    df_final = dataframes[0]
    for df in dataframes[1:]:
        df_final = pd.merge(df_final, df, on="nm_municipio_padrao", how="inner")

    if target_col in df_final.columns:
        df_final.dropna(subset=[target_col], inplace=True)

    print(f"[+] Final dataset shape: {df_final.shape}")
    return df_final, target_col


# ==========================================
# MINING ALGORITHM
# ==========================================


def mine_subgroups(df: pd.DataFrame, target_col: str, config: MinerConfig):
    print(f"\n[*] Starting Subgroup Discovery. Target: {target_col} == True")

    target = ps.BinaryTarget(target_col, True)

    ignore_cols = [target_col, "nm_municipio_padrao", "Candidato_Vencedor"]
    searchspace = ps.create_selectors(
        df, ignore=[c for c in ignore_cols if c in df.columns]
    )

    task = ps.SubgroupDiscoveryTask(
        df,
        target,
        searchspace,
        result_set_size=config.result_size,
        depth=config.depth,
        qf=ps.WRAccQF(),
    )

    result = ps.BeamSearch().execute(task)
    df_results = result.to_dataframe()

    print("\n" + "=" * 70)
    print(f" TOP {config.result_size} SUBGROUPS FOUND")
    print("=" * 70)

    for i, row in df_results.iterrows():
        rule = row["subgroup"]
        size = row["size_sg"]
        positives = row["positives_sg"]
        confidence = (positives / size) * 100 if size > 0 else 0

        print(f"[{i+1}] Rule: {rule}")
        print(f"    - Covered municipalities: {size}")
        print(f"    - Target matches inside group: {positives} ({confidence:.1f}%)")
        print("-" * 70)


# ==========================================
# CLI ENTRY POINT
# ==========================================


def main():
    parser = argparse.ArgumentParser(
        description="Subgroup Discovery CLI for Brazilian Municipalities."
    )

    parser.add_argument(
        "--datasets",
        nargs="+",
        choices=["panorama", "elections", "birthdays"],
        default=["panorama", "elections"],
        help="Select at least 2 datasets to merge and analyze. Default: panorama elections",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        help="Maximum depth of the rules (number of conditions). Default: 2",
    )
    parser.add_argument(
        "--results",
        type=int,
        default=10,
        help="Number of top rules to output. Default: 10",
    )
    parser.add_argument(
        "--candidate",
        type=str,
        default="LULA",
        help="Candidate name to set as target (e.g., 'LULA', 'BOLSONARO'). Default: LULA",
    )

    args = parser.parse_args()

    if len(set(args.datasets)) < 2:
        print("[!] Error: You must select at least 2 different datasets to merge.")
        return

    config = MinerConfig(
        datasets=list(set(args.datasets)),
        depth=args.depth,
        result_size=args.results,
        candidate=args.candidate,
    )

    df_merged, target_column = merge_datasets(config)

    # ---> VERIFICAÇÃO CONTRA O ZERO-DIVISION ERROR <---
    if df_merged.empty:
        print("\n[!] CRITICAL ERROR: The merged dataset is empty (0 rows).")
        print(
            "    This usually means there was no intersection between the selected datasets,"
        )
        print(
            "    or the selected candidate did not win in any of the mapped municipalities."
        )
        print("    Mining aborted to prevent ZeroDivisionError.")
        return

    mine_subgroups(df_merged, target_column, config)


if __name__ == "__main__":
    main()
