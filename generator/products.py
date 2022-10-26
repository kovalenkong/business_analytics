from typing import List

import numpy as np
import pandas as pd

from .utils import P, choose_random


def generate_products(
        n: int,
        supplier_ids: List[int],
        p: P = P.NORMAL
) -> pd.DataFrame:
    products = pd.read_csv('generator/perekrestok/products.csv')[['title', 'price']]
    products = products[(products['title'].notna()) & (products['price'].notna())][:n]
    products['title'].replace(';', ',', inplace=True)
    products['price'] /= 100
    suppliers = choose_random(supplier_ids, 100, p)
    df = pd.DataFrame({
        'name': products['title'],
        'price': products['price'],
        'supplier_id': suppliers,
    })
    df.index = np.arange(1, df.shape[0] + 1)
    return df
