from .connection import get_connection 
from psycopg.rows import dict_row 

def fetch_order_status(order_id: int):
    # get connection
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as curr:
            # fetch order
            curr.execute("SELECT id, customer_id, item, amount_cents, currency, status, created_at FROM orders WHERE id = %s", (order_id,))
            return curr.fetchone()

# check the refund status first
# dont retry if already refunded
# only execute if not done before        
def process_refund(order_id: int):
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as curr:
            # 1. Check the current status first, and lock the row
            curr.execute("SELECT * FROM orders where id=%s", (order_id,))
            order = curr.fetchone()
            
            # 2. Already refunded? Don't retry — return the existing refund
            if order["status"] == "REFUNDED":
                curr.execute("SELECT * FROM refunds where order_id=%s", (order_id,))
                return curr.fetchone()

            # 3. Only execute if not done before
            curr.execute(
                "INSERT INTO refunds (order_id, idempotency_key, amount_cents, status) "
                "VALUES (%s, %s, %s, 'COMPLETED') RETURNING *",
                (order_id, f"refund-{order_id}", order["amount_cents"]),
            )
            refund = curr.fetchone()
            curr.execute("UPDATE orders SET status = 'REFUNDED' WHERE id = %s", (order_id,))
            conn.commit()
            return refund


