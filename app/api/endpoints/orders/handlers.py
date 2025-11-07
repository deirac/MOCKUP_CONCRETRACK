from fastapi import Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from app.services.orders import OrdersService
from app.models.schemas.orders import CreateOrderRequest

async def orders_page(request: Request) -> HTMLResponse:
    """
    Serve the orders management page
    """
    try:
        templates = request.app.state.templates
        
        return templates.TemplateResponse(
            "orders.html", 
            {
                "request": request,
                "project_name": request.app.title,
                "version": request.app.version
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading orders page: {str(e)}"
        )

async def get_orders_data():
    """
    Get all orders data
    """
    try:
        orders = OrdersService.get_all_orders()
        return {
            "success": True,
            "data": orders,
            "total": len(orders)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading orders data: {str(e)}"
        )

async def get_order_details(order_id: int):
    """
    Get specific order details
    """
    try:
        order = OrdersService.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {
            "success": True,
            "data": order
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error loading order details: {str(e)}"
        )

async def create_order(order_data: CreateOrderRequest):
    """
    Create a new order
    """
    try:
        order = OrdersService.create_order(order_data)
        return {
            "success": True,
            "message": "Order created successfully",
            "data": order
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error creating order: {str(e)}"
        )

async def update_order_status(order_id: int, status: str = Form(...)):
    """
    Update order status
    """
    try:
        success = OrdersService.update_order_status(order_id, status)
        if not success:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {
            "success": True,
            "message": f"Order status updated to {status}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error updating order status: {str(e)}"
        )