import pandas as pd
import mysql.connector
from pathlib import Path
from datetime import datetime

# File paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PART1_DIR = BASE_DIR / "part1-database-etl"
REPORT_PATH = PART1_DIR / "data_quality_report.txt"

# MySQL connection config
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Shreya@123",
    "database": "fleximart"
}

# Extract - Load CSV files
def load_data():
    customers = pd.read_csv(DATA_DIR / "customers_raw.csv")
    products = pd.read_csv(DATA_DIR / "products_raw.csv")
    sales = pd.read_csv(DATA_DIR / "sales_raw.csv")
    
    return customers, products, sales

# Transform - Clean data
def clean_customers(df):
    original = len(df)
    df = df.drop_duplicates()
    dup_removed = original - len(df)
    
    missing_email = df["email"].isna().sum()
    df = df.dropna(subset=["email"])
    
    df["phone"] = df["phone"].fillna("").astype(str)
    
    if "registration_date" not in df.columns:
        df["registration_date"] = datetime.now().date()
    else:
        df["registration_date"] = pd.to_datetime(df["registration_date"], errors="coerce").dt.date
    
    return df, dup_removed, missing_email

def clean_products(df):
    original = len(df)
    df = df.drop_duplicates()
    dup_removed = original - len(df)
    
    missing_price = df["price"].isna().sum()
    df["price"] = df["price"].fillna(0)
    
    df["category"] = df["category"].astype(str).str.strip().str.capitalize()
    
    if "stock_quantity" in df.columns:
        df["stock_quantity"] = df["stock_quantity"].fillna(0).astype(int)
    else:
        df["stock_quantity"] = 0
    
    return df, dup_removed, missing_price

def clean_sales(df):
    original = len(df)
    df = df.drop_duplicates()
    dup_removed = original - len(df)
    
    missing_ids = df[["customer_id", "product_id"]].isna().sum().sum()
    df = df.dropna(subset=["customer_id", "product_id"])
    
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce").dt.date
    missing_dates = df["transaction_date"].isna().sum()
    df = df.dropna(subset=["transaction_date"])
    
    return df, dup_removed, missing_ids + missing_dates

# Load - Insert into database
def insert_customers(conn, df):
    cursor = conn.cursor()
    count = 0
    
    for _, row in df.iterrows():
        sql = "INSERT INTO customers (first_name, last_name, email, phone, city, registration_date) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, (
                row.get("first_name", ""),
                row.get("last_name", ""),
                row.get("email", ""),
                row.get("phone", ""),
                row.get("city", ""),
                row.get("registration_date")
            ))
            count += 1
        except:
            pass
    
    conn.commit()
    return count

def insert_products(conn, df):
    cursor = conn.cursor()
    count = 0
    
    for _, row in df.iterrows():
        sql = "INSERT INTO products (product_name, category, price, stock_quantity) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(sql, (
                row.get("product_name", ""),
                row.get("category", ""),
                float(row.get("price", 0)),
                int(row.get("stock_quantity", 0))
            ))
            count += 1
        except:
            pass
    
    conn.commit()
    return count

def insert_orders(conn, df):
    cursor = conn.cursor()
    orders_count = 0
    items_count = 0
    
    order_groups = df.groupby(["customer_id", "transaction_date"])
    
    for (cust_id, trans_date), group in order_groups:
        total = (group["unit_price"] * group["quantity"]).sum() if "unit_price" in df.columns else 0
        status = group["status"].iloc[0] if "status" in df.columns else "Pending"
        
        sql_order = "INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES (%s, %s, %s, %s)"
        try:
            cursor.execute(sql_order, (int(cust_id), trans_date, float(total), status))
            conn.commit()
            orders_count += 1
            order_id = cursor.lastrowid
            
            for _, item in group.iterrows():
                sql_item = "INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal) VALUES (%s, %s, %s, %s, %s)"
                qty = int(item.get("quantity", 1))
                price = float(item.get("unit_price", 0))
                subtotal = qty * price
                
                try:
                    cursor.execute(sql_item, (order_id, int(item.get("product_id", 0)), qty, price, subtotal))
                    items_count += 1
                except:
                    pass
            
            conn.commit()
        except:
            pass
    
    return orders_count, items_count

