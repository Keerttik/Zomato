import sqlite3
import os
import sys

# Import config and models
try:
    import config
    from db.models import CREATE_RESTAURANTS_TABLE_SQL, CREATE_INDEXES_SQL
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config
    from db.models import CREATE_RESTAURANTS_TABLE_SQL, CREATE_INDEXES_SQL

def get_connection():
    """Returns a connection to the SQLite database."""
    os.makedirs(os.path.dirname(config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the SQLite database tables and indexes."""
    print(f"Initializing database at: {config.DATABASE_PATH}")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CREATE_RESTAURANTS_TABLE_SQL)
        for index_sql in CREATE_INDEXES_SQL:
            cursor.execute(index_sql)
        conn.commit()
    print("Database initialization complete.")

def insert_restaurants(restaurants_list):
    """
    Bulk inserts a list of restaurant dictionaries into the database.
    Uses executemany for optimal speed.
    """
    if not restaurants_list:
        return
        
    query = """
    INSERT INTO restaurants (
        name, location, cuisines, average_cost_for_two, currency,
        has_table_booking, has_online_delivery, rating_number, rating_text, votes
    ) VALUES (
        :name, :location, :cuisines, :average_cost_for_two, :currency,
        :has_table_booking, :has_online_delivery, :rating_number, :rating_text, :votes
    )
    """
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(query, restaurants_list)
        conn.commit()
    print(f"Successfully inserted {len(restaurants_list)} records into database.")

def get_distinct_filters():
    """
    Retrieves all unique locations and individual cuisines from the database.
    """
    locations = []
    cuisines = set()
    
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Get distinct locations
        cursor.execute("SELECT DISTINCT location FROM restaurants ORDER BY location ASC")
        locations = [row['location'] for row in cursor.fetchall() if row['location']]
        
        # Get distinct cuisines by parsing comma separated strings
        cursor.execute("SELECT DISTINCT cuisines FROM restaurants")
        for row in cursor.fetchall():
            cuis_str = row['cuisines']
            if cuis_str:
                for c in cuis_str.split(","):
                    c_clean = c.strip()
                    if c_clean:
                        cuisines.add(c_clean)
                        
    return {
        "locations": locations,
        "cuisines": sorted(list(cuisines))
    }
