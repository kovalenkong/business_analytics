import random
from typing import Tuple, Union

import numpy as np
import pandas as pd

COMPANY_TYPES = [
    'ООО',
    'ЗАО',
    'ОАО',
    'ИП',
]


def generate_supplier_name(supplier_number: int) -> str:
    return f'{random.choice(COMPANY_TYPES)} Supplier {supplier_number}'


def generate_suppliers(
        n: int,
        n_delivery_days: Union[int, Tuple[int, int]],
        n_notify_days: Union[int, Tuple[int, int]]
) -> pd.DataFrame:
    suppliers = [generate_supplier_name(i + 1) for i in range(n)]

    if isinstance(n_delivery_days, int):
        delivery_days = np.array([n_delivery_days] * n)
    else:
        delivery_days = np.random.randint(n_delivery_days[0], n_delivery_days[1] + 1, n)

    if isinstance(n_notify_days, int):
        notify_days = np.array([n_notify_days] * n)
    else:
        notify_days = np.random.randint(n_notify_days[0], n_notify_days[1] + 1, n)
    return pd.DataFrame({
        'name': suppliers,
        'delivery_day': delivery_days,
        'notify_days': notify_days,
    }, index=np.arange(1, n + 1))
