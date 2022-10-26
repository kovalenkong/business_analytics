import numpy as np
import pandas as pd


def generate_balance_dc(
        sales: pd.DataFrame,
        shops: pd.DataFrame,
        storages: pd.DataFrame,
        products: pd.DataFrame,
        suppliers: pd.DataFrame,
        add_zero_balances: bool = False
):
    merged = pd.merge(
        sales,
        shops.reset_index(names=['id'])[['id', 'storage_id']].rename(columns={'id': 'shop_id'}),
        on='shop_id'
    )
    merged = pd.merge(
        merged,
        storages.reset_index(names=['id'])[['id', 'dc_id']].rename(columns={'id': 'storage_id'}),
        on='storage_id'
    ).groupby(['dc_id', 'product_id', 'date'])['quantity'].sum().reset_index()

    product_info = pd.merge(
        products.reset_index(names=['id'])[['id', 'supplier_id']],
        suppliers.reset_index(names=['id'])[['id', 'delivery_day']].rename(columns={'id': 'supplier_id'}),
        on='supplier_id'
    ).rename(columns={'id': 'product_id'})

    merged = pd.merge(
        merged,
        product_info[['product_id', 'delivery_day']],
        on='product_id'
    ).sort_values('date')
    merged['weekday'] = merged['date'].astype('datetime64[ns]').dt.weekday + 1

    values = []
    for (dc_id, product_id), group in merged.groupby(['dc_id', 'product_id']):
        mean_quantity = group['quantity'].mean()
        for i, row in group.iterrows():
            weekday, delivery_day = row[['weekday', 'delivery_day']]
            values.append([
                row['date'],
                dc_id,
                product_id,
                np.abs(mean_quantity * (7 - (weekday - delivery_day) % 7) * np.random.uniform(1, 1.1)).astype(int),
            ])
    df = pd.DataFrame(
        values,
        columns=['date', 'dc_id', 'product_id', 'balance']
    )
    df.index += 1
    if add_zero_balances:
        df['date'] = df['date'].astype('datetime64[ns]', copy=False)
        for dc_id, group in df[df['date'] <= df['date'].mean()].sort_values('balance').groupby('dc_id')[
            ['product_id', 'balance']]:
            for_zero = group.iloc[:int(group.shape[0] * np.random.uniform(0.02, 0.03))]
            df.loc[for_zero.index, 'balance'] = 0

    return df
