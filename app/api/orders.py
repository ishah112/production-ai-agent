from fastapi import APIRouter, HTTPException
from app.db.orders import fetch_order_status, process_refund

router = APIRouter()

@router.get("/orders/{order_id}")
def get_order(order_id: int):
    order = fetch_order_status(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/orders/{order_id}/refund")
def refund_order(order_id):
    refund = process_refund(order_id)
    if refund is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return refund