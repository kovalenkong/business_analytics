from typing import List

import numpy as np
import pandas as pd


def generate_distribution_center_name(center_number: int) -> str:
    return f'РЦ №{center_number}'


def generate_distribution_centers(n: int, geo_dc: List[List[float]] = None) -> pd.DataFrame:
    df = pd.DataFrame({
        'name': [generate_distribution_center_name(i + 1) for i in range(n)]
    })
    if geo_dc is not None:

        df['location'] = None
        for i, j in enumerate(geo_dc):
            df.loc[i, 'location'] = str(j)

    df.index = np.arange(1, n + 1)
    return df
