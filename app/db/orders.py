from .connection import get_connection 
from psycopg.rows import dict_row 

def fetch_order_status(order_id: int):
    # get connection
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as curr:
            # fetch order
            curr.execute("SELECT id, customer_id, item, amount_cents, currency, status, created_at FROM orders WHERE id = %s", (order_id,))
            return curr.fetchone()
        

    
