CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    item TEXT NOT NULL,
    amount_cents INT NOT NULL,
    currency TEXT DEFAULT 'USD',
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS refunds (
    refund_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL REFERENCES orders(id),
    idempotency_key TEXT NOT NULL,
    amount_cents INT NOT NULL CHECK (amount_cents > 0),
    status TEXT NOT NULL DEFAULT 'COMPLETED',
    created_at TIMESTAMPTZ DEFAULT now()
)
CREATE INDEX IF NOT EXISTS idx_refunds_order_id ON refunds(order_id);


INSERT INTO orders (customer_id, item, amount_cents, status) VALUES
    (101, 'Keyboard', 7500, 'PAID'),
    (102, 'Mouse', 2500, 'SHIPPED'),
    (103, 'Monitor', 30000, 'DELIVERED');
