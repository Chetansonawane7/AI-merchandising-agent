import json
import google.generativeai as genai

# Import the necessary function from our core logic module
from core_logic import calculate_merchandising_score

def run_agent_logic(api_key, products_df, category, context):
    """
    Configures API, runs the agent's reasoning loop, and returns the results.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        You are an expert e-commerce merchandiser for a skincare brand called SkinSeoul.
        Your task is to define the optimal product ranking strategy for the '{category}' category based on real-time data.

        Here is the current context:
        {json.dumps(context, indent=2)}

        Based on this context, provide a weighting strategy. The four weights ('popularity', 'quality', 'recency', 'business_priority') must sum to 1.0.

        Your response MUST be a single, valid JSON object. Do not include any text, markdown, or explanations before or after the JSON.
        The JSON object must contain two keys:
        1. "reasoning": A brief explanation of your strategic choices.
        2. "weights": A JSON object with the four weight keys and their corresponding numeric values.
        """

        response = model.generate_content(prompt)
        # Clean the response to ensure it's valid JSON
        cleaned_response_text = response.text.strip().replace("```json", "").replace("```", "")
        strategy = json.loads(cleaned_response_text)
        
        # Filter the main DataFrame for the selected category
        filtered_df = products_df[products_df['category'] == category].copy()
        if filtered_df.empty:
            return {"error": f"No products found for category: {category}"}

        # Use the imported function to calculate scores
        ranked_df = calculate_merchandising_score(filtered_df, strategy['weights'])
        ranked_df = ranked_df.sort_values(by='final_score', ascending=False)
        
        # Return all results as a dictionary
        return {
            "reasoning": strategy['reasoning'],
            "weights": strategy['weights'],
            "ranked_df": ranked_df
        }

    except Exception as e:
        return {"error": f"An error occurred: {e}"}
