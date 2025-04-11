# 🏭 Supply Chain Management System

This project is a backend system that streamlines the **supply chain process** — from order placement to delivery — by integrating the following three core modules:

- **📦 Order Management System (OMS)**
- **🚚 Transportation Management System (TMS)**
- **🏬 Distribution Management System (DMS)**

Each module is built independently using **FastAPI** and communicates via **modular API endpoints**.

---

## 📌 Features

### 🔹 Order Management System (OMS)
- Capture and validate customer orders
- Real-time inventory checks before order placement
- Handle order status updates and returns

### 🔹 Transportation Management System (TMS)
- Route planning and delivery time estimation
- Carrier assignment using dummy 3PL data
- Freight cost calculation based on distance
- Delivery confirmation and order sync

### 🔹 Distribution Management System (DMS)
- Warehouse registration and management
- Inventory control per warehouse
- Product restocking on return

---

## ⚙️ Tech Stack

| Layer | Tools |
|-------|-------|
| Backend | Python, FastAPI |
| Database | MySQL (via `mysql-connector-python`) |
| API Format | REST (JSON) |

---

## 🔄 API Endpoints Overview

### 📦 OMS
- `POST /orders/` – Place an order
- `GET /orders/` – List orders
- `PUT /orders/{id}` – Update status
- `DELETE /orders/{id}` – Delete order
- `POST /orders/{id}/return` – Handle return

### 🚚 TMS
- `POST /shipments/` – Create shipment
- `POST /tms/plan-route/{id}` – Simulate route planning
- `POST /tms/assign-carrier/{id}` – Assign carrier
- `POST /tms/freight/{id}` – Calculate freight
- `POST /tms/confirm-delivery/{id}` – Confirm delivery
- `POST /webhook/shipment-status/` – Real-time shipment update (simulated)
- `GET /shipments/` – List all shipments

### 🏬 DMS
- `POST /dms/warehouse` – Add warehouse
- `GET /dms/warehouse` – List warehouses
- `POST /dms/inventory` – Add/update inventory
- `GET /dms/inventory/{warehouse_id}` – Get warehouse inventory
- `POST /dms/returns` – Process a return


## 💾 Setup Instructions

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Setup Database
- Create a MySQL database named `scm_db`
- Run the `database.sql` script to create tables

### 3. Set Environment Variable (in `.env`)
```env
DB_PASSWORD=your_mysql_password
```

### 4. Run FastAPI App
```bash
uvicorn main:app --reload
```
