-- Create the Database
CREATE DATABASE IF NOT EXISTS scm_db;
USE scm_db;

-- Orders Table (OMS)
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    order_status ENUM('Pending', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shipments Table (TMS)
CREATE TABLE IF NOT EXISTS shipments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    carrier_name VARCHAR(255),
    tracking_number VARCHAR(100) UNIQUE,
    status ENUM('In Transit', 'Delivered', 'Delayed') DEFAULT 'In Transit',
    estimated_delivery DATE,
    actual_delivery DATE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Table (DMS)
CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_id INT NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    stock_level INT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE warehouse (
    warehouse_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    location VARCHAR(100),
    manager_name VARCHAR(100)
);

CREATE TABLE inventory_control (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_id INT,
    product_name VARCHAR(100),
    quantity INT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE returns (
    return_id INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_id INT,
    product_name VARCHAR(100),
    quantity INT,
    return_reason VARCHAR(255),
    return_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



show TABLES;

select * from shipments;

ALTER TABLE shipments
ADD COLUMN route_distance_km INT,
ADD COLUMN estimated_delivery_time VARCHAR(50);

ALTER TABLE shipments
ADD COLUMN freight_cost DECIMAL(10, 2),
ADD COLUMN payment_status VARCHAR(20) DEFAULT 'Pending';



