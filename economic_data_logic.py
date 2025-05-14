# economic_data_logic.py

import pandas as pd
from datetime import datetime, timedelta
import random

# As per Framework Part 2, Sec 19.2: GDP Growth Rate, IIP, CPI Inflation, Core Sector Growth,
# Bank Credit Growth, Unemployment Rate, Foreign Exchange Reserves, INR Depreciation,
# GST Collections, Automobile Sales, Stock Market Performance, Rural Demand, Global Economic Indicators.

# For now, we will use mock data generation.
# In a real scenario, this module would contain functions to fetch data from:
# - Government APIs (e.g., data.gov.in, RBI, MOSPI) - check for free tiers/public access.
# - Reliable public data sources (ethical scraping if APIs are not available/paid, respecting terms of service).

INDICATOR_NAMES = [
    "gdp_growth_rate", "iip_growth", "cpi_inflation", "core_sector_growth",
    "bank_credit_growth", "unemployment_rate", "forex_reserves_usd_billion",
    "inr_usd_exchange_rate", "gst_collections_inr_lakh_crore", "automobile_sales_units",
    "stock_market_index_points", "rural_demand_indicator_value", "global_economic_indicator_value"
]

def generate_mock_economic_data(start_date_str="2023-01-01", num_months=24) -> pd.DataFrame:
    """
    Generates a DataFrame of mock monthly economic data.
    Aligns with the 'monthly_economic_summary' table structure.
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    dates = [start_date + timedelta(days=30 * i) for i in range(num_months)]
    data_list = []

    base_values = {
        "gdp_growth_rate": 7.0, "iip_growth": 5.0, "cpi_inflation": 5.5,
        "core_sector_growth": 6.0, "bank_credit_growth": 15.0, "unemployment_rate": 7.5,
        "forex_reserves_usd_billion": 600.0, "inr_usd_exchange_rate": 82.0,
        "gst_collections_inr_lakh_crore": 1.5, "automobile_sales_units": 300000,
        "stock_market_index_points": 65000, "rural_demand_indicator_value": 100,
        "global_economic_indicator_value": 50
    }

    for dt in dates:
        month_data = {"data_month": dt.strftime("%Y-%m-%d")}
        for indicator in INDICATOR_NAMES:
            base = base_values.get(indicator, 0)
            # Add some random variation and slight trend
            variation_factor = 1 + (random.uniform(-0.1, 0.1)) # +/- 10% variation
            trend_factor = 1 + ( (dt - start_date).days / (30 * num_months) ) * random.uniform(-0.05, 0.05) # slight trend over time
            value = base * variation_factor * trend_factor
            
            if indicator in ["forex_reserves_usd_billion", "automobile_sales_units", "stock_market_index_points", "rural_demand_indicator_value", "global_economic_indicator_value", "gst_collections_inr_lakh_crore"]:
                month_data[indicator] = round(value, 2)
            elif indicator == "inr_usd_exchange_rate":
                 month_data[indicator] = round(value, 2)
            else: # Percentage based indicators
                month_data[indicator] = round(value, 1)
        data_list.append(month_data)
    
    df = pd.DataFrame(data_list)
    df["data_month"] = pd.to_datetime(df["data_month"])
    df = df.sort_values(by="data_month", ascending=False).reset_index(drop=True)
    return df

# Placeholder for database interaction (to be implemented in main app or DB layer)
# For now, this module will just generate and return data.

ECONOMIC_DATA_CACHE = None

def get_economic_data(refresh_cache=False) -> pd.DataFrame:
    """Fetches economic data, using a simple cache."""
    global ECONOMIC_DATA_CACHE
    if ECONOMIC_DATA_CACHE is None or refresh_cache:
        # In a real app, this would fetch from DB, which is populated by a scheduled job
        # that calls data source APIs or scrapers.
        ECONOMIC_DATA_CACHE = generate_mock_economic_data(num_months=36) # Generate 3 years of data
    return ECONOMIC_DATA_CACHE

def get_latest_economic_data() -> pd.Series | None:
    """Returns the most recent row of economic data."""
    df = get_economic_data()
    if not df.empty:
        return df.iloc[0]
    return None

def get_historical_trend(indicator_name: str, months: int = 12) -> pd.DataFrame:
    """Returns historical data for a specific indicator for trend analysis."""
    if indicator_name not in INDICATOR_NAMES:
        raise ValueError(f"Invalid indicator name: {indicator_name}. Valid names are: {INDICATOR_NAMES}")
    df = get_economic_data()
    if df.empty or indicator_name not in df.columns:
        return pd.DataFrame()
    
    # Ensure data_month is datetime for sorting, then select recent months
    df_sorted = df.sort_values(by="data_month", ascending=False)
    trend_df = df_sorted[["data_month", indicator_name]].head(months)
    return trend_df.sort_values(by="data_month") # Sort back to ascending for plotting

# --- AI Placeholder Functions (to be developed further) ---
def generate_ai_forecast(indicator_name: str, historical_data: pd.DataFrame) -> str:
    """Placeholder for AI-driven forecast."""
    if historical_data.empty:
        return "Not enough data for forecast."
    # Simple trend extrapolation placeholder
    try:
        latest_value = historical_data[indicator_name].iloc[-1]
        previous_value = historical_data[indicator_name].iloc[-2] if len(historical_data) > 1 else latest_value
        trend = latest_value - previous_value
        forecast_value = latest_value + trend
        return f"Simple forecast: {forecast_value:.2f} (based on recent trend)"
    except Exception:
        return "Forecast unavailable."

def check_early_warning_triggers(latest_data: pd.Series) -> list:
    """Placeholder for checking early warning triggers."""
    warnings = []
    if latest_data is None:
        return warnings

    # Example triggers (Framework Part 2, Sec 19.4)
    if latest_data.get("gdp_growth_rate", 100) < 4.0:
        warnings.append(f"Warning: GDP Growth Rate is low ({latest_data['gdp_growth_rate']}%). Possible economic slowdown.")
    if latest_data.get("iip_growth", 100) < 2.0:
        warnings.append(f"Warning: IIP Growth is low ({latest_data['iip_growth']}%). Consider impact on industrial sector.")
    if latest_data.get("cpi_inflation", 0) > 6.0:
        warnings.append(f"Warning: CPI Inflation is high ({latest_data['cpi_inflation']}%). May impact purchasing power.")
    # Add more triggers as per framework
    return warnings

if __name__ == "__main__":
    print("--- Test Economic Data Logic ---")
    latest_data = get_latest_economic_data()
    if latest_data is not None:
        print("\nLatest Economic Data:")
        print(latest_data)

    print("\nHistorical GDP Growth (12 months):")
    gdp_trend = get_historical_trend("gdp_growth_rate", 12)
    print(gdp_trend)

    if not gdp_trend.empty:
        print("\nAI Forecast for GDP Growth:")
        forecast = generate_ai_forecast("gdp_growth_rate", gdp_trend)
        print(forecast)

    if latest_data is not None:
        print("\nEarly Warning Triggers:")
        warnings = check_early_warning_triggers(latest_data)
        if warnings:
            for warning in warnings:
                print(warning)
        else:
            print("No early warnings triggered.")

    # Test fetching all data
    # all_data = get_economic_data()
    # print(f"\nTotal {len(all_data)} months of data generated.")
    # print(all_data.head())

