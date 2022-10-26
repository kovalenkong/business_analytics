import os
from os.path import join

import pandas as pd
from dotenv import load_dotenv

from _common import setup_logger
from generator import (generate_balance_dc, generate_balance_shops,
                       generate_balance_storages,
                       generate_distribution_centers, generate_products,
                       generate_sales, generate_shop_assortment,
                       generate_shops, generate_storages, generate_suppliers)
from generator.utils import P, parse_geo_points, parse_point

load_dotenv()

logger = setup_logger(__name__)

N_SUPPLIERS = int(os.getenv('N_SUPPLIERS', 20))
N_DC = int(os.getenv('N_DC', 3))
N_STORAGES = int(os.getenv('N_STORAGES', N_DC * 3))
N_SHOPS = int(os.getenv('N_SHOPS', N_STORAGES * 4))
N_PRODUCTS = int(os.getenv('N_PRODUCTS', 100))

GEO_DC = os.getenv('GEO_DC')
if GEO_DC is not None:
    GEO_DC = parse_geo_points(GEO_DC)
    assert len(GEO_DC) == N_DC, 'length GEO_DC should be the same as N_DC'

GEO_STORAGES = os.getenv('GEO_STORAGES')
if GEO_STORAGES:
    assert GEO_DC is not None, 'if you set GEO_STORAGES, then GEO_DC should be set too'
    GEO_STORAGES = parse_geo_points(GEO_STORAGES)
    assert len(GEO_STORAGES) == len(GEO_DC), 'length GEO_STORAGES should be the same as length GEO_DC'

GEO_CENTER = os.getenv('GEO_CENTER')
if GEO_CENTER:
    assert GEO_STORAGES is not None, 'if you set GEO_CENTER, then GEO_STORAGES should be set too'
    GEO_CENTER = parse_point(GEO_CENTER)


def generate_data(
        from_date: str,
        to_date: str,
        output_dir: str
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    logger.debug('generate suppliers')
    suppliers = generate_suppliers(N_SUPPLIERS, n_delivery_days=(1, 7), n_notify_days=(1, 3))
    to_csv(suppliers, join(output_dir, 'suppliers.csv'))

    logger.debug('generate distribution centers')
    distribution_centers = generate_distribution_centers(N_DC, GEO_DC)
    to_csv(distribution_centers, join(output_dir, 'distribution_centers.csv'), sep=';')

    logger.debug('generate storages')
    storages = generate_storages(N_STORAGES, dc=distribution_centers, geo_storages=GEO_STORAGES)
    to_csv(storages, join(output_dir, 'storages.csv'), sep=';')

    logger.debug('generate shops')
    shops = generate_shops(N_SHOPS, storages=storages, geo_center=GEO_CENTER)
    to_csv(shops, join(output_dir, 'shops.csv'), sep=';')

    logger.debug('generate products')
    products = generate_products(N_PRODUCTS, suppliers.index, p=P.RANDOM)
    to_csv(products, join(output_dir, 'products.csv'), sep=';')

    logger.debug('generate shop assortment')
    shop_assortment = generate_shop_assortment(shops, products, part=(0.8, 0.95))
    to_csv(shop_assortment, join(output_dir, 'shop_assortment.csv'), use_index=False)

    logger.debug('generate sales')
    sales = generate_sales(from_date, to_date, shops, shop_assortment)
    to_csv(sales, join(output_dir, 'sales.csv'))

    logger.debug('generate balance shops')
    balance_shops = generate_balance_shops(sales)
    to_csv(balance_shops, join(output_dir, 'balance_shops.csv'))

    logger.debug('generate balance for storages')
    balance_storages = generate_balance_storages(sales, shops)
    to_csv(balance_storages, join(output_dir, 'balance_storages.csv'))

    logger.debug('generate balance for distribution centers')
    balance_dc = generate_balance_dc(sales, shops, storages, products, suppliers)
    to_csv(balance_dc, join(output_dir, 'balance_dc.csv'))


def to_csv(
        df: pd.DataFrame,
        filename: str,
        use_index: bool = True,
        index_col: str = 'id',
        sep: str = ','
):
    df.to_csv(filename, index=use_index, index_label=index_col, sep=sep)


if __name__ == '__main__':
    DATE_FROM = os.getenv('DATE_FROM')
    DATE_TO = os.getenv('DATE_TO')
    DATA_DIR = os.getenv('DATA_DIR', 'data')
    assert DATE_FROM is not None, 'should set "DATE_FROM" env variable'
    assert DATE_TO is not None, 'should set "DATE_TO" env variable'
    generate_data(DATE_FROM, DATE_TO, DATA_DIR)
