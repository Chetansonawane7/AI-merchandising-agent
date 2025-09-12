import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv

# --- Import our custom modules ---
from data import products_df
from agent import run_agent_logic

# --- Load Environment Variables ---
# This line loads the GEMINI_API_KEY from your .env file
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="SkinSeoul AI Merchandising Agent",
    page_icon="🤖",
    layout="wide"
)

# --- Streamlit Frontend ---

st.title("🤖 SkinSeoul AI Merchandising Agent")
st.markdown("This tool uses an AI agent to dynamically set product ranking strategies based on real-time context.")

# --- Sidebar for Inputs ---
with st.sidebar:
    st.header("⚙️ Controls")
    
    # Improved API Key Handling:
    # 1. Try to get the key from the environment variables (.env file).
    # 2. If not found, provide a text input field as a fallback.
    api_key_env = os.environ.get("GEMINI_API_KEY")
    if api_key_env:
        st.success("API Key loaded from .env file!")
        api_key = api_key_env
    else:
        st.warning("API Key not found in .env file.")
        api_key = st.text_input("Enter your Gemini API Key", type="password")
        st.markdown("[Get your API key here](https://aistudio.google.com/app/apikey)")

    st.subheader("Situation Context")
    st.info("Modify the context below to see how the agent adapts its strategy.")
    
    season = st.selectbox("Season", ["Spring", "Summer", "Monsoon", "Autumn", "Winter"], index=3)
    active_campaign = st.text_input("Active Marketing Campaign", "Diwali Glow Sale")
    market_trend = st.text_area("Current Market Trend", "Customers are looking for gift sets and radiant-finish products.")
    inventory_status = st.text_area("Inventory Status Alert", "High stock of 'Radiant Glycolic Acid Peel' (ID 106).")
    
    category_to_rank = st.selectbox("Select Category to Rank", products_df['category'].unique())

    run_button = st.button("🚀 Run Agent", type="primary")

# --- Main Area for Output ---
st.header("Agent's Decision & Output")

if run_button:
    if not api_key:
        st.error("Please provide your Gemini API Key to proceed.")
    else:
        user_context = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "season": season,
            "active_campaign": active_campaign,
            "inventory_status": inventory_status,
            "market_trend": market_trend
        }
        
        with st.spinner("AI Agent is thinking..."):
            result = run_agent_logic(api_key, products_df, category_to_rank, user_context)

        if "error" in result:
            st.error(f"An error occurred while running the agent:")
            st.error(result["error"]) # Display the specific error message
        else:
            st.subheader("Agent's Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"**Agent's Reasoning:**")
                st.write(result['reasoning'])

            with col2:
                st.warning("**Chosen Strategy (Weights):**")
                st.json(result['weights'])

            st.subheader(f"🏆 Dynamically Ranked Products for '{category_to_rank}'")
            st.dataframe(result['ranked_df'][['product_id', 'product_name', 'price', 'final_score']], use_container_width=True)

else:
    st.info("Set the context in the sidebar and click 'Run Agent'.")

