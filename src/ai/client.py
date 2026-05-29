import os
import sys
import json
from pydantic import BaseModel, Field
from groq import Groq

# Import config
try:
    import config
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config

# Define expected Pydantic schema validation structures for LLM recommendations
class AIRecommendationItem(BaseModel):
    rank: int = Field(..., description="The numerical ranking of this recommendation.")
    name: str = Field(..., description="The name of the restaurant.")
    cuisine: str = Field(..., description="The cuisines of the restaurant.")
    rating: float = Field(..., description="The rating score.")
    cost_for_two: int = Field(..., description="Average cost for two people.")
    currency: str = Field(..., description="The currency symbol (e.g. Rs.).")
    ai_explanation: str = Field(..., description="Personalized reasoning explaining why this restaurant matches the user's specific preferences.")

class AIRecommendationResponse(BaseModel):
    recommendations: list[AIRecommendationItem] = Field(..., description="List of top recommended restaurants.")

def get_groq_client():
    """Initializes and returns a Groq Client if API key is present."""
    if not config.LLM_API_KEY or config.LLM_API_KEY == "your_llm_api_key_here":
        raise ValueError("Groq LLM_API_KEY is missing. Please configure it in your .env file.")
    return Groq(api_key=config.LLM_API_KEY)

def generate_personalized_recommendations(user_prefs, candidate_restaurants):
    """
    Constructs the prompt, calls Groq API in JSON mode,
    and returns parsed recommendation objects.
    """
    if not candidate_restaurants:
        return {"recommendations": []}

    client = get_groq_client()
    
    # Smart Fallback / Model Override:
    # If the user has a Groq key (gsk_...) but configures an OpenAI model (gpt-4o-mini),
    # map it to a valid, high-performance Groq model to prevent API errors.
    model_to_use = config.LLM_MODEL
    if config.LLM_API_KEY.startswith("gsk_") and "gpt" in model_to_use.lower():
        # Fall back to Llama 3.3 70B on Groq
        model_to_use = "llama-3.3-70b-versatile"
        print(f"Groq override: Mapping unsupported model '{config.LLM_MODEL}' to '{model_to_use}'")

    # 1. Format candidate list
    candidates_formatted = []
    for idx, r in enumerate(candidate_restaurants):
        candidates_formatted.append(
            f"{idx + 1}. Name: {r['name']} | Location: {r['location']} | "
            f"Cuisines: {r['cuisines']} | Rating: {r['rating_number']} ({r['rating_text']}) | "
            f"Cost for two: {r['currency']}{r['average_cost_for_two']} | "
            f"Delivery: {'Yes' if r['has_online_delivery'] else 'No'} | "
            f"Table Booking: {'Yes' if r['has_table_booking'] else 'No'}"
        )
    candidates_text = "\n".join(candidates_formatted)

    min_b = user_prefs.get('min_budget')
    max_b = user_prefs.get('max_budget')
    budget_str = f"Rs. {min_b} to {f'Rs. {max_b}' if max_b and int(max_b) < 2000 else 'unlimited'}"

    # 2. Compile user prompt
    user_prompt = f"""
**User Specific Preferences**:
* Location: {user_prefs.get('location')}
* Preferred Cuisine: {user_prefs.get('cuisine', 'Any')}
* Budget Range: {budget_str}
* Minimum Rating: {user_prefs.get('min_rating', 'Any')}
* Additional Custom Preferences: "{user_prefs.get('additional_preferences', 'None')}"

**Candidate Restaurants (Pre-filtered from database)**:
{candidates_text}

Select up to 3 best matching unique restaurants, rank them by match quality, and write a personalized explanation for why each is chosen.
"""

    # 3. Compile system instructions enforcing JSON schema output
    json_schema_format = {
        "type": "object",
        "properties": {
            "recommendations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "rank": {"type": "integer"},
                        "name": {"type": "string"},
                        "cuisine": {"type": "string"},
                        "rating": {"type": "number"},
                        "cost_for_two": {"type": "integer"},
                        "currency": {"type": "string"},
                        "ai_explanation": {"type": "string"}
                    },
                    "required": ["rank", "name", "cuisine", "rating", "cost_for_two", "currency", "ai_explanation"]
                }
            }
        },
        "required": ["recommendations"]
    }

    system_instruction = f"""
You are Zomato's AI Restaurant Recommendation Assistant.
Your task is to select and rank the top 3 restaurants from the provided candidate list that best fit the user's preferences.
Do NOT suggest any restaurant that is not in the provided candidates list.
For each selected restaurant, write a concise, personalized explanation (2-3 sentences) directly addressing the user's explicit and implicit preferences.

You MUST return a JSON object adhering exactly to this JSON schema:
{json.dumps(json_schema_format, indent=2)}
"""

    # 4. Invoke Groq completion in JSON mode
    try:
        completion = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )
        
        # Load and parse output string
        raw_text = completion.choices[0].message.content
        result_json = json.loads(raw_text)
        
        # Validate schema using Pydantic model dump/load check
        AIRecommendationResponse(**result_json)
        
        return result_json
        
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        raise e
