from services.orchestrator import get_recommendations_orchestrated
import os
import sys

def main():
    print("=== TESTING ORCHESTRATOR CORE ===")
    
    # Check if API key is present
    api_key = os.getenv("LLM_API_KEY")
    print(f"API Key configured: {api_key is not None and not api_key.startswith('your_')}")
    
    user_prefs = {
        "location": "BTM",
        "cuisine": "North Indian",
        "budget": "medium",
        "min_rating": 4.0,
        "additional_preferences": "romantic ambiance, outdoor setting, delicious paneer"
    }
    
    print("\nExecuting Orchestrated Query...")
    response = get_recommendations_orchestrated(user_prefs)
    
    print("\nResponse Metadata:")
    print(f"Fallback Mode Triggered: {response.get('fallback_mode')}")
    if response.get('fallback_mode'):
        print(f"Fallback Reason: {response.get('fallback_reason')}")
        
    print(f"\nRecommendations Returned: {len(response.get('recommendations', []))}")
    for rec in response.get('recommendations', []):
        print(f"Rank {rec['rank']}: {rec['name']}")
        print(f"  Cuisine: {rec['cuisine']}")
        print(f"  Rating: {rec['rating']}")
        print(f"  Cost: {rec['currency']}{rec['cost_for_two']}")
        print(f"  Rationale: {rec['ai_explanation']}")
        print("-" * 50)

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from dotenv import load_dotenv
    load_dotenv()
    main()
