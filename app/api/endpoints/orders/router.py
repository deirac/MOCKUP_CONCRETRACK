from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.api.endpoints.orders.handlers import (
    orders_page,
    get_orders_data,
    get_order_details,
    create_order,
    update_order_status
)

router = APIRouter()

# Register routes
router.get("/orders", response_class=HTMLResponse, summary="Orders Page")(orders_page)
router.get("/api/orders", summary="Get orders data")(get_orders_data)
router.get("/api/orders/{order_id}", summary="Get order details")(get_order_details)
router.post("/api/orders", summary="Create new order")(create_order)
router.put("/api/orders/{order_id}/status", summary="Update order status")(update_order_status)