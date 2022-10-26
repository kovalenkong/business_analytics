from typing import List

import numpy as np
import pandas as pd

from .utils import P, choose_random


def generate_storages(
        n: int,
        dc: pd.DataFrame,
        p: P = P.NORMAL,
        geo_storages: List[List[float]] = None
) -> pd.DataFrame:
    dc_ids = dc.index
    df = pd.DataFrame({
        'name': [f'Storage №{i + 1}' for i in range(n)],
        'dc_id': choose_random(dc_ids, n, p),
    })

    if geo_storages is not None:
        df['location'] = None
        points = np.hstack(
            (geo_storages, dc['location'].str.extract('(\d+.?\d+)\D+(\d+.?\d+)').astype(float).values)
        )
        for storage_id in df.index:
            points_between = points[df.loc[storage_id]['dc_id'] - 1]
            loc = [
                np.round(np.random.uniform(
                    min((points_between[0], points_between[2])),
                    max((points_between[0], points_between[2]))
                ), 6),
                np.round(np.random.uniform(
                    min((points_between[1], points_between[3])),
                    max((points_between[1], points_between[3]))
                ), 6),
            ]
            df.loc[storage_id, 'location'] = str(loc)

    df.index = np.arange(1, n + 1)
    return df
