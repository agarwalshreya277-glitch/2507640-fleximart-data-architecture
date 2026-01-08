# Star Schema Design - FlexiMart Data Warehouse

## Section 1: Schema Overview

The FlexiMart data warehouse uses a star schema with one central fact table called `fact_sales` and three dimension tables: `dim_date`, `dim_product` and `dim_customer`. The grain of `fact_sales` is one row per product per order line item, which means each record represents a single product sold in a specific order on a specific date to a specific customer.

The `fact_sales` table stores numeric measures related to sales: `quantity_sold`, `unit_price`, `discount_amount` and `total_amount`. It also contains foreign keys `date_key`, `product_key` and `customer_key` which link to the respective dimension tables. The `dim_date` table is a conformed date dimension with attributes such as `full_date`, `day_of_week`, `month`, `month_name`, `quarter`, `year` and `is_weekend`, allowing rich time-based analysis. The `dim_product` dimension stores attributes like `product_id`, `product_name`, `category`, `subcategory` and `unit_price`. The `dim_customer` dimension holds customer-related attributes including `customer_id`, `customer_name`, `city`, `state` and `customer_segment`. Together these tables support flexible slicing and dicing of sales data by time, product and customer.

## Section 2: Design Decisions

The chosen granularity for `fact_sales` is the transaction line-item level because it preserves maximum detail about each sale. At this grain, analysts can aggregate data to any higher level such as daily, monthly, product-level or customer-level summaries. If the fact table stored only order headers, important information like per-product quantities and discounts inside an order would be lost.

Surrogate keys are used in the dimension tables instead of natural keys like product codes or customer IDs. Surrogate keys are integer values generated inside the warehouse and are stable even if source system codes change. They also allow slowly changing dimension techniques in the future. This star schema supports drill-down and roll-up operations naturally. Users can start from yearly revenue, then drill down to quarter, month and specific dates using `dim_date`, or slice performance by product category and individual products using `dim_product`, and by customer segments, cities or individual customers using `dim_customer`.

## Section 3: Sample Data Flow

Source Transaction (OLTP system):

Order #101, Customer "John Doe", Product "Laptop Pro 14", Quantity: 2, Unit Price: 50000, Order Date: 2024-01-15.

In the data warehouse, this transaction is broken into keys and measures. First, the order date `2024-01-15` is mapped to a row in `dim_date` with `date_key = 20240115`, `month = 1`, `month_name = 'January'` and `quarter = 'Q1'`. The product "Laptop Pro 14" is mapped to a row in `dim_product`, for example `product_key = 5`, with category `Electronics`. The customer "John Doe" is mapped to `dim_customer` with `customer_key = 12` and attributes like city and customer_segment.

The `fact_sales` table then receives a record such as:

- `date_key`: 20240115  
- `product_key`: 5  
- `customer_key`: 12  
- `quantity_sold`: 2  
- `unit_price`: 50000  
- `discount_amount`: 0  
- `total_amount`: 100000  

This structure allows the same transaction to be analyzed by time, product, and customer dimensions efficiently.
