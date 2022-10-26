import numpy as np
import pandas as pd


def generate_balance_shops(
        sales: pd.DataFrame
):
    grouped: pd.Series = sales.groupby(['shop_id', 'date', 'product_id'])['quantity'].mean().reset_index()
    base_line: pd.DataFrame = grouped.groupby(
        ['shop_id', 'product_id']
    )['quantity'].max().reset_index()
    base_line['quantity'] = (base_line['quantity'] * (np.random.random(base_line.shape[0]) * 0.2 + 1)).astype(int)
    base_line.rename(columns={'quantity': 'balance'}, inplace=True)

    merged = pd.merge(grouped, base_line, on=['shop_id', 'product_id'])
    merged['balance'] = np.abs(merged['balance'] * (np.random.uniform(-0.2, 0.2, merged.shape[0]) + 1)).astype(int)
    merged.drop(columns='quantity', inplace=True)
    merged.index += 1
    return merged
