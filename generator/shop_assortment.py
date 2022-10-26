from typing import Tuple, Union

import numpy as np
import pandas as pd


def generate_shop_assortment(
        shops: pd.DataFrame,
        products: pd.DataFrame,
        part: Union[float, Tuple[float, float]]
) -> pd.DataFrame:
    df = pd.DataFrame(columns=['shop_id', 'product_id'])
    for shop_id in shops.index:
        if isinstance(part, float):
            size = int(products.shape[0] * part)
        else:
            size = int(products.shape[0] * np.random.uniform(*part))
        product_ids = np.random.choice(products.index, size, replace=False)
        df = pd.concat((
            df,
            pd.DataFrame({
                'shop_id': shop_id,
                'product_id': product_ids,
            })
        ))
    return df
