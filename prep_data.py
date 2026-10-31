import pandas as pd
import time

file_name = "supermarket_large_dataset.csv"
output_name = "supermarket_clean.csv"

# أهم الأعمدة اللي هنحتاجها في الداشبورد
columns_to_keep = [
    'transaction_id', 'customer_id', 'store_id', 'product_id',
    'customer_age', 'customer_gender', 'customer_segment', 'customer_city',
    'loyalty_tier', 'customer_churn_risk',
    'store_city', 'store_type', 'store_rating',
    'product_name', 'product_category', 'product_subcategory', 'brand',
    'quantity', 'unit_price', 'net_sales', 'gross_profit', 'profit_margin_percent',
    'transaction_date', 'month_name', 'year', 'season', 'day_name'
]

print("⏳ جاري قراءة البيانات... (ده هياخد شوية وقت لأن الملف كبير)")
start = time.time()

# قراءة الملف بالقطع (chunks) عشان منستهلكش كل الرامات
chunks = []
for chunk in pd.read_csv(file_name, usecols=columns_to_keep, chunksize=100000):
    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)

print(f"✅ تم قراءة {len(df):,} صف في {time.time() - start:.1f} ثانية.")

print("🧹 جاري تنظيف البيانات...")
# التأكد من تحويل التاريخ
df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')

# حذف الصفوف اللي فيها قيم ناقصة في الأعمدة المهمة
df = df.dropna(subset=['net_sales', 'quantity', 'product_category'])

# حفظ الملف النضيف
df.to_csv(output_name, index=False)
print(f"✅ تم حفظ الملف النضيف: {output_name}")
print(f"📊 عدد الصفوف النهائي: {len(df):,}")