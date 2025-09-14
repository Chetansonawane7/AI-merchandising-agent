import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load the provided CSV dataset
file_path = './Mock_Skincare_Dataset - Data.csv'
products_df = pd.read_csv(file_path)

# Assign unique product IDs
products_df['product_id'] = range(1, len(products_df) + 1)

# Map product name to inferred category
def infer_category(product_name):
    name = product_name.lower()
    if 'serum' in name:
        return 'Serums'
    elif 'moisturizer' in name:
        return 'Moisturizers'
    elif 'mask' in name:
        return 'Masks'
    elif 'cleanser' in name:
        return 'Cleansers'
    elif 'toner' in name:
        return 'Toners'
    elif 'eye' in name:
        return 'Eye Creams'
    elif 'peel' in name:
        return 'Peels'
    else:
        return 'General Skincare'

# Rename columns first
products_df.rename(columns={
    'Product Name': 'product_name',
    'Brand': 'brand',
    'Price (USD)': 'price'
}, inplace=True)

products_df['category'] = products_df['product_name'].apply(infer_category)

# Populate other required columns
products_df['stock_quantity'] = products_df['Units in Stock']
products_df['sales_count_last_30_days'] = products_df['Volume Sold Last Month']
products_df['view_count_last_30_days'] = products_df['Views Last Month']
products_df['avg_rating'] = np.random.uniform(3.5, 5.0, len(products_df))  # Simulated ratings
products_df['is_new_arrival'] = np.random.choice([True, False], len(products_df), p=[0.1, 0.9])
products_df['on_sale'] = np.random.choice([True, False], len(products_df), p=[0.2, 0.8])

# Generate simulated product launch dates
start_date = datetime(2023, 1, 1)
products_df['launch_date'] = [start_date + timedelta(days=np.random.randint(0, 600)) for _ in range(len(products_df))]
products_df['days_since_launch'] = (datetime.now() - pd.to_datetime(products_df['launch_date'])).dt.days

# Select final relevant columns
products_df = products_df[[
    'product_id',
    'product_name',
    'category',
    'price',
    'stock_quantity',
    'sales_count_last_30_days',
    'avg_rating',
    'view_count_last_30_days',
    'is_new_arrival',
    'on_sale',
    'days_since_launch'
]]
