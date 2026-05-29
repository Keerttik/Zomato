import csv
import os
import sys
import json
import urllib.request
import re

# Increase CSV limit for large fields
csv.field_size_limit(10 * 1024 * 1024)

# Import config
try:
    import config
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import config

# Import DB repository
try:
    from db.repository import init_db, insert_restaurants
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from db.repository import init_db, insert_restaurants

def download_raw_dataset():
    """Downloads raw zomato.csv from Hugging Face if it doesn't exist locally."""
    url = f"https://huggingface.co/datasets/{config.DATASET_NAME}/resolve/main/zomato.csv"
    dest_path = os.path.join(config.DATA_DIR, "zomato.csv")
    
    if os.path.exists(dest_path):
        print(f"Raw dataset already exists at {dest_path}. Skipping download.")
        return dest_path
        
    print(f"Downloading raw dataset from: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            with open(dest_path, "wb") as f:
                chunk_size = 1024 * 1024
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
        print("Download completed successfully.")
        return dest_path
    except Exception as e:
        print(f"Error downloading raw dataset: {e}")
        # Try local seed CSV if available
        seed_path = os.path.join(config.DATA_DIR, "raw_seed.csv")
        if os.path.exists(seed_path):
            print(f"Using local seed file: {seed_path}")
            return seed_path
        raise e

def clean_rate(rate_str):
    """
    Cleans rating strings into float.
    Examples: '4.1/5' -> 4.1, 'NEW' -> 0.0, '-' -> 0.0, None -> 0.0
    """
    if not rate_str:
        return 0.0
    rate_str = rate_str.strip()
    if rate_str in ("NEW", "-", ""):
        return 0.0
    # Match something like "4.1/5" or just "4.1"
    match = re.match(r"^([0-9.]+)\s*/\s*5", rate_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    try:
        return float(rate_str)
    except ValueError:
        return 0.0

def get_rating_text(rating):
    """Maps float rating to qualitative rating text."""
    if rating >= 4.5:
        return "Excellent"
    elif rating >= 4.0:
        return "Very Good"
    elif rating >= 3.5:
        return "Good"
    elif rating >= 2.5:
        return "Average"
    elif rating > 0.0:
        return "Poor"
    else:
        return "Not Rated"

def clean_cost(cost_str):
    """
    Cleans approximate cost string into integer.
    Example: '1,200' -> 1200, None -> 500 (default)
    """
    if not cost_str:
        return 500
    cost_str = cost_str.strip().replace(",", "")
    try:
        return int(cost_str)
    except ValueError:
        # Try extracting numbers
        numbers = re.findall(r"\d+", cost_str)
        if numbers:
            return int("".join(numbers))
        return 500

def clean_boolean(val_str):
    """Converts yes/no strings to integer boolean representation (1 or 0)."""
    if not val_str:
        return 0
    val_str = val_str.strip().lower()
    return 1 if val_str == "yes" else 0

def clean_votes(votes_str):
    """Converts votes string to integer."""
    if not votes_str:
        return 0
    try:
        return int(votes_str.strip())
    except ValueError:
        return 0

def preprocess_data(raw_csv_path):
    """Reads raw CSV, sanitizes data rows, and exports a cleaned JSON file."""
    clean_json_path = os.path.join(config.DATA_DIR, "zomato_clean.json")
    print(f"Preprocessing raw dataset: {raw_csv_path} -> {clean_json_path}")
    
    cleaned_records = []
    try:
        with open(raw_csv_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                name = row.get("name", "").strip()
                location = row.get("location", "").strip()
                cuisines = row.get("cuisines", "").strip()
                
                # Filter out records missing vital identification fields
                if not name or not location:
                    continue
                
                if not cuisines:
                    cuisines = "Various"
                
                rating_num = clean_rate(row.get("rate"))
                rating_txt = get_rating_text(rating_num)
                avg_cost = clean_cost(row.get("approx_cost(for two people)"))
                votes = clean_votes(row.get("votes"))
                has_delivery = clean_boolean(row.get("online_order"))
                has_booking = clean_boolean(row.get("book_table"))
                
                record = {
                    "name": name,
                    "location": location,
                    "cuisines": cuisines,
                    "average_cost_for_two": avg_cost,
                    "currency": "Rs.",
                    "has_table_booking": has_booking,
                    "has_online_delivery": has_delivery,
                    "rating_number": rating_num,
                    "rating_text": rating_txt,
                    "votes": votes
                }
                cleaned_records.append(record)
                
        # Write clean data to JSON staging file
        with open(clean_json_path, "w", encoding="utf-8") as out:
            json.dump(cleaned_records, out, indent=2)
            
        print(f"Preprocess successful! Extracted {len(cleaned_records)} valid records.")
        return clean_json_path
        
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        raise e

def main():
    print("=== STARTING PHASE 1: DATA INGESTION ===")
    try:
        raw_csv = download_raw_dataset()
        clean_json_path = preprocess_data(raw_csv)
        print("=== PHASE 1 COMPLETED SUCCESSFULLY ===")
        
        print("\n=== STARTING PHASE 2: DATABASE MIGRATION ===")
        # Initialize DB tables and indexes
        init_db()
        
        # Load clean records from JSON staging file
        print(f"Loading cleaned records from: {clean_json_path}")
        with open(clean_json_path, "r", encoding="utf-8") as f:
            cleaned_records = json.load(f)
            
        # Bulk insert into database
        insert_restaurants(cleaned_records)
        print("=== PHASE 2 COMPLETED SUCCESSFULLY ===")
    except Exception as e:
        print(f"=== MIGRATION FAILED: {e} ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
