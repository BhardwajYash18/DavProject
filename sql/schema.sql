-- SQLite Relational Schema for Customer Shopping Behaviour Analytics
-- Designed with normalized entities: Customers and Orders

PRAGMA foreign_keys = ON;

-- Table: customers
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL CHECK(age >= 10 AND age <= 120),
    gender TEXT NOT NULL CHECK(gender IN ('Male', 'Female')),
    location TEXT NOT NULL,
    age_group TEXT NOT NULL CHECK(age_group IN ('Young-adult', 'Adult', 'Middle-aged', 'Senior')),
    subscription_status TEXT NOT NULL CHECK(subscription_status IN ('Yes', 'No')),
    previous_purchases INTEGER NOT NULL CHECK(previous_purchases >= 0),
    frequency_of_purchases TEXT NOT NULL,
    purchase_frequency_days INTEGER NOT NULL
);

-- Table: orders
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    item_purchased TEXT NOT NULL,
    category TEXT NOT NULL,
    purchase_amount REAL NOT NULL CHECK(purchase_amount > 0),
    size TEXT NOT NULL,
    color TEXT NOT NULL,
    season TEXT NOT NULL,
    review_rating REAL NOT NULL CHECK(review_rating >= 1.0 AND review_rating <= 5.0),
    shipping_type TEXT NOT NULL,
    discount_applied TEXT NOT NULL CHECK(discount_applied IN ('Yes', 'No')),
    payment_method TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

-- Indexing for optimized query performance
CREATE INDEX IF NOT EXISTS idx_customers_gender ON customers(gender);
CREATE INDEX IF NOT EXISTS idx_customers_age_group ON customers(age_group);
CREATE INDEX IF NOT EXISTS idx_customers_subscription ON customers(subscription_status);
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_category ON orders(category);
CREATE INDEX IF NOT EXISTS idx_orders_item ON orders(item_purchased);

-- View: customer_shopping_view (Combines normalized tables for seamless analytics)
CREATE VIEW IF NOT EXISTS customer_shopping_view AS
SELECT 
    c.customer_id,
    c.age,
    c.gender,
    c.location,
    c.age_group,
    c.subscription_status,
    c.previous_purchases,
    c.frequency_of_purchases,
    c.purchase_frequency_days,
    o.order_id,
    o.item_purchased,
    o.category,
    o.purchase_amount,
    o.size,
    o.color,
    o.season,
    o.review_rating,
    o.shipping_type,
    o.discount_applied,
    o.payment_method
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

