DROP TABLE IF EXISTS suppliers, distribution_centers, storages, shops, products, shop_assortment, orders_to_suppliers, sales, balance_dc, balance_storages, balance_shops CASCADE;

CREATE TABLE suppliers
(
    id           SERIAL PRIMARY KEY,
    name         VARCHAR(256) NOT NULL,
    delivery_day SMALLINT     NOT NULL, -- день недели от 1 (пн) до 7 (вс) по которым поставщик осуществляет поставки
    notify_days  INTEGER      NOT NULL, -- предупредить не раньше чем за N дней до поставки

    CONSTRAINT correct_delivery_day CHECK ( delivery_day BETWEEN 1 AND 7),
    CONSTRAINT positive_notify_days CHECK (notify_days >= 0)
);

CREATE TABLE distribution_centers
(
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(256) NOT NULL,
    location VARCHAR NULL
);

CREATE TABLE storages
(
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(256) NOT NULL,
    dc_id    INTEGER      NOT NULL REFERENCES distribution_centers (id) ON DELETE RESTRICT,
    location VARCHAR NULL
);

CREATE TABLE shops
(
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(256) NOT NULL,
    storage_id INTEGER      NOT NULL REFERENCES storages (id) ON DELETE RESTRICT,
    location   VARCHAR NULL
);

CREATE TABLE products
(
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(256) NOT NULL,
    supplier_id INTEGER      NOT NULL REFERENCES suppliers (id) ON DELETE RESTRICT,
    price DECIMAL NULL
);

CREATE TABLE shop_assortment
(
    shop_id    INTEGER NOT NULL REFERENCES shops (id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    is_active  BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX shop_assortment_idx ON shop_assortment (shop_id, product_id);

CREATE TABLE orders_to_suppliers -- эта таблица будет заполняться с помощью Loginom
(
    id                   SERIAL PRIMARY KEY,
    date_created         DATE    NOT NULL,
    expected_date_income DATE    NOT NULL,
    dc_id                INTEGER NOT NULL REFERENCES distribution_centers (id) ON DELETE CASCADE,
    supplier_id          INTEGER REFERENCES suppliers (id) ON DELETE SET NULL,
    product_id           INTEGER REFERENCES products (id) ON DELETE SET NULL,
    quantity             DECIMAL NOT NULL,

    CONSTRAINT positive_quantity CHECK (quantity > 0),
    CONSTRAINT expected_date_income_gte_date_created CHECK (expected_date_income >= date_created),
    UNIQUE (date_created, dc_id, supplier_id, product_id)
);

CREATE TABLE sales
(
    id         SERIAL PRIMARY KEY,
    date       DATE    NOT NULL,
    shop_id    INTEGER NOT NULL REFERENCES shops (id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    quantity   DECIMAL NOT NULL,

    CONSTRAINT positive_quantity CHECK (quantity > 0),
    UNIQUE (date, shop_id, product_id)
);

CREATE TABLE balance_dc
(
    id         SERIAL PRIMARY KEY,
    date       DATE    NOT NULL,
    dc_id      INTEGER NOT NULL REFERENCES distribution_centers (id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    balance    DECIMAL NOT NULL,

    UNIQUE (date, dc_id, product_id)
);

CREATE TABLE balance_storages
(
    id         SERIAL PRIMARY KEY,
    date       DATE    NOT NULL,
    storage_id INTEGER NOT NULL REFERENCES storages (id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    balance    DECIMAL NOT NULL,

    UNIQUE (date, storage_id, product_id)
);

CREATE TABLE balance_shops
(
    id         SERIAL PRIMARY KEY,
    date       DATE    NOT NULL,
    shop_id    INTEGER NOT NULL REFERENCES shops (id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products (id) ON DELETE CASCADE,
    balance    DECIMAL NOT NULL
);