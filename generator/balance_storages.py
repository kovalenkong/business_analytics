import numpy as np
import pandas as pd


def generate_balance_storages(
        sales: pd.DataFrame,
        shops: pd.DataFrame
) -> pd.DataFrame:
    df = pd.DataFrame(columns=['date', 'storage_id', 'product_id', 'balance'])
    for storage_id, group in shops.groupby('storage_id'):
        shop_ids = group.index

        grouped_sales = sales[
            sales['shop_id'].isin(shop_ids)
        ].groupby(['product_id', 'date'])['quantity'].sum().reset_index().sort_values('date')

        for product_id, sub_group in grouped_sales.groupby('product_id'):
            quantity: pd.Series = sub_group['quantity']
            shipment_every = np.random.randint(2, 5)
            balance = np.zeros(quantity.size)
            for i in range(quantity.size):
                i_from, i_to = i, i + shipment_every - i % shipment_every
                value = quantity.iloc[i_from:i_to].sum()
                balance[i] = value
            df = pd.concat((
                df,
                pd.DataFrame({
                    'date': sub_group['date'],
                    'storage_id': storage_id,
                    'product_id': product_id,
                    'balance': np.abs(balance * np.random.uniform(1, 1.1)).astype(int),
                })
            ))
    df.index = np.arange(1, df.shape[0] + 1)
    return df
