import pandas as pd

# In a real-world application, this would be a connection to a live database.
# For this project, we are mocking the data here.

data = {
    'product_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'product_name': [
        'Hydrating Hyaluronic Acid Serum', 'Glow-Up Vitamin C Moisturizer',
        'Daily Mineral Sunscreen SPF 50', 'Clarifying BHA Toner',
        'Soothing Centella Cream', 'Radiant Glycolic Acid Peel',
        'Overnight Retinol Treatment', 'Deep Cleanse Oil Cleanser',
        'Peptide Firming Eye Cream', 'Calming Green Tea Mask'
    ],
    'category': [
        'Serums', 'Moisturizers', 'Sunscreens', 'Toners', 'Moisturizers',
        'Serums', 'Serums', 'Cleansers', 'Eye Creams', 'Masks'
    ],
    'price': [25.00, 35.00, 28.00, 22.00, 32.00, 45.00, 55.00, 24.00, 40.00, 29.00],
    'stock_quantity': [150, 80, 200, 120, 50, 75, 40, 180, 90, 110],
    'sales_count_last_30_days': [500, 350, 600, 250, 150, 200, 180, 450, 120, 220],
    'avg_rating': [4.8, 4.6, 4.9, 4.5, 4.7, 4.8, 4.4, 4.9, 4.6, 4.8],
    'view_count_last_30_days': [5000, 4000, 7000, 3000, 2500, 3500, 3200, 6000, 2000, 4500],
    'is_new_arrival': [True, False, False, False, True, False, False, True, False, False],
    'on_sale': [False, True, False, False, False, True, False, False, True, False]
}

products_df = pd.DataFrame(data)
