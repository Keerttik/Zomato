import os
import sys

# Import config and repository
try:
    import config
    from db.repository import get_connection
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config
    from db.repository import get_connection

def query_restaurants(location=None, cuisine=None, min_budget=None, max_budget=None, min_rating=0.0):
    """
    Queries the SQLite database for restaurants matching the user parameters.
    Implements cascading query relaxation as per the edge-case handling strategy
    if initial strict queries return no matches.
    Returns:
        tuple: (list of matching restaurants, relaxed_reason string or None)
    """
    
    # 1. Try strict matching query
    results = _execute_restaurant_query(location, cuisine, min_budget, max_budget, min_rating)
    if results:
        print(f"Strict query matched {len(results)} restaurants.")
        return results, None
        
    # Edge case mitigation: Cascading query relaxation
    print("Strict query yielded 0 results. Relaxing search criteria...")
    
    # Relaxation step 1: Lower minimum rating threshold (to 0.0)
    if min_rating > 0.0:
        print("Relaxation 1: Dropping minimum rating constraint...")
        results = _execute_restaurant_query(location, cuisine, min_budget, max_budget, 0.0)
        if results:
            return results, "rating"

    # Relaxation step 2: Search using only the location parameter (preserve budget)
    print("Relaxation 2: Dropping cuisine search and matching location only...")
    results = _execute_restaurant_query(location, None, min_budget, max_budget, 0.0)
    if results:
        return results, "cuisine"

    # Return empty list if absolutely nothing matches location
    print("No matching restaurants found even after query relaxation.")
    return [], None

def _execute_restaurant_query(location=None, cuisine=None, min_budget=None, max_budget=None, min_rating=0.0):
    """Executes the raw SQL query against SQLite, respecting config limits."""
    query = "SELECT * FROM restaurants WHERE 1=1"
    params = []
    
    # Filter by Location (exact OR prefix matching to support sub-blocks)
    if location:
        query += " AND (LOWER(location) = LOWER(?) OR LOWER(location) LIKE ?)"
        params.append(location.strip())
        params.append(f"{location.strip().lower()}%")
        
    # Filter by Cuisine (substring check, case-insensitive)
    if cuisine:
        query += " AND LOWER(cuisines) LIKE ?"
        params.append(f"%{cuisine.strip().lower()}%")
        
    # Filter by Budget Range
    if min_budget is not None:
        query += " AND average_cost_for_two >= ?"
        params.append(int(min_budget))
    if max_budget is not None and int(max_budget) < 2000:
        query += " AND average_cost_for_two <= ?"
        params.append(int(max_budget))
            
    # Filter by Minimum Rating
    if min_rating > 0.0:
        # Clamp rating inputs to [0.0, 5.0]
        clamped_rating = max(0.0, min(5.0, float(min_rating)))
        query += " AND rating_number >= ?"
        params.append(clamped_rating)
        
    # Order by rating and number of votes to prioritize popular/highly-rated ones
    # Limits output based on config candidate limit
    query += " ORDER BY rating_number DESC, votes DESC LIMIT ?"
    params.append(config.CANDIDATE_LIMIT)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
    return [dict(row) for row in rows]
