from database import get_db_connection
import random

def create_order(data):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO orders (customer_name, product_name, quantity, price, order_status) VALUES (%s, %s, %s, %s, 'Pending')"
        values = (data["customer_name"], data["product_name"], data["quantity"], data["price"])
        cursor.execute(query, values)
        order_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Order created successfully", "order_id": order_id}
    return {"error": "Database connection failed"}

def get_orders():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
        cursor.close()
        conn.close()
        return orders
    return {"error": "Database connection failed"}

def update_order_status(order_id, new_status):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE orders SET order_status = %s WHERE id = %s"
        cursor.execute(query, (new_status, order_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Order status updated successfully"}
    return {"error": "Database connection failed"}

def delete_order(order_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Order deleted successfully"}
    return {"error": "Database connection failed"}

def add_inventory_item(data):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO inventory (warehouse_id, product_name, stock_level) VALUES (%s, %s, %s)"
        values = (data["warehouse_id"], data["product_name"], data["stock_level"])
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Inventory item added successfully"}
    return {"error": "Database connection failed"}

def get_inventory():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventory")
        inventory = cursor.fetchall()
        cursor.close()
        conn.close()
        return inventory
    return {"error": "Database connection failed"}

def update_stock(item_id, new_stock):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE inventory SET stock_level = %s WHERE id = %s"
        cursor.execute(query, (new_stock, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Stock updated successfully"}
    return {"error": "Database connection failed"}

def delete_inventory_item(item_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = %s", (item_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Inventory item deleted successfully"}
    return {"error": "Database connection failed"}

def create_shipment(data):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO shipments (order_id, carrier_name, tracking_number, status, estimated_delivery) VALUES (%s, %s, %s, %s, %s)"
        values = (data["order_id"], data["carrier_name"], data["tracking_number"], "In Transit", data["estimated_delivery"])
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Shipment created successfully"}
    return {"error": "Database connection failed"}

def get_shipments():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM shipments")
        shipments = cursor.fetchall()
        cursor.close()
        conn.close()
        return shipments
    return {"error": "Database connection failed"}

def update_shipment_status(shipment_id, new_status):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE shipments SET status = %s WHERE id = %s"
        cursor.execute(query, (new_status, shipment_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Shipment status updated successfully"}
    return {"error": "Database connection failed"}

def delete_shipment(shipment_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM shipments WHERE id = %s", (shipment_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Shipment deleted successfully"}
    return {"error": "Database connection failed"}

def update_shipment_status_from_webhook(order_id, new_status):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE shipments SET status = %s WHERE order_id = %s", (new_status, order_id))
        cursor.execute("UPDATE orders SET order_status = %s WHERE id = %s", (new_status, order_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": f"Shipment and order status updated to '{new_status}'"}
    
    return {"error": "Database connection failed"}

def process_return(order_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, quantity FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()

        if not order:
            return {"error": "Order not found"}

        product_name, quantity = order
        cursor.execute("UPDATE orders SET order_status = 'Returned' WHERE id = %s", (order_id,))
        cursor.execute("SELECT id, stock_level FROM inventory WHERE product_name = %s", (product_name,))
        inventory = cursor.fetchone()

        if inventory:
            inv_id, current_stock = inventory
            new_stock = current_stock + quantity
            cursor.execute("UPDATE inventory SET stock_level = %s WHERE id = %s", (new_stock, inv_id))
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": f"Order {order_id} returned and inventory updated"}

        return {"error": "Product not found in inventory"}

    return {"error": "DB connection failed"}

def plan_route(shipment_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        distance = random.randint(10, 100)
        eta = f"{random.randint(1, 5)} hours"

        update_query = """
        UPDATE shipment
        SET route_distance_km = %s, estimated_delivery_time = %s
        WHERE shipment_id = %s
        """
        cursor.execute(update_query, (distance, eta, shipment_id))
        conn.commit()
        cursor.close()
        conn.close()
        return {"shipment_id": shipment_id, "distance": distance, "ETA": eta}

    return {"error": "Database connection failed"}

def assign_carrier(shipment_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        carriers = [
            {"name": "DHL", "contact": "1800-DHL-FAST"},
            {"name": "FedEx", "contact": "1800-FEDEX"},
            {"name": "BlueDart", "contact": "1800-BLUE"},
        ]

        selected = random.choice(carriers)

        update_query = """
        UPDATE shipment
        SET carrier_name = %s, carrier_contact = %s
        WHERE shipment_id = %s
        """
        cursor.execute(update_query, (selected["name"], selected["contact"], shipment_id))
        conn.commit()

        cursor.close()
        conn.close()

        return {"shipment_id": shipment_id, "carrier": selected}

    return {"error": "Database connection failed"}

def calculate_freight(shipment_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT route_distance_km FROM shipment WHERE shipment_id = %s", (shipment_id,))
        shipment = cursor.fetchone()

        if shipment and shipment["route_distance_km"]:
            distance = shipment["route_distance_km"]
            rate_per_km = 5.0
            total_cost = round(distance * rate_per_km, 2)

            update_query = """
            UPDATE shipment
            SET freight_cost = %s, payment_status = 'Pending'
            WHERE shipment_id = %s
            """
            cursor.execute(update_query, (total_cost, shipment_id))
            conn.commit()
            cursor.close()
            conn.close()

            return {
                "shipment_id": shipment_id,
                "distance_km": distance,
                "freight_cost": total_cost,
                "payment_status": "Pending"
            }

        return {"error": "Shipment not found or distance missing"}

    return {"error": "Database connection failed"}

def create_warehouse(warehouse):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO warehouse (name, location, manager_name) VALUES (%s, %s, %s)"
        values = (warehouse["name"], warehouse["location"], warehouse["manager_name"])
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Warehouse created successfully"}
    return {"error": "DB connection failed"}

def get_all_warehouses():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM warehouse")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    return {"error": "DB connection failed"}

def add_or_update_inventory(inv):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        check_query = """
        SELECT inventory_id FROM inventory_control
        WHERE warehouse_id = %s AND product_name = %s
        """
        cursor.execute(check_query, (inv["warehouse_id"], inv["product_name"]))
        existing = cursor.fetchone()

        if existing:
            update_query = """
            UPDATE inventory_control
            SET quantity = %s
            WHERE inventory_id = %s
            """
            cursor.execute(update_query, (inv["quantity"], existing[0]))
        else:
            insert_query = """
            INSERT INTO inventory_control (warehouse_id, product_name, quantity)
            VALUES (%s, %s, %s)
            """
            cursor.execute(insert_query, (inv["warehouse_id"], inv["product_name"], inv["quantity"]))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Inventory updated successfully"}
    return {"error": "DB connection failed"}

def get_inventory_by_warehouse(warehouse_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM inventory_control WHERE warehouse_id = %s", (warehouse_id,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    return {"error": "DB connection failed"}

def handle_return(return_data: dict):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO returns (warehouse_id, product_name, quantity, return_reason)
        VALUES (%s, %s, %s, %s)
        """
        values = (
            return_data["warehouse_id"],
            return_data["product_name"],
            return_data["quantity"],
            return_data["return_reason"]
        )
        cursor.execute(insert_query, values)
        update_query = """
        UPDATE inventory_control
        SET quantity = quantity + %s
        WHERE warehouse_id = %s AND product_name = %s
        """
        cursor.execute(update_query, (
            return_data["quantity"],
            return_data["warehouse_id"],
            return_data["product_name"]
        ))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Return processed and inventory updated"}
    return {"error": "DB connection failed"}

