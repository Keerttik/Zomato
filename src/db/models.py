from dataclasses import dataclass, asdict

# SQL Schema creation query
CREATE_RESTAURANTS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    cuisines TEXT NOT NULL,
    average_cost_for_two INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'Rs.',
    has_table_booking INTEGER NOT NULL DEFAULT 0,
    has_online_delivery INTEGER NOT NULL DEFAULT 0,
    rating_number REAL NOT NULL DEFAULT 0.0,
    rating_text TEXT NOT NULL DEFAULT 'Not Rated',
    votes INTEGER NOT NULL DEFAULT 0
);
"""

# Indexes for fast querying
CREATE_INDEXES_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_location ON restaurants (location);",
    "CREATE INDEX IF NOT EXISTS idx_cuisines ON restaurants (cuisines);",
    "CREATE INDEX IF NOT EXISTS idx_rating ON restaurants (rating_number);"
]

@dataclass
class RestaurantModel:
    name: str
    location: str
    cuisines: str
    average_cost_for_two: int
    currency: str = "Rs."
    has_table_booking: int = 0
    has_online_delivery: int = 0
    rating_number: float = 0.0
    rating_text: str = "Not Rated"
    votes: int = 0
    id: int = None

    def to_dict(self):
        return asdict(self)
