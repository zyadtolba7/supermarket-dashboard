import pandas as pd
import os

file_name = "supermarket_large_dataset.csv"

if os.path.exists(file_name):
    print("جاري قراءة أول 1000 صف لاستكشاف البيانات...\n")
    
    # قراءة أول 1000 صف بس عشان نعرف شكل الداتا بسرعة
    df = pd.read_csv(file_name, nrows=1000)
    
    print("================ أسماء الأعمدة ================")
    print(df.columns.tolist())
    
    print("\n================ أول 5 صفوف ================")
    print(df.head())
    
    print("\n================ أنواع البيانات (dtypes) ================")
    print(df.dtypes)
    
    print("\n================ القيم الناقصة في أول 1000 صف ================")
    print(df.isnull().sum())
    
else:
    print("مش لاقي الملف! تأكد من الاسم.")