import pandas as pd
import time

file_name = "supermarket_large_dataset.csv"
output_name = "supermarket_advanced.csv"

# سحب أعمدة من كل قسم في الداتا
columns_to_keep = [
    # Transactions & Time
    'transaction_id', 'basket_id', 'customer_id', 'store_id', 'product_id',
    'transaction_date', 'transaction_time', 'day_name', 'month_name', 'year', 'season', 'is_weekend',
    # Customers
    'customer_age', 'customer_gender', 'customer_segment', 'customer_city',
    'customer_churn_risk', 'loyalty_tier', 'customer_lifetime_value', 'customer_retention_score',
    # Store
    'store_city', 'store_type', 'store_rating', 'store_size_sqft',
    # Product & Sales
    'product_name', 'product_category', 'product_subcategory', 'brand',
    'quantity', 'unit_price', 'net_sales', 'gross_profit', 'profit_margin_percent',
    # Inventory & Ops
    'stockout_status', 'low_stock_status', 'inventory_turnover_rate', 'supplier_rating', 'delivery_delay_days'
]

print("⏳ جاري قراءة البيانات...")
start = time.time()

chunks = []
for chunk in pd.read_csv(file_name, usecols=columns_to_keep, chunksize=200000):
    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)
print(f"✅ تم قراءة {len(df):,} صف في {time.time() - start:.1f} ثانية.")

print("🧹 جاري تنظيف البيانات...")
df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

# التأكد إن الأرقام أرقام
for col in ['net_sales', 'gross_profit', 'quantity', 'unit_price', 'profit_margin_percent', 'store_rating']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

df = df.dropna(subset=['net_sales', 'quantity', 'product_category'])
df.to_csv(output_name, index=False)
print(f"✅ تم حفظ الملف: {output_name} ({len(df):,} صف)")