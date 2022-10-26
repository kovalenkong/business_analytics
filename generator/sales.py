import numpy as np
import pandas as pd


def _random_line(n: int):
    a, b = np.random.random(2)
    line = np.linspace(a, b, num=n)
    if np.random.random() > 0.5:
        return np.abs(np.sin(line))
    return np.abs(np.cos(line))


def generate_sales(
        date_from: str,
        date_to: str,
        shops: pd.DataFrame,
        shop_assortment: pd.DataFrame,
) -> pd.DataFrame:
    df = pd.DataFrame(columns=['date', 'shop_id', 'product_id', 'quantity'])
    date_range = pd.date_range(date_from, date_to, freq='D')
    period = date_range.size
    for shop_id in shops.index:
        shop_products_ids = shop_assortment[shop_assortment['shop_id'] == shop_id]['product_id']
        for product_id in shop_products_ids:
            sales_from = np.random.randint(500, 1000)
            base_consumption = np.random.randint(sales_from, sales_from * 1.1, period)
            consumption = (base_consumption + base_consumption * _random_line(period)).astype(int)
            df = pd.concat((
                df,
                pd.DataFrame({
                    'date': date_range,
                    'shop_id': shop_id,
                    'product_id': product_id,
                    'quantity': consumption,
                })
            ))
    df.index = np.arange(1, df.shape[0] + 1)
    return df
