USE fleximart_dw;

INSERT INTO dim_date (
    date_key,
    full_date,
    day_of_week,
    day_of_month,
    month,
    month_name,
    quarter,
    year,
    is_weekend
) VALUES
(20240101, '2024-01-01', 'Monday',    1, 1, 'January',  'Q1', 2024, 0),
(20240215, '2024-02-15', 'Thursday', 15, 2, 'February', 'Q1', 2024, 0);

-- Insert into dim_product (15 products, 3 categories)

INSERT INTO dim_product (product_id, product_name, category, subcategory, unit_price) VALUES
('ELEC001', 'Samsung Galaxy S21',      'Electronics', 'Mobile',      79999.00),
('ELEC002', 'Apple iPhone 14',         'Electronics', 'Mobile',      89999.00),
('ELEC003', 'Dell Inspiron Laptop',    'Electronics', 'Laptop',      65000.00),
('ELEC004', 'Sony WH-1000XM4',         'Electronics', 'Headphones',  24999.00),
('ELEC005', 'Mi Smart LED TV 43\"',     'Electronics', 'Television',  29999.00),

('SHOE001', 'Nike Running Shoes',      'Footwear',    'Sports Shoes', 4999.00),
('SHOE002', 'Adidas Sports Shoes',     'Footwear',    'Sports Shoes', 4499.00),
('SHOE003', 'Puma Casual Sneakers',    'Footwear',    'Casual Shoes', 3999.00),
('SHOE004', 'Bata Formal Shoes',       'Footwear',    'Formal Shoes', 2999.00),
('SHOE005', 'Campus Walking Shoes',    'Footwear',    'Walking Shoes',2499.00),

('HOME001', 'Prestige Mixer Grinder',  'Home & Kitchen', 'Appliances', 5499.00),
('HOME002', 'Philips Air Fryer',       'Home & Kitchen', 'Appliances',11999.00),
('HOME003', 'Milton Water Bottle',     'Home & Kitchen', 'Accessories', 699.00),
('HOME004', 'Sleepwell Mattress',      'Home & Kitchen', 'Bedding',   15999.00),
('HOME005', 'Havells Ceiling Fan',     'Home & Kitchen', 'Appliances', 3499.00);

-- Insert into dim_customer (12 customers, 4 cities)

INSERT INTO dim_customer (customer_id, customer_name, city, state, customer_segment) VALUES
('C001', 'Riya Sharma',      'Mumbai',     'Maharashtra', 'Retail'),
('C002', 'Amit Verma',       'Bengaluru',  'Karnataka',   'Retail'),
('C003', 'John Dsouza',      'Mumbai',     'Maharashtra', 'Corporate'),
('C004', 'Priya Singh',      'Delhi',      'Delhi',       'Retail'),
('C005', 'Rahul Mehta',      'Ahmedabad',  'Gujarat',     'SMB'),
('C006', 'Sneha Kulkarni',   'Pune',       'Maharashtra', 'Retail'),
('C007', 'Vikas Yadav',      'Lucknow',    'Uttar Pradesh','SMB'),
('C008', 'Neha Agarwal',     'Jaipur',     'Rajasthan',   'Corporate'),
('C009', 'Sanjay Gupta',     'Kolkata',    'West Bengal', 'Retail'),
('C010','Anita Nair',        'Bengaluru',  'Karnataka',   'Corporate'),
('C011','Manish Jain',       'Delhi',      'Delhi',       'SMB'),
('C012','Kavya Reddy',       'Hyderabad',  'Telangana',   'Retail');

INSERT INTO fact_sales (date_key, product_key, customer_key, quantity_sold, unit_price, discount_amount, total_amount) VALUES
(20240101, 1, 1, 1, 79999.00, 0, 79999.00),
(20240101, 2, 2, 1, 89999.00, 0, 89999.00),
(20240215, 3, 3, 2, 65000.00, 5000.00, 125000.00),
(20240215, 6, 4, 3,  4999.00, 0, 14997.00);
