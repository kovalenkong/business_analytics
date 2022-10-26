from typing import List

import numpy as np
import pandas as pd

from .utils import P, choose_random


def generate_shops(
        n: int,
        storages: pd.DataFrame,
        p: P = P.NORMAL,
        geo_center: List[float] = None
) -> pd.DataFrame:
    storage_ids = storages.index
    df = pd.DataFrame({
        'name': [f'Shop №{i + 1}' for i in range(n)],
        'storage_id': choose_random(storage_ids, n, p),
    })
    if geo_center:
        df['location'] = None
        points = np.hstack(
            (np.repeat([geo_center], storages.shape[0], axis=0), storages['location'].str.extract('(\d+.?\d+)\D+(\d+.?\d+)').astype(float).values)
        )
        for shop_id in df.index:
            points_between = points[df.loc[shop_id]['storage_id'] - 1]
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
            df.loc[shop_id, 'location'] = str(loc)

    df.index = np.arange(1, n + 1)
    return df
