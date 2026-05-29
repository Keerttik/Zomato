from db.repository import get_distinct_filters
from services.filter_service import query_restaurants
import os
import sys

def main():
    print("=== TESTING DB FILTER ENGINE ===")
    
    # Test distinct filters
    print("\n1. Testing Distinct Filters Lookup:")
    filters = get_distinct_filters()
    locations = filters["locations"]
    cuisines = filters["cuisines"]
    print(f"Total Unique Locations: {len(locations)}")
    print(f"Total Unique Cuisines: {len(cuisines)}")
    print(f"Sample Locations: {locations[:5]}")
    print(f"Sample Cuisines: {cuisines[:5]}")
    
    # Test strict search
    print("\n2. Testing Strict Search (BTM, North Indian, 500-1500 Budget, 4.0 Rating):")
    results, relaxed_reason = query_restaurants(location="BTM", cuisine="North Indian", min_budget=500, max_budget=1500, min_rating=4.0)
    print(f"Strict search matched {len(results)} restaurants. (Relaxed: {relaxed_reason})")
    if results:
        print("First match sample:")
        print(f"  Name: {results[0]['name']}")
        print(f"  Location: {results[0]['location']}")
        print(f"  Cuisines: {results[0]['cuisines']}")
        print(f"  Rating: {results[0]['rating_number']}")
        print(f"  Cost for two: {results[0]['average_cost_for_two']}")
        
    # Test query relaxation
    print("\n3. Testing Query Relaxation (Searching for non-existent parameters):")
    results, relaxed_reason = query_restaurants(location="BTM", cuisine="French", min_budget=0, max_budget=500, min_rating=4.5)
    print(f"Relaxed search matched {len(results)} restaurants. (Relaxed: {relaxed_reason})")
    if results:
        print("First match sample from relaxed search:")
        print(f"  Name: {results[0]['name']}")
        print(f"  Location: {results[0]['location']}")
        print(f"  Cuisines: {results[0]['cuisines']}")
        print(f"  Rating: {results[0]['rating_number']}")

if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    main()
