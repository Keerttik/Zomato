from ai.client import generate_personalized_recommendations
import os
import sys

def main():
    print("=== TESTING GROQ LLM INTEGRATION ===")
    
    # Check key configuration
    api_key = os.getenv("LLM_API_KEY")
    if not api_key or api_key.startswith("your_"):
        print("Error: LLM_API_KEY is not configured in your .env file.")
        sys.exit(1)
        
    print(f"API Key found (starts with: {api_key[:6]}...)")
    
    # Mock user preferences
    user_prefs = {
        "location": "BTM",
        "cuisine": "North Indian",
        "budget": "medium",
        "min_rating": 4.0,
        "additional_preferences": "Must have outdoor rooftop seating and serve good paneer tikka."
    }
    
    # Mock candidate restaurants (usually from SQLite filter service)
    candidates = [
        {
            "name": "AB's - Absolute Barbecues",
            "location": "BTM",
            "cuisines": "European, Mediterranean, North Indian, BBQ",
            "rating_number": 4.9,
            "rating_text": "Excellent",
            "average_cost_for_two": 1400,
            "currency": "Rs.",
            "has_table_booking": 1,
            "has_online_delivery": 0
        },
        {
            "name": "eat.fit",
            "location": "BTM",
            "cuisines": "Healthy Food, North Indian, Biryani, Continental, Sandwich, Desserts",
            "rating_number": 4.6,
            "rating_text": "Very Good",
            "average_cost_for_two": 500,
            "currency": "Rs.",
            "has_table_booking": 0,
            "has_online_delivery": 1
        },
        {
            "name": "House of Commons",
            "location": "BTM",
            "cuisines": "Continental, Asian, North Indian",
            "rating_number": 4.8,
            "rating_text": "Excellent",
            "average_cost_for_two": 1000,
            "currency": "Rs.",
            "has_table_booking": 1,
            "has_online_delivery": 1
        }
    ]
    
    print("\nSending mock candidates to Groq API...")
    try:
        response = generate_personalized_recommendations(user_prefs, candidates)
        print("\nSuccessfully received and validated response from Groq!")
        print("-" * 50)
        
        recs = response.get("recommendations", [])
        print(f"Total Recommendations: {len(recs)}")
        for rec in recs:
            print(f"Rank {rec['rank']}: {rec['name']}")
            print(f"  Cuisine: {rec['cuisine']}")
            print(f"  Rating: {rec['rating']}")
            print(f"  Cost: {rec['currency']}{rec['cost_for_two']}")
            print(f"  AI Explanation: {rec['ai_explanation']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"\nFailed to get recommendations from Groq: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # Load dotenv explicitly in script context
    from dotenv import load_dotenv
    load_dotenv()
    main()
