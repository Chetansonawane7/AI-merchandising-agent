import pandas as pd

def normalize(series):
    """Scales a pandas Series to a 0-1 range."""
    if series.max() == series.min():
        return pd.Series(0.5, index=series.index)
    return (series - series.min()) / (series.max() - series.min())

def calculate_merchandising_score(df, weights):
    """Calculates a dynamic score for each product based on agent-provided weights."""
    scored_df = df.copy()
    
    # Calculate individual score components
    scored_df['sales_norm'] = normalize(scored_df['sales_count_last_30_days'])
    scored_df['views_norm'] = normalize(scored_df['view_count_last_30_days'])
    scored_df['popularity_score'] = (0.6 * scored_df['sales_norm']) + (0.4 * scored_df['views_norm'])
    
    scored_df['quality_score'] = normalize(scored_df['avg_rating'])
    scored_df['recency_score'] = scored_df['is_new_arrival'].apply(lambda x: 1 if x else 0)
    
    scored_df['sale_boost'] = scored_df['on_sale'].apply(lambda x: 1 if x else 0)
    scored_df['stock_boost'] = normalize(scored_df['stock_quantity'])
    scored_df['business_priority_score'] = (0.7 * scored_df['sale_boost']) + (0.3 * scored_df['stock_boost'])
    
    # Calculate the final weighted score
    scored_df['final_score'] = (
        weights['popularity'] * scored_df['popularity_score'] +
        weights['quality'] * scored_df['quality_score'] +
        weights['recency'] * scored_df['recency_score'] +
        weights['business_priority'] * scored_df['business_priority_score']
    )
    
    scored_df['final_score'] = round(scored_df['final_score'] * 100, 2)
    return scored_df
