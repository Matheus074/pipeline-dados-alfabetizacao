"""
Funções utilitárias de leitura e escrita no Cloud Storage.

O bucket é escolhido pelo prefixo do caminho:
- "bronze/..." -> bucket da camada Bronze
- "silver/..." -> bucket da camada Silver
"""

import pandas as pd

from config import GCS_BUCKET_BRONZE
from config import GCS_BUCKET_SILVER


def _bucket_do_caminho(caminho):
    """
    Retorna o bucket correto de acordo com a camada do caminho.
    """

    if caminho.startswith("silver/"):
        return GCS_BUCKET_SILVER

    return GCS_BUCKET_BRONZE


def ler_parquet(caminho):
    """
    Lê um parquet do Cloud Storage, no bucket da camada indicada pelo caminho.
    """

    return pd.read_parquet(
        f"gs://{_bucket_do_caminho(caminho)}/{caminho}",
        engine="pyarrow"
    )


def salvar_parquet(df, caminho):
    """
    Salva um dataframe na camada Silver.
    """

    destino = f"gs://{GCS_BUCKET_SILVER}/{caminho}"

    df.to_parquet(
        destino,
        index=False,
        engine="pyarrow"
    )

    print(f"Arquivo salvo em {destino}")
