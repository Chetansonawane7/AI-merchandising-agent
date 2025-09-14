import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LinearRegression

# Initialize text embedding model once
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def normalize(series):
    """Scales a pandas Series to a 0-1 range."""
    if series.max() == series.min():
        return pd.Series(0.5, index=series.index)
    return (series - series.min()) / (series.max() - series.min())

def calculate_campaign_similarity(products_df, campaign_text):
    """Calculates semantic similarity between product names and the active campaign."""
    campaign_emb = embedding_model.encode(campaign_text)
    product_embs = embedding_model.encode(products_df['product_name'].tolist())
    
    similarities = np.dot(product_embs, campaign_emb) / (
        np.linalg.norm(product_embs, axis=1) * np.linalg.norm(campaign_emb)
    )
    return similarities

def calculate_merchandising_score(df, weights, campaign_text):
    """Calculates a dynamic score for each product based on improved features."""
    scored_df = df.copy()
    
    # Normalize base metrics
    scored_df['sales_norm'] = normalize(scored_df['sales_count_last_30_days'])
    scored_df['views_norm'] = normalize(scored_df['view_count_last_30_days'])
    
    # Popularity = Combination of normalized sales and views
    scored_df['popularity_score'] = (0.6 * scored_df['sales_norm']) + (0.4 * scored_df['views_norm'])
    
    # Quality = Average rating normalized
    scored_df['quality_score'] = normalize(scored_df['avg_rating'])
    
    # Recency = More recent products get higher score
    scored_df['recency_score'] = 1 / (1 + normalize(scored_df['days_since_launch']))

    # Business priority
    scored_df['sale_boost'] = scored_df['on_sale'].apply(lambda x: 1 if x else 0)
    scored_df['stock_boost'] = normalize(scored_df['stock_quantity'])
    scored_df['business_priority_score'] = (0.7 * scored_df['sale_boost']) + (0.3 * scored_df['stock_boost'])

    # Campaign similarity score
    scored_df['campaign_similarity'] = calculate_campaign_similarity(scored_df, campaign_text)
    
    # Final weighted score includes the new campaign similarity term
    scored_df['final_score'] = (
        weights['popularity'] * scored_df['popularity_score'] +
        weights['quality'] * scored_df['quality_score'] +
        weights['recency'] * scored_df['recency_score'] +
        weights['business_priority'] * scored_df['business_priority_score'] +
        weights['campaign_relevance'] * scored_df['campaign_similarity']
    )

    scored_df['final_score'] = round(scored_df['final_score'] * 100, 2)
    return scored_df
