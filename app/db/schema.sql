CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    item TEXT NOT NULL,
    amount_cents INT NOT NULL,
    currency TEXT DEFAULT 'USD',
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO orders (customer_id, item, amount_cents, status) VALUES
    (101, 'Keyboard', 7500, 'PAID'),
    (102, 'Mouse', 2500, 'SHIPPED'),
    (103, 'Monitor', 30000, 'DELIVERED');
