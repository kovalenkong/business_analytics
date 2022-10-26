import os
from io import StringIO
from os.path import join

import pandas as pd
import psycopg2
from dotenv import load_dotenv

from _common import setup_logger

load_dotenv()

logger = setup_logger(__name__)

PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_DB = os.getenv('PG_DB')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')


def migrate(data_dir: str):
    logger.debug('connecting to database')
    conn = psycopg2.connect(f'dbname={PG_DB} user={PG_USER} host={PG_HOST} port={PG_PORT} password={PG_PASSWORD}')
    logger.debug('successfully connected')
    cursor = conn.cursor()
    with open('migrations/setup.sql') as f:
        logger.debug('create tables')
        cursor.execute(f.read())

    logger.debug('applying migrations to suppliers')
    suppliers = pd.read_csv(join(data_dir, 'suppliers.csv'), index_col='id')
    copy_table(cursor, suppliers, 'suppliers')

    logger.debug('applying migrations to distribution_centers')
    distribution_centers = pd.read_csv(join(data_dir, 'distribution_centers.csv'), index_col='id', sep=';')
    copy_table(cursor, distribution_centers, 'distribution_centers', csv_sep=';')

    logger.debug('applying migrations to storages')
    storages = pd.read_csv(join(data_dir, 'storages.csv'), index_col='id', sep=';')
    copy_table(cursor, storages, 'storages', csv_sep=';')

    logger.debug('applying migrations to shops')
    shops = pd.read_csv(join(data_dir, 'shops.csv'), index_col='id', sep=';')
    copy_table(cursor, shops, 'shops', csv_sep=';')

    logger.debug('applying migrations to products')
    products = pd.read_csv(join(data_dir, 'products.csv'), sep=';', index_col='id')
    copy_table(cursor, products, 'products', csv_sep=';')

    logger.debug('applying migrations to shop_assortment')
    shop_assortment = pd.read_csv(join(data_dir, 'shop_assortment.csv'))
    copy_table(cursor, shop_assortment, 'shop_assortment', use_index=False)

    logger.debug('applying migrations to sales')
    sales = pd.read_csv(join(data_dir, 'sales.csv'), index_col='id')
    copy_table(cursor, sales, 'sales')

    logger.debug('applying migrations to balance_shops')
    balance_shops = pd.read_csv(join(data_dir, 'balance_shops.csv'), index_col='id')
    copy_table(cursor, balance_shops, 'balance_shops')

    logger.debug('applying migrations to balance_storages')
    balance_storages = pd.read_csv(join(data_dir, 'balance_storages.csv'), index_col='id')
    copy_table(cursor, balance_storages, 'balance_storages')

    logger.debug('applying migrations to balance_dc')
    balance_dc = pd.read_csv(join(data_dir, 'balance_dc.csv'), index_col='id')
    copy_table(cursor, balance_dc, 'balance_dc')

    logger.debug('committing')
    conn.commit()
    logger.debug('successfully committed')


def copy_table(
        cursor,
        df: pd.DataFrame,
        table_name: str,
        csv_sep: str = ',',
        use_index: bool = True,
        index_col: str = 'id'
):
    b = StringIO()
    df.to_csv(b, header=False, index=use_index, index_label=index_col, sep=csv_sep)  # noqa
    b.seek(0)
    columns = df.columns.tolist()
    if use_index:
        columns.insert(0, index_col)
    cursor.copy_from(b, table_name, sep=csv_sep, columns=columns)


if __name__ == '__main__':
    DATA_DIR = os.getenv('DATA_DIR', 'data')
    migrate(DATA_DIR)
