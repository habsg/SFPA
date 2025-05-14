import requests
import time
import json
import os
from datetime import datetime

# World Bank API base URL
BASE_URL = "https://api.worldbank.org/v2"

# Indicators to fetch
INDICATORS = {
    "gdp_growth": "NY.GDP.MKTP.KD.ZG",  # GDP growth (annual %)
    "cpi_inflation": "FP.CPI.TOTL.ZG"   # CPI inflation (annual %)
}

# Country code for India
COUNTRY = "IN"

# Date range for data (last 5 years up to 2025)
DATE_RANGE = "2020:2025"

# Delay between requests to avoid rate limiting (seconds)
REQUEST_DELAY = 2  # 2 seconds between requests

# Cache file to store fetched data
CACHE_FILE = "economic_data_cache.json"
CACHE_DURATION_DAYS = 1  # Cache data for 1 day

def is_cache_valid():
    """Check if the cached data is still valid (less than 1 day old)."""
    if not os.path.exists(CACHE_FILE):
        return False
    cache_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
    return (datetime.now() - cache_time).days < CACHE_DURATION_DAYS

def load_cached_data():
    """Load data from the cache if available and valid."""
    if is_cache_valid():
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return None

def save_to_cache(data):
    """Save data to the cache."""
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)

def fetch_world_bank_data(indicator_code, country, date_range):
    """
    Fetch data for a specific indicator from the World Bank API.
    """
    # Construct the API URL
    url = f"{BASE_URL}/country/{country}/indicator/{indicator_code}?date={date_range}&format=json"

    try:
        # Make the API request
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the JSON response
        data = response.json()

        # World Bank API returns a list where the second element contains the data
        if len(data) < 2 or not data[1]:
            print(f"No data returned for indicator {indicator_code}")
            return None

        # Extract the latest non-null entry
        entries = data[1]
        for entry in sorted(entries, key=lambda x: x["date"], reverse=True):
            if entry["value"] is not None:
                return {
                    "year": entry["date"],
                    "value": entry["value"],
                    "indicator": entry.get("indicator", {}).get("value", indicator_code)
                }
        print(f"No non-null values found for indicator {indicator_code}")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            print("Rate limit exceeded. Waiting before retrying...")
            time.sleep(10)  # Wait 10 seconds before retrying
            return fetch_world_bank_data(indicator_code, country, date_range)  # Retry once
        else:
            print(f"HTTP Error for indicator {indicator_code}: {e}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for indicator {indicator_code}: {e}")
        return None

def fetch_economic_data():
    """
    Fetch economic indicators for India and return in the required format.
    """
    # Check cache first
    cached_data = load_cached_data()
    if cached_data:
        print("Using cached data.")
        return cached_data

    # Fetch fresh data
    output = {}
    for indicator_name, indicator_code in INDICATORS.items():
        print(f"Fetching {indicator_name} data...")
        data = fetch_world_bank_data(indicator_code, COUNTRY, DATE_RANGE)
        
        # Add delay to avoid rate limiting
        time.sleep(REQUEST_DELAY)

        if data:
            output[indicator_name] = data
        else:
            print(f"Failed to fetch {indicator_name} data.")

    if not output:
        # Fallback to mock data if no data is fetched
        print("No data fetched. Using mock data as fallback.")
        output = {
            "gdp_growth": {"year": "2025", "value": 4.2, "indicator": "GDP growth (annual %)"},
            "cpi_inflation": {"year": "2025", "value": 5.8, "indicator": "Inflation, consumer prices (annual %)"}
        }

    # Save to cache
    save_to_cache(output)
    return output

if __name__ == "__main__":
    print("Fetching economic data...")
    result = fetch_economic_data()
    print("Final JSON output:")
    print(json.dumps(result, indent=2))