# Report generation
def generate_report(stats):
    with open(REPORT_PATH, "w") as f:
        f.write("=" * 70 + "\n")
        f.write("FlexiMart ETL Data Quality Report\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("FILE: customers_raw.csv\n")
        f.write("-" * 70 + "\n")
        f.write(f"Records processed: {stats['cust_proc']}\n")
        f.write(f"Duplicates removed: {stats['cust_dup']}\n")
        f.write(f"Missing values handled: {stats['cust_miss']}\n")
        f.write(f"Records loaded: {stats['cust_loaded']}\n\n")
        
        f.write("FILE: products_raw.csv\n")
        f.write("-" * 70 + "\n")
        f.write(f"Records processed: {stats['prod_proc']}\n")
        f.write(f"Duplicates removed: {stats['prod_dup']}\n")
        f.write(f"Missing values handled: {stats['prod_miss']}\n")
        f.write(f"Records loaded: {stats['prod_loaded']}\n\n")
        
        f.write("FILE: sales_raw.csv\n")
        f.write("-" * 70 + "\n")
        f.write(f"Records processed: {stats['sales_proc']}\n")
        f.write(f"Duplicates removed: {stats['sales_dup']}\n")
        f.write(f"Missing values handled: {stats['sales_miss']}\n")
        f.write(f"Orders created: {stats['orders_loaded']}\n")
        f.write(f"Order items created: {stats['items_loaded']}\n\n")
        
        f.write("=" * 70 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 70 + "\n")
        total_proc = stats['cust_proc'] + stats['prod_proc'] + stats['sales_proc']
        total_loaded = stats['cust_loaded'] + stats['prod_loaded'] + stats['orders_loaded']
        f.write(f"Total records processed: {total_proc}\n")
        f.write(f"Total records loaded: {total_loaded}\n")
        if total_proc > 0:
            f.write(f"Data quality score: {(total_loaded / total_proc * 100):.1f}%\n")

# Main execution
def main():
    print("\nStarting ETL Pipeline...")
    print("=" * 70)
    
    try:
        # Load CSV files
        print("\n[EXTRACT] Loading CSV files...")
        customers, products, sales = load_data()
        print(f"  - Customers: {len(customers)} records")
        print(f"  - Products: {len(products)} records")
        print(f"  - Sales: {len(sales)} records")
        
        # Clean data
        print("\n[TRANSFORM] Cleaning data...")
        customers_clean, cust_dup, cust_miss = clean_customers(customers)
        products_clean, prod_dup, prod_miss = clean_products(products)
        sales_clean, sales_dup, sales_miss = clean_sales(sales)
        
        print(f"  - Customers cleaned: {len(customers_clean)} records remaining")
        print(f"  - Products cleaned: {len(products_clean)} records remaining")
        print(f"  - Sales cleaned: {len(sales_clean)} records remaining")
        
        # Connect to database
        print("\n[LOAD] Connecting to MySQL...")
        conn = mysql.connector.connect(**db_config)
        print("  - Connected successfully")
        
        # Insert data
        print("\nInserting data into tables...")
        cust_loaded = insert_customers(conn, customers_clean)
        prod_loaded = insert_products(conn, products_clean)
        orders_loaded, items_loaded = insert_orders(conn, sales_clean)
        
        print(f"  - {cust_loaded} customers inserted")
        print(f"  - {prod_loaded} products inserted")
        print(f"  - {orders_loaded} orders inserted")
        print(f"  - {items_loaded} order items inserted")
        
        conn.close()
        
        # Generate report
        print("\n[REPORT] Generating data quality report...")
        stats = {
            'cust_proc': len(customers),
            'cust_dup': cust_dup,
            'cust_miss': cust_miss,
            'cust_loaded': cust_loaded,
            'prod_proc': len(products),
            'prod_dup': prod_dup,
            'prod_miss': prod_miss,
            'prod_loaded': prod_loaded,
            'sales_proc': len(sales),
            'sales_dup': sales_dup,
            'sales_miss': sales_miss,
            'orders_loaded': orders_loaded,
            'items_loaded': items_loaded
        }
        generate_report(stats)
        
        print(f"  - Report saved to {REPORT_PATH}")
        print("\n" + "=" * 70)
        print("ETL Pipeline completed successfully!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Please check:")
        print("  - MySQL is running")
        print("  - CSV files exist in /data folder")
        print("  - Database password is correct")

if __name__ == "__main__":
    main()
