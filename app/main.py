from fastapi import FastAPI
from crud import (
    create_order, get_orders, update_order_status, delete_order,
    add_inventory_item, get_inventory, update_stock, delete_inventory_item,
    create_shipment, get_shipments, update_shipment_status, delete_shipment,
    update_shipment_status_from_webhook, process_return,
    plan_route, assign_carrier, calculate_freight,
    create_warehouse, get_all_warehouses, get_inventory_by_warehouse,
    add_or_update_inventory, handle_return
)

app = FastAPI()

# Order Endpoints
@app.post("/orders/")
def add_order(order):
    return create_order(order)

@app.get("/orders/")
def fetch_orders():
    return get_orders()

@app.put("/orders/{order_id}")
def modify_order_status(order_id, status):
    return update_order_status(order_id, status)

@app.delete("/orders/{order_id}")
def remove_order(order_id):
    return delete_order(order_id)

# Inventory Endpoints
@app.post("/inventory/")
def add_inventory(item):
    return add_inventory_item(item)

@app.get("/inventory/")
def fetch_inventory():
    return get_inventory()

@app.put("/inventory/{item_id}")
def modify_stock(item_id, stock_level):
    return update_stock(item_id, stock_level)

@app.delete("/inventory/{item_id}")
def remove_inventory(item_id):
    return delete_inventory_item(item_id)

# Shipments Endpoints
@app.post("/shipments/")
def add_shipment(shipment):
    return create_shipment(shipment)

@app.get("/shipments/")
def fetch_shipments():
    return get_shipments()

@app.put("/shipments/{shipment_id}")
def modify_shipment_status(shipment_id, status):
    return update_shipment_status(shipment_id, status)

@app.delete("/shipments/{shipment_id}")
def remove_shipment(shipment_id):
    return delete_shipment(shipment_id)

@app.post("/webhook/shipment-status/")
def webhook_shipment_status(data):
    order_id = data.get("order_id")
    new_status = data.get("status")

    if not order_id or not new_status:
        return {"error": "order_id and status are required"}

    return update_shipment_status_from_webhook(order_id, new_status)

@app.post("/orders/{order_id}/return")
def return_order(order_id):
    return process_return(order_id)

@app.post("/tms/plan-route/{shipment_id}")
def plan_route_for_shipment(shipment_id):
    return plan_route(shipment_id)

@app.post("/tms/assign-carrier/{shipment_id}")
def assign_carrier_to_shipment(shipment_id):
    return assign_carrier(shipment_id)

@app.post("/tms/freight/{shipment_id}")
def calculate_freight_for_shipment(shipment_id):
    return calculate_freight(shipment_id)

@app.post("/dms/warehouse")
def add_warehouse(warehouse):
    return create_warehouse(warehouse)

@app.get("/dms/warehouse")
def fetch_warehouses():
    return get_all_warehouses()

@app.post("/dms/inventory")
def add_update_inventory(item):
    return add_or_update_inventory(item)

@app.get("/dms/inventory/{warehouse_id}")
def view_inventory(warehouse_id):
    return get_inventory_by_warehouse(warehouse_id)

@app.post("/dms/returns")
def process_return(return_data):
    return handle_return(return_data)
