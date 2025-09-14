import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

from data import products_df
from agent import run_agent_logic

load_dotenv()

st.set_page_config(
    page_title="SkinSeoul AI Merchandising Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 SkinSeoul AI Merchandising Agent")
st.markdown("Dynamically rank products using AI based on real-time context and custom weights.")

with st.sidebar:
    st.header("⚙️ Controls")
    
    api_key_env = os.environ.get("GEMINI_API_KEY")
    if api_key_env:
        st.success("API Key loaded from .env file!")
        api_key = api_key_env
    else:
        st.warning("API Key not found.")
        api_key = st.text_input("Enter your Gemini API Key", type="password")

    st.subheader("Situation Context")
    season = st.selectbox("Season", ["Spring", "Summer", "Monsoon", "Autumn", "Winter"], index=3)
    active_campaign = st.text_input("Active Marketing Campaign", "Diwali Glow Sale")
    market_trend = st.text_area("Current Market Trend", "Customers prefer radiant-finish products.")
    inventory_status = st.text_area("Inventory Status Alert", "High stock of 'Radiant Glycolic Acid Peel' (ID 106).")
    category_to_rank = st.selectbox("Select Category to Rank", products_df['category'].unique())

    st.subheader("📊 Set Custom Weights (They sum to 1.0)")
    pop = st.slider('Popularity Weight', 0.0, 1.0, 0.25, step=0.05)
    qual = st.slider('Quality Weight', 0.0, 1.0, 0.25, step=0.05)
    rec = st.slider('Recency Weight', 0.0, 1.0, 0.15, step=0.05)
    biz = st.slider('Business Priority Weight', 0.0, 1.0, 0.20, step=0.05)
    camp = st.slider('Campaign Relevance Weight', 0.0, 1.0, 0.15, step=0.05)

    # Normalize weights so sum is exactly 1
    total = pop + qual + rec + biz + camp
    normalized_weights = {
        'popularity': pop / total,
        'quality': qual / total,
        'recency': rec / total,
        'business_priority': biz / total,
        'campaign_relevance': camp / total
    }

    run_button = st.button("🚀 Run Agent", type="primary")

st.header("Agent's Decision & Output")

if run_button:
    if not api_key:
        st.error("Please provide your Gemini API Key.")
    else:
        user_context = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "season": season,
            "active_campaign": active_campaign,
            "inventory_status": inventory_status,
            "market_trend": market_trend
        }

        with st.spinner("AI Agent is thinking..."):
            result = run_agent_logic(
                api_key,
                products_df,
                category_to_rank,
                user_context,
                normalized_weights
            )

        if "error" in result:
            st.error(f"An error occurred: {result['error']}")
        else:
            st.subheader("🧠 Agent's Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Reasoning:**")
                st.write(result['reasoning'])

            with col2:
                st.warning("**Weights Used:**")
                st.json(result['weights'])

            st.subheader(f"🏆 Ranked Products for '{category_to_rank}'")
            st.dataframe(result['ranked_df'][[
                'product_id', 'product_name', 'price', 'final_score'
            ]], use_container_width=True)

else:
    st.info("Configure context and weights in the sidebar, then click 'Run Agent'.")


