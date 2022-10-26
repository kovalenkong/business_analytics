import json
from typing import List

import pandas as pd
import requests

CATEGORIES = [
    113,
    148,
    100,
    708,
    187,
    205,
    782,
    132,
    54,
    217,
    79,
    224,
    168,
    74,
    157,
    108,
]


def _parse_page(data: dict) -> List[dict]:
    products = []
    category = data['content']['category']
    for item_group in data['content']['items']:
        sub_category = item_group['category']['title']
        print(sub_category)
        for product in item_group['products']:
            products.append({
                'category_id': category['id'],
                'category_title': category['title'],
                'category_slug': category['slug'],
                'sub_category': sub_category,
                'title': product['title'],
                'slug': product['masterData']['slug'],
                'unit': product['masterData']['unit'],
                'unit_name': product['masterData']['unitName'],
                'rating': product['rating'],
                'price': product['priceTag']['price']
            })
    return products


def parse_products(x5_auth_token: str) -> pd.DataFrame:
    all_products = []
    with requests.session() as s:
        for category in CATEGORIES:
            resp = s.get(
                f'https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/category/feed/{category}',
                headers={
                    'Authorization': x5_auth_token,
                }
            )
            all_products.extend(_parse_page(resp.json()))
    return pd.DataFrame.from_records(all_products)
