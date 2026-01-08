# Database Schema Documentation

## Entity-Relationship Description

### ENTITY: customers
Purpose: Stores customer information.

Attributes:
- customer_id: Unique identifier for each customer (Primary Key, auto-increment).
- first_name: Customer’s first name.
- last_name: Customer’s last name.
- email: Unique email address of the customer (NOT NULL).
- phone: Standardized phone number.
- city: City where the customer lives.
- registration_date: Date when the customer registered on FlexiMart.

Relationships:
- One customer can place many orders (1:M with orders table via customer_id).

### ENTITY: products
Purpose: Stores product master data.

Attributes:
- product_id: Unique identifier for each product (Primary Key, auto-increment).
- product_name: Name of the product.
- category: Category of the product (e.g., Electronics, Clothing).
- price: Selling price of one unit.
- stock_quantity: Available stock quantity.

Relationships:
- One product can appear in many order_items rows (1:M with order_items via product_id).

### ENTITY: orders
Purpose: Stores high level order information.

Attributes:
- order_id: Unique identifier for each order (Primary Key, auto-increment).
- customer_id: References the customer who placed the order (Foreign Key to customers.customer_id).
- order_date: Date when the order was created.
- total_amount: Total monetary value of the order.
- status: Current status of the order (e.g., Pending, Completed).

Relationships:
- Many orders belong to one customer (M:1 with customers).
- One order can have many order_items (1:M with order_items via order_id).

### ENTITY: order_items
Purpose: Stores line-item details for each order.

Attributes:
- order_item_id: Unique identifier for each order line (Primary Key, auto-increment).
- order_id: References the parent order (Foreign Key to orders.order_id).
- product_id: References the product being sold (Foreign Key to products.product_id).
- quantity: Quantity of the product in that line.
- unit_price: Price per unit at time of sale.
- subtotal: Line amount = quantity × unit_price.

Relationships:
- Each order_item is linked to exactly one order and one product (M:1 to orders and products).

## Normalization Explanation (3NF)

The FlexiMart OLTP schema is designed in third normal form to reduce redundancy and avoid anomalies. Each table represents a single, clear entity: customers, products, orders, and order_items. All non-key attributes in a table depend only on that table’s primary key. For example, in the customers table, attributes like first_name, last_name, email, phone, city, and registration_date depend only on customer_id. In the products table, product_name, category, price, and stock_quantity depend only on product_id.

In the orders table, order_date, total_amount, and status depend entirely on order_id. No customer details like name or city are stored inside orders, because that information lives in the customers table. Similarly, in the order_items table, quantity, unit_price, and subtotal depend on order_item_id and logically on the combination of order_id and product_id. Product details such as product_name or category are not duplicated in order_items.

This design avoids update anomalies because if a customer changes their email or a product price changes, the update happens in only one row in the respective master table. Insert anomalies are reduced since a new product or customer can be inserted without creating an order. Delete anomalies are avoided because deleting an order does not delete the product or customer definitions. Since every non-key attribute depends on “the key, the whole key, and nothing but the key”, the schema satisfies the conditions of third normal form.

## Sample Data Representation

### customers

| customer_id | first_name | last_name | email                    | phone          | city      | registration_date |
|------------|------------|-----------|--------------------------|----------------|-----------|-------------------|
| 1          | Riya       | Sharma    | riya.sharma@example.com  | +91-9876543210 | Mumbai    | 2024-01-10        |
| 2          | Amit       | Verma     | amit.verma@example.com   | +91-9123456789 | Bengaluru | 2024-02-05        |

### products

| product_id | product_name      | category     | price   | stock_quantity |
|-----------|-------------------|-------------|---------|----------------|
| 1         | Laptop Pro 14     | Electronics | 75000.0 | 25             |
| 2         | Running Shoes Max | Footwear    | 4500.0  | 80             |

### orders

| order_id | customer_id | order_date | total_amount | status    |
|---------|-------------|------------|--------------|-----------|
| 101     | 1           | 2024-01-15 | 150000.00    | Completed |
| 102     | 2           | 2024-02-12 | 4500.00      | Pending   |

### order_items

| order_item_id | order_id | product_id | quantity | unit_price | subtotal  |
|--------------|----------|-----------|----------|-----------|----------|
| 1            | 101      | 1         | 2        | 75000.00  | 150000.00|
| 2            | 102      | 2         | 1        | 4500.00   | 4500.00  |
