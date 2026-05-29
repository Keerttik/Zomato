import os
import sys

# Import components
try:
    import config
    from services.filter_service import query_restaurants
    from ai.client import generate_personalized_recommendations
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config
    from services.filter_service import query_restaurants
    from ai.client import generate_personalized_recommendations

def _clean_name_for_matching(name):
    import re
    # Keep only ASCII alphanumeric characters and lowercase them
    return "".join(re.findall(r'[a-z0-9]+', name.lower()))

def get_recommendations_orchestrated(user_prefs):
    """
    Orchestrates the recommendation flow:
    1. Pre-filters restaurants from SQLite database.
    2. Fallback check: if LLM API is not configured, degradations/fallbacks apply.
    3. Triggers LLM personalizer to rank and generate explanations.
    4. Validates output and formats the payload.
    """
    location = user_prefs.get("location")
    cuisine = user_prefs.get("cuisine")
    min_budget = user_prefs.get("min_budget")
    max_budget = user_prefs.get("max_budget")
    min_rating = user_prefs.get("min_rating", 0.0)
    additional_prefs = user_prefs.get("additional_preferences", "")
    
    # 1. Fetch pre-filtered candidates from database (respects config limits)
    candidates, relaxed_reason = query_restaurants(
        location=location,
        cuisine=cuisine,
        min_budget=min_budget,
        max_budget=max_budget,
        min_rating=min_rating
    )
    
    # If no candidate matches at all (even after relaxation)
    if not candidates:
        return {
            "user_context": user_prefs,
            "fallback_mode": False,
            "query_relaxed": None,
            "recommendations": []
        }
        
    # 2. Check if LLM API key is present. If not, trigger DB-Only fallback mode.
    if not config.LLM_API_KEY or config.LLM_API_KEY == "your_llm_api_key_here":
        print("Warning: Groq API Key not configured. Using Database-Only Fallback Mode.")
        return _build_db_only_fallback(candidates, user_prefs, "API key not configured.", relaxed_reason)
        
    # 3. Call LLM personalizer via Groq
    try:
        llm_response = generate_personalized_recommendations(user_prefs, candidates)
        
        # 4. Hallucination Guard: Validate LLM output names match database records
        db_clean_map = {_clean_name_for_matching(c["name"]): c for c in candidates}
        validated_recs = []
        
        seen_names = set()
        for item in llm_response.get("recommendations", []):
            name_key = _clean_name_for_matching(item.get("name", ""))
            if name_key in db_clean_map and name_key not in seen_names:
                seen_names.add(name_key)
                db_record = db_clean_map[name_key]
                # Merge DB properties with LLM rank & explanation to prevent LLM rating/cost fabrication
                validated_recs.append({
                    "name": db_record["name"],
                    "cuisine": db_record["cuisines"],
                    "rating": db_record["rating_number"],
                    "cost_for_two": db_record["average_cost_for_two"],
                    "currency": db_record["currency"],
                    "ai_explanation": item.get("ai_explanation")
                })
            elif name_key in seen_names:
                print(f"Deduplication: Skipped duplicate suggestion '{item.get('name')}'")
            else:
                print(f"Hallucination Guard: Discarded LLM hallucinated suggestion '{item.get('name')}'")
                
        # If the LLM returned nothing or all items were filtered out, run DB fallback
        if not validated_recs:
            print("Warning: No valid suggestions returned by LLM. Using database fallback.")
            return _build_db_only_fallback(candidates, user_prefs, "Empty or hallucinated LLM response.", relaxed_reason)
            
        # Re-index the validated recommendations so that they are always 1, 2, 3...
        for idx, rec in enumerate(validated_recs):
            rec["rank"] = idx + 1
            
        return {
            "user_context": user_prefs,
            "fallback_mode": False,
            "query_relaxed": relaxed_reason,
            "recommendations": validated_recs
        }
        
    except Exception as e:
        print(f"Error executing AI personalizer: {e}. Falling back to Database-Only Mode.")
        return _build_db_only_fallback(candidates, user_prefs, f"API Exception: {str(e)}", relaxed_reason)

def _build_db_only_fallback(candidates, user_prefs, reason, relaxed_reason=None):
    """
    Constructs a structured recommendation payload directly from database records,
    providing direct database results when the LLM is offline or fails.
    """
    fallback_recs = []
    # Grab the top 3 database candidates directly (already sorted by rating/votes)
    for idx, r in enumerate(candidates[:3]):
        # Construct standard database description
        explanation = (
            f"Recommended based on your matching criteria of {r['cuisines']} food in {r['location']}. "
            f"This restaurant has a rating of {r['rating_number']} and average cost of {r['currency']}{r['average_cost_for_two']} for two."
        )
        fallback_recs.append({
            "rank": idx + 1,
            "name": r["name"],
            "cuisine": r["cuisines"],
            "rating": r["rating_number"],
            "cost_for_two": r["average_cost_for_two"],
            "currency": r["currency"],
            "ai_explanation": explanation
        })
        
    return {
        "user_context": user_prefs,
        "fallback_mode": True,
        "fallback_reason": reason,
        "query_relaxed": relaxed_reason,
        "recommendations": fallback_recs
    }
