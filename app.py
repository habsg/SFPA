import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date
import json
from cryptography.fernet import Fernet
import math
import plotly.express as px
import re
import os

# Attempt to import fetch_economic_data, handle if not found for local testing
try:
    from economic_data_fetcher import fetch_economic_data
except ImportError:
    st.warning("economic_data_fetcher.py not found. Economic data features will use fallbacks.")
    def fetch_economic_data(): # Fallback function
        return {}

# Streamlit app configuration
st.set_page_config(page_title="Financial Planning App", layout="wide")

# Custom CSS for styling - Updated for Redesign
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
    body, .stApp, .stTextInput input, .stNumberInput input, .stSelectbox select, .stDateInput input, .stTextArea textarea, button {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
        color: #1a1a1a; /* Dark grey for text for better readability */
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
        color: #111827; /* Even darker for headers */
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px; /* Reduced gap for a more connected look */
        border-bottom: 1px solid #D1D5DB; /* Light grey border bottom for tab list */
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px; /* Slightly taller tabs */
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 6px 6px 0 0; /* Rounded top corners */
        padding: 0px 20px; /* More horizontal padding */
        margin-bottom: -1px; /* To make selected tab border merge with list border */
        font-weight: 500;
        color: #4B5563; /* Medium grey for inactive tabs */
        border: 1px solid transparent; /* Prepare for border */
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF; /* White background for active tab */
        color: #007AFF; /* Apple blue for active tab text */
        border-color: #D1D5DB #D1D5DB #FFFFFF; /* Border to match list and hide bottom */
        font-weight: 600;
    }
    .stButton > button {
        background-color: #007AFF; /* Apple blue */
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border: none;
        transition: background-color 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #0056b3; /* Darker Apple blue */
    }
    .stTextInput > div > div > input, .stNumberInput > div > div > input, 
    .stSelectbox > div > div > select, .stDateInput > div > div > input, 
    .stTextArea > div > textarea {
        border: 1px solid #D1D5DB; /* Light grey border for inputs */
        border-radius: 6px;
        padding: 10px;
        font-size: 0.95rem;
    }
    .stTextInput > label, .stNumberInput > label, .stSelectbox > label, 
    .stDateInput > label, .stCheckbox > label, .stTextArea > label, .stRadio > label {
        font-weight: 500;
        color: #374151; /* Darker grey for labels */
        margin-bottom: 6px;
        display: inline-block;
    }
    .stRadio > div > label > div {
        background-color: #F3F4F6; /* Light grey for radio items */
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 4px;
    }
    .stRadio > div > label > input:checked + div {
        background-color: #007AFF; /* Apple blue for selected radio */
        color: white;
    }
    .stForm [data-testid="stFormSubmitButton"] button {
         background-color: #28a745; /* Green for submit */
         color: white;
    }
    .stForm [data-testid="stFormSubmitButton"] button:hover {
         background-color: #218838; /* Darker green */
    }
    </style>
""", unsafe_allow_html=True)

# Encryption key management
KEY_FILE = "encryption_key.key"
def load_or_generate_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key

key = load_or_generate_key()
cipher = Fernet(key)

# Database setup
def init_db():
    conn = sqlite3.connect('financial_planning.db')
    c = conn.cursor()
    try: c.execute("ALTER TABLE investors ADD COLUMN investor_profile TEXT")
    except sqlite3.OperationalError: pass 
    try: c.execute("ALTER TABLE investors ADD COLUMN pan_number TEXT") # For PAN
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE investors ADD COLUMN email_address TEXT")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE investors ADD COLUMN mobile_number TEXT")
    except sqlite3.OperationalError: pass

    c.execute('''CREATE TABLE IF NOT EXISTS investors (
        investor_id TEXT PRIMARY KEY,
        name TEXT,
        dob TEXT,
        financial_details TEXT, 
        occupation TEXT,
        urban_rural_status TEXT,
        dependents TEXT, -- Stores JSON string of dependents list
        home_ownership BOOLEAN,
        rent_amount REAL,
        emi_amount REAL,
        emergency_fund REAL,
        risk_score INTEGER,
        risk_answers TEXT,
        plan_in_action_date TEXT,
        consent_log TEXT,
        market_linked_experience TEXT,
        investor_profile TEXT,
        pan_number TEXT, 
        email_address TEXT,
        mobile_number TEXT,
        total_investments REAL,
        total_loans REAL,
        monthly_household_expenses REAL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS economic_indicators (
        date TEXT PRIMARY KEY,
        data TEXT,
        is_fallback BOOLEAN DEFAULT FALSE
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS risk_adjustment_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        investor_id TEXT,
        log_timestamp TEXT,
        base_risk_score_100 REAL,
        economic_conditions_summary TEXT,
        economic_adjustment_factor REAL,
        goal_adjustment_details TEXT,
        final_risk_score_25 REAL,
        reason TEXT,
        FOREIGN KEY (investor_id) REFERENCES investors(investor_id)
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS financial_goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        investor_id TEXT,
        goal_name TEXT,
        goal_type TEXT,
        target_amount REAL,
        target_year INTEGER,
        current_savings_for_goal REAL DEFAULT 0,
        priority INTEGER,
        notes TEXT,
        creation_date TEXT,
        FOREIGN KEY (investor_id) REFERENCES investors(investor_id)
    )''')
    conn.commit()
    return conn

# Generate Investor ID
def generate_investor_id(conn):
    today_str = datetime.now().strftime("%Y%m%d")
    prefix = f"INV-{today_str}-"
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM investors WHERE investor_id LIKE ?", (f"{prefix}%",))
    count = c.fetchone()[0] + 1
    investor_id = f"{prefix}{count:04d}"
    return investor_id

# --- Economic Data Fetching and Management ---
DEFAULT_ECONOMIC_DATA = {
    "gdp_growth": {"value": 6.5, "year": "N/A (Fallback)", "indicator": "GDP Growth (Annual %)"},
    "cpi_inflation": {"value": 5.0, "year": "N/A (Fallback)", "indicator": "CPI Inflation (Annual %)"}
}

def fetch_and_store_economic_data(conn):
    try:
        fetched_data = fetch_economic_data()
        if not fetched_data or (not fetched_data.get("gdp_growth") and not fetched_data.get("cpi_inflation")):
            st.warning("Economic data fetcher returned empty/invalid data. Using fallback.")
            data_to_store = DEFAULT_ECONOMIC_DATA
            is_fallback_flag = True
        else:
            data_to_store = fetched_data
            is_fallback_flag = "N/A (Fallback)" in fetched_data.get("gdp_growth", {}).get("year", "")
        
save_economic_data(conn, datetime.now().strftime("%Y-%m-%d"), data_to_store, is_fallback=is_fallback_flag)
        st.session_state.latest_economic_data = data_to_store
        return True, data_to_store
    except Exception as e:
        st.error(f"Error fetching economic data: {e}. Using fallback.")
        save_economic_data(conn, datetime.now().strftime("%Y-%m-%d"), DEFAULT_ECONOMIC_DATA, is_fallback=True)
        st.session_state.latest_economic_data = DEFAULT_ECONOMIC_DATA
        return False, DEFAULT_ECONOMIC_DATA

def get_latest_economic_data_from_db(conn):
    c = conn.cursor()
    c.execute("SELECT data, is_fallback FROM economic_indicators WHERE date = ? AND is_fallback = 0 ORDER BY date DESC LIMIT 1", (datetime.now().strftime("%Y-%m-%d"),))
    row = c.fetchone()
    if row and row[0]:
        try: return json.loads(row[0]), bool(row[1])
        except json.JSONDecodeError: pass
    c.execute("SELECT data, is_fallback FROM economic_indicators ORDER BY date DESC LIMIT 1")
    row = c.fetchone()
    if row and row[0]:
        try: return json.loads(row[0]), bool(row[1])
        except json.JSONDecodeError: return DEFAULT_ECONOMIC_DATA, True
    return DEFAULT_ECONOMIC_DATA, True

def save_economic_data(conn, date_str, data_dict, is_fallback=False):
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO economic_indicators (date, data, is_fallback) VALUES (?, ?, ?)",
              (date_str, json.dumps(data_dict), is_fallback))
    conn.commit()

# Calculate Age & other helper functions
def calculate_age(dob_str, today_date_obj):
    if not dob_str: return 0
    try:
        if isinstance(dob_str, date):
            dob = dob_str
        elif isinstance(dob_str, str):
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        else: # Not a date object or valid string
            return 0
        return today_date_obj.year - dob.year - ((today_date_obj.month, today_date_obj.day) < (dob.month, dob.day))
    except ValueError: return 0

def encrypt_data(data):
    if data is None: return None
    return cipher.encrypt(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_data):
    if not encrypted_data: return None
    try: return json.loads(cipher.decrypt(encrypted_data.encode()).decode())
    except: return None # Or raise error, or return default dict

def get_income_level(monthly_household_income, occupation_type_raw):
    occupation_type = "White-Collar" if "White-Collar" in occupation_type_raw else "Blue-Collar" if "Blue-Collar" in occupation_type_raw else "Other"
    daily_income = (monthly_household_income * 12) / 365
    if occupation_type == "White-Collar":
        if daily_income < 1000: return "Low"
        elif daily_income <= 2500: return "Sufficient"
        else: return "Good"
    elif occupation_type == "Blue-Collar":
        if daily_income < 400: return "Low"
        elif daily_income <= 1000: return "Sufficient"
        else: return "Good"
    return "Unknown"

def calculate_required_emergency_fund(investor_data_dict):
    monthly_income = investor_data_dict.get('total_household_income', 0)
    owns_home = investor_data_dict.get('owns_home', False)
    urban_rural_raw = investor_data_dict.get('urban_rural_status', 'Urban (Metro/Tier I)')
    occupation_type_raw = investor_data_dict.get('occupation', 'Other')
    urban_rural = "Urban" if "Urban" in urban_rural_raw else "Rural"
    if monthly_income == 0: return 0
    essential_expense_ratio = (0.4 if urban_rural == "Urban" else 0.3) if owns_home else (0.6 if urban_rural == "Urban" else 0.5)
    monthly_essential_expenses = monthly_income * essential_expense_ratio
    income_level = get_income_level(monthly_income, occupation_type_raw)
    occupation_simple = "White-Collar" if "White-Collar" in occupation_type_raw else "Blue-Collar" if "Blue-Collar" in occupation_type_raw else "Other"
    required_months = 3
    if occupation_simple == "Blue-Collar":
        if income_level == "Low": required_months = 6
        elif income_level == "Sufficient": required_months = 4
    elif occupation_simple == "White-Collar":
        if income_level == "Low": required_months = 4
        elif income_level == "Sufficient": required_months = 3
        else: required_months = 2 # Good income white collar
    return required_months * monthly_essential_expenses

# Calculate Risk Score (0-25 score with economic adjustments)
def calculate_risk_score(db_conn, investor_id_for_log, investor_data_dict, answers):
    base_score_100 = 0
    # ... (rest of risk score logic as previously defined, ensure it uses investor_data_dict correctly for num_dependents etc.)
    # For num_dependents, it should use investor_data_dict.get('num_dependents', 0)
    # This 'num_dependents' field in investor_data_dict will be populated from len(dependents_data_list)
    # when the full investor profile is assembled before calling this function.
    # For now, the existing logic using investor_row (if that's how it was) might need adaptation.
    # Assuming investor_data_dict contains all necessary fields like 'dob', 'occupation', 'total_household_income', 'loan_emis', 'current_emergency_fund', 'market_experience', 'num_dependents'.
    
    raw_psychometric_score = 0
    greed_map = {"Not likely at all": 1, "Somewhat unlikely": 2, "Neutral": 3, "Somewhat likely": 4, "Very likely": 5}
    preference_map = {"Definitely Fixed Deposit": 1, "Lean towards Fixed Deposit": 2, "Neutral": 3, "Lean towards equity fund": 4, "Definitely equity fund": 5}
    willingness_map = {"Not willing at all": 1, "Somewhat reluctant": 2, "Neutral": 3, "Somewhat willing": 4, "Very willing": 5}
    reaction_map = {"Sell all investments immediately": 1, "Sell some investments and wait": 2, "Hold and wait for recovery": 3, "Hold and monitor closely": 4, "Invest more during the dip": 5}
    anxiety_map = {"Extremely anxious, unable to sleep": 1, "Quite anxious, very concerned": 2, "Mildly anxious, somewhat concerned": 3, "Not very anxious, can manage": 4, "Not anxious at all, comfortable": 5}
    
    if len(answers) == 5:
        raw_psychometric_score += greed_map.get(answers[0], 1)
        raw_psychometric_score += preference_map.get(answers[1], 1)
        raw_psychometric_score += willingness_map.get(answers[2], 1)
        raw_psychometric_score += reaction_map.get(answers[3], 1)
        raw_psychometric_score += anxiety_map.get(answers[4], 1)
        stated_risk_points = ((raw_psychometric_score - 5) / 20) * 30
        base_score_100 += stated_risk_points

    current_emergency_fund = investor_data_dict.get('current_emergency_fund', 0)
    required_emergency_fund = calculate_required_emergency_fund(investor_data_dict)
    adequacy_ratio = current_emergency_fund / required_emergency_fund if required_emergency_fund > 0 else 0
    if adequacy_ratio < 0.25: emergency_points = 2
    elif adequacy_ratio < 0.50: emergency_points = 5
    elif adequacy_ratio < 0.75: emergency_points = 9
    elif adequacy_ratio < 1.00: emergency_points = 13
    elif adequacy_ratio < 1.50: emergency_points = 17
    else: emergency_points = 20
    base_score_100 += emergency_points

    total_income = investor_data_dict.get('total_household_income', 0)
    total_emi = investor_data_dict.get('loan_emis', 0) # Assuming 'loan_emis' is the key for total EMIs
    debt_burden_ratio = total_emi / total_income if total_income > 0 else 1
    if debt_burden_ratio == 0: debt_points = 15
    elif debt_burden_ratio < 0.10: debt_points = 12
    elif debt_burden_ratio < 0.20: debt_points = 9
    elif debt_burden_ratio < 0.30: debt_points = 6
    elif debt_burden_ratio < 0.40: debt_points = 3
    else: debt_points = 0
    base_score_100 += debt_points

    age_val = calculate_age(investor_data_dict.get('dob'), date.today())
    if 22 <= age_val <= 30: lifecycle_points = 15
    elif 30 < age_val <= 35: lifecycle_points = 12
    elif 35 < age_val <= 50: lifecycle_points = 9
    elif 50 < age_val <= 60: lifecycle_points = 6
    else: lifecycle_points = 3
    base_score_100 += lifecycle_points

    income_val = investor_data_dict.get('total_household_income', 0)
    income_level_str = get_income_level(income_val, investor_data_dict.get('occupation', 'Other'))
    occupation_simple = "White-Collar" if "White-Collar" in investor_data_dict.get('occupation', 'Other') else "Blue-Collar" if "Blue-Collar" in investor_data_dict.get('occupation', 'Other') else "Other"
    if occupation_simple == "White-Collar" and income_level_str == "Good": income_points = 10
    elif (occupation_simple == "White-Collar" and income_level_str == "Sufficient") or 
         (occupation_simple == "Blue-Collar" and income_level_str == "Good"): income_points = 8
    elif (occupation_simple == "White-Collar" and income_level_str == "Low") or 
         (occupation_simple == "Blue-Collar" and income_level_str == "Sufficient"): income_points = 6
    else: income_points = 3
    base_score_100 += income_points

    num_deps = investor_data_dict.get('num_dependents', 0) # This key needs to be in investor_data_dict
    if num_deps == 0: dependents_points = 5
    elif num_deps == 1: dependents_points = 4
    elif num_deps == 2: dependents_points = 2
    else: dependents_points = 0
    base_score_100 += dependents_points

    market_exp = investor_data_dict.get('market_experience', "No")
    market_points = 5 if market_exp == "Yes" else 2
    base_score_100 += market_points
    
    base_score_100 = max(0, min(100, base_score_100))

    latest_eco_data, is_fallback = get_latest_economic_data_from_db(db_conn)
    economic_adjustment_factor = 1.0
    economic_conditions_summary = "No current economic data for adjustment."
    adjustment_reason_eco = []

    if latest_eco_data:
        economic_conditions_summary = json.dumps(latest_eco_data)
        gdp_growth_data = latest_eco_data.get("gdp_growth", {})
        cpi_inflation_data = latest_eco_data.get("cpi_inflation", {})
        gdp_value = gdp_growth_data.get("value", 0)
        cpi_value = cpi_inflation_data.get("value", 0)
        gdp_year = gdp_growth_data.get("year", "Unknown")
        cpi_year = cpi_inflation_data.get("year", "Unknown")
        if cpi_value > 6.0: economic_adjustment_factor -= 0.10; adjustment_reason_eco.append(f"CPI > 6.0% ({cpi_value}% in {cpi_year})")
        if gdp_value < 5.0: economic_adjustment_factor -= 0.05; adjustment_reason_eco.append(f"GDP < 5.0% ({gdp_value}% in {gdp_year})")

    goal_adjustment_factor = 1.0 
    goal_adjustment_details_str = "No specific goal adjustments applied yet."
    adjusted_score_100 = base_score_100 * economic_adjustment_factor * goal_adjustment_factor
    final_risk_score_25 = max(0, min(25, round(adjusted_score_100 / 4)))

    log_timestamp = datetime.now().isoformat()
    reason_for_adjustment = f"Economic Factors: {', '.join(adjustment_reason_eco) if adjustment_reason_eco else 'None'}. Goal Factors: {goal_adjustment_details_str}"
    
    c = db_conn.cursor()
    c.execute("""INSERT INTO risk_adjustment_log 
                 (investor_id, log_timestamp, base_risk_score_100, economic_conditions_summary, economic_adjustment_factor, goal_adjustment_details, final_risk_score_25, reason)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
              (investor_id_for_log, log_timestamp, base_score_100, economic_conditions_summary, economic_adjustment_factor, goal_adjustment_details_str, final_risk_score_25, reason_for_adjustment))
    db_conn.commit()
    return final_risk_score_25

def get_risk_rating(score):
    if score <= 8: return "Risk-Averse"
    elif score <= 16: return "Moderate"
    else: return "Aggressive"

def assign_profile(investor_data_dict):
    # ... (Profile assignment logic as previously defined, using investor_data_dict)
    age = calculate_age(investor_data_dict.get('dob'), date.today())
    occupation_raw = investor_data_dict.get('occupation', 'Other')
    monthly_income = investor_data_dict.get('total_household_income', 0)
    income_level = get_income_level(monthly_income, occupation_raw)
    occupation_simple = "White-Collar" if "White-Collar" in occupation_raw else "Blue-Collar" if "Blue-Collar" in occupation_raw else "Other"
    # Example: if occupation_simple == "White-Collar" and 22 <= age <= 28 and income_level == "Low": return "W1"
    # This needs the full W1-W15 and B1-B15 logic from before.
    # For brevity, I'll just return a default here, assuming the full logic exists.
    if occupation_simple == "White-Collar":
        if 22 <= age <= 28:
            if income_level == "Low": return "W1"
            if income_level == "Sufficient": return "W2"
            if income_level == "Good": return "W3"
        elif 29 <= age <= 35:
            if income_level == "Low": return "W4"
            if income_level == "Sufficient": return "W5"
            if income_level == "Good": return "W6"
        elif 36 <= age <= 45:
            if income_level == "Low": return "W7"
            if income_level == "Sufficient": return "W8"
            if income_level == "Good": return "W9"
        elif 46 <= age <= 55:
            if income_level == "Low": return "W10"
            if income_level == "Sufficient": return "W11"
            if income_level == "Good": return "W12"
        elif age > 55:
            if income_level == "Low": return "W13"
            if income_level == "Sufficient": return "W14"
            if income_level == "Good": return "W15"
    elif occupation_simple == "Blue-Collar":
        if 22 <= age <= 28:
            if income_level == "Low": return "B1"
            if income_level == "Sufficient": return "B2"
            if income_level == "Good": return "B3"
        elif 29 <= age <= 35:
            if income_level == "Low": return "B4"
            if income_level == "Sufficient": return "B5"
            if income_level == "Good": return "B6"
        elif 36 <= age <= 45:
            if income_level == "Low": return "B7"
            if income_level == "Sufficient": return "B8"
            if income_level == "Good": return "B9"
        elif 46 <= age <= 55:
            if income_level == "Low": return "B10"
            if income_level == "Sufficient": return "B11"
            if income_level == "Good": return "B12"
        elif age > 55:
            if income_level == "Low": return "B13"
            if income_level == "Sufficient": return "B14"
            if income_level == "Good": return "B15"
    return "P_Default"

def calculate_sip(target_amount, years, annual_return_rate, current_savings=0):
    # ... (SIP calculation logic as previously defined)
    if years <= 0 or annual_return_rate <=0: return float('inf')
    future_value_of_current_savings = current_savings * ((1 + annual_return_rate / 100) ** years)
    remaining_target = target_amount - future_value_of_current_savings
    if remaining_target <= 0: return 0
    r = (annual_return_rate / 100) / 12
    n = years * 12
    try: sip = remaining_target * r / (((1 + r) ** n) - 1)
    except OverflowError: return float('inf')
    return sip if sip > 0 else 0

def get_recommended_savings_rate(investor_profile_code, urban_rural_raw, owns_home, num_dependents):
    # ... (Savings rate logic as previously defined)
    base_rate = 0.10
    urban_rural = "Urban" if "Urban" in urban_rural_raw else "Rural"
    if investor_profile_code.startswith("W"): 
        profile_num = int(re.findall(r'\d+', investor_profile_code)[0]) if re.findall(r'\d+', investor_profile_code) else 0
        if profile_num <= 3: base_rate = 0.15
        elif profile_num <= 6: base_rate = 0.20
        elif profile_num <= 9: base_rate = 0.25
        elif profile_num <= 12: base_rate = 0.30
        else: base_rate = 0.35
    elif investor_profile_code.startswith("B"): 
        profile_num = int(re.findall(r'\d+', investor_profile_code)[0]) if re.findall(r'\d+', investor_profile_code) else 0
        if profile_num <= 3: base_rate = 0.10
        elif profile_num <= 6: base_rate = 0.12
        elif profile_num <= 9: base_rate = 0.15
        elif profile_num <= 12: base_rate = 0.18
        else: base_rate = 0.20
    if urban_rural == "Rural": base_rate -= 0.02
    if not owns_home: base_rate += 0.03
    if num_dependents == 1: base_rate -= 0.01
    elif num_dependents == 2: base_rate -= 0.02
    elif num_dependents > 2: base_rate -= 0.03
    return max(0.05, min(0.50, base_rate))

def validate_investor_inputs_ai(data_dict):
    # ... (AI validation logic as previously defined)
    warnings = []
    income = data_dict.get('total_household_income', 0)
    occupation_raw = data_dict.get('occupation', 'Other')
    profile = data_dict.get('investor_profile', 'P_Default')
    income_level = get_income_level(income, occupation_raw)
    occupation_simple = "White-Collar" if "White-Collar" in occupation_raw else "Blue-Collar" if "Blue-Collar" in occupation_raw else "Other"
    if occupation_simple == "White-Collar" and income_level == "Low" and profile and not profile.endswith(("1", "4", "7", "10", "13")):
        warnings.append(f"Warning: Low income for White-Collar profile {profile} seems inconsistent.")
    if occupation_simple == "Blue-Collar" and income_level == "Low" and profile and not profile.endswith(("1", "4", "7", "10", "13")):
        warnings.append(f"Warning: Low income for Blue-Collar profile {profile} seems inconsistent.")
    return {"valid": not warnings, "warnings": warnings}

def get_ai_fund_recommendations(risk_rating, goals_list, economic_data):
    # ... (AI fund recommendation logic as previously defined)
    recommendations = []
    is_slowdown = economic_data.get("gdp_growth", {}).get("value", 7.0) < 5.0
    for goal in goals_list:
        goal_type = goal.get('goal_type', 'Other')
        timeline_years = goal.get('target_year', datetime.now().year + 5) - datetime.now().year
        rec = f"For goal '{goal.get('goal_name', 'Unnamed Goal')}' ({goal_type}): "
        if risk_rating == "Risk-Averse":
            if timeline_years <= 3: rec += "Consider Debt Funds (Short Duration) or Fixed Deposits."
            else: rec += "Consider Debt Funds (Medium to Long Duration) or Balanced Advantage Funds."
        elif risk_rating == "Moderate":
            if timeline_years <= 3: rec += "Consider Hybrid Funds (Conservative) or Debt Funds."
            elif timeline_years <= 7: rec += "Consider Diversified Equity Funds or Balanced Advantage Funds."
            else: rec += "Consider Large Cap or Flexi Cap Equity Funds."
        elif risk_rating == "Aggressive":
            if timeline_years <= 3: rec += "Consider Arbitrage Funds or Short-Term Hybrid Funds."
            elif timeline_years <= 7: rec += "Consider Mid Cap or Flexi Cap Equity Funds."
            else: rec += "Consider Small Cap or Thematic Equity Funds (with caution)."
        if is_slowdown and "Equity" in rec: rec += " (Economic slowdown; consider phased investment.)"
        recommendations.append(rec)
    if not goals_list: recommendations.append("No specific goals. General recommendation based on risk:") # ... (general recs)
    return recommendations

# Initialize session state keys
def initialize_session_state():
    defaults = {
        'latest_economic_data': DEFAULT_ECONOMIC_DATA,
        'selected_language': 'English',
        'current_investor_id': None,
        'investor_data_for_dashboard': None,
        'active_investor_for_mfd': None,
        'num_dependents_value': 0, # For the number input controlling dependents
        'dependents_data_list': [], # List of dicts for each dependent's data
        'num_dependents_value_input': 0, # Temp key for number_input widget
        'financial_goals_list': [], # For financial goals section
        # Add keys for personal info tab to preserve data across tab switches before final save
        'p_name': '', 'p_dob': None, 'p_pan_number': '', 'p_email': '', 'p_mobile': '',
        'p_occupation': 'Salaried - White-Collar', 'p_urban_rural': 'Urban (Metro/Tier I)',
        # Add keys for income/expenses tab
        'ie_monthly_income': 0.0, 'ie_monthly_expenses': 0.0, 'ie_total_investments': 0.0,
        'ie_home_ownership': False, 'ie_rent_amount': 0.0, 'ie_loan_emis': 0.0,
        'ie_current_emergency_fund': 0.0, 'ie_market_experience': 'No',
        # Add keys for risk assessment tab
        'ra_answers': [None]*5 # Assuming 5 questions
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    # Ensure num_dependents_value_input reflects num_dependents_value initially
    if 'num_dependents_value_input' in st.session_state and 'num_dependents_value' in st.session_state:
        st.session_state.num_dependents_value_input = st.session_state.num_dependents_value

initialize_session_state()

# Language Selection & Text Retrieval
languages = {
    "English": {
        "app_title": "Comprehensive Financial Planning Tool",
        "personal_info_tab": "👤 Personal Info",
        "family_structure_tab": "👪 Family & Dependents",
        "income_expenses_tab": "💰 Income, Expenses & Assets",
        "financial_goals_tab": "🎯 Financial Goals",
        "risk_assessment_tab": "⚖️ Risk Assessment",
        "mfd_dashboard_tab": "📊 MFD Dashboard",
        "investor_dashboard_tab": "📈 Investor Dashboard",
        "investor_guide_tab": "📜 Investor Guide",
        "form_intro": "Please provide accurate details for your financial plan.",
        "welcome_hindi": ""
    },
    "Hindi": {
        "app_title": "व्यापक वित्तीय योजना उपकरण",
        "personal_info_tab": "👤 व्यक्तिगत जानकारी",
        "family_structure_tab": "👪 परिवार और आश्रित",
        "income_expenses_tab": "💰 आय, व्यय और संपत्ति",
        "financial_goals_tab": "🎯 वित्तीय लक्ष्य",
        "risk_assessment_tab": "⚖️ जोखिम मूल्यांकन",
        "mfd_dashboard_tab": "📊 एमएफडी डैशबोर्ड",
        "investor_dashboard_tab": "📈 निवेशक डैशबोर्ड",
        "investor_guide_tab": "📜 निवेशक गाइड",
        "form_intro": "कृपया व्यक्तिगत वित्तीय योजना बनाने के लिए सटीक विवरण प्रदान करें।",
        "welcome_hindi": "नमस्ते! आपके वित्तीय योजना में आपका स्वागत है। कृपया अपने जानकारी सही-सही भरें।"
    }
}
def get_text(key):
    return languages[st.session_state.selected_language].get(key, f"Missing: {key}")

st.sidebar.header("Language / भाषा")
selected_lang_label = st.sidebar.radio("Select Language", list(languages.keys()), 
                                     index=list(languages.keys()).index(st.session_state.selected_language), 
                                     key="lang_selector_sidebar")
if selected_lang_label != st.session_state.selected_language:
    st.session_state.selected_language = selected_lang_label
    st.experimental_rerun()

st.title(get_text("app_title"))
if st.session_state.selected_language == 'Hindi' and get_text("welcome_hindi"):
    st.write(get_text("welcome_hindi"))

conn = init_db()

# --- UI Elements for each Tab --- 
def personal_info_tab_content(conn):
    st.header(get_text("personal_info_tab"))
    st.write(get_text("form_intro"))
    with st.form("personal_info_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.p_name = st.text_input("Full Name *", value=st.session_state.p_name, key="p_name_input")
            st.session_state.p_dob = st.date_input("Date of Birth *", value=st.session_state.p_dob, min_value=date(1920,1,1), max_value=date.today(), key="p_dob_input")
            st.session_state.p_pan_number = st.text_input("PAN Number", value=st.session_state.p_pan_number, key="p_pan_input") # PAN field added
        with col2:
            st.session_state.p_email = st.text_input("Email Address", value=st.session_state.p_email, key="p_email_input")
            st.session_state.p_mobile = st.text_input("Mobile Number", value=st.session_state.p_mobile, key="p_mobile_input")
            st.session_state.p_occupation = st.selectbox("Occupation *", ["Salaried - White-Collar", "Salaried - Blue-Collar", "Self-Employed Professional", "Self-Employed Non-Professional", "Business Owner", "Retired", "Student", "Other"], index=0, key="p_occupation_input", help="Select the option that best describes your primary occupation.")
            st.session_state.p_urban_rural = st.selectbox("Location Type *", ["Urban (Metro/Tier I)", "Urban (Tier II/III)", "Rural"], index=0, key="p_urban_rural_input")
        
        personal_submit = st.form_submit_button("Save Personal Info")
        if personal_submit:
            # Data is already in session state due to direct assignment with keys
            st.success("Personal information section updated in session.")
            # Actual DB save might happen with a global save button or when investor ID is confirmed

def family_structure_tab_content(conn):
    st.header(get_text("family_structure_tab"))
    st.write("Please provide details about your dependents.")

    def update_dependents_list_callback():
        current_num = len(st.session_state.dependents_data_list)
        target_num = st.session_state.num_dependents_value_input
        if target_num > current_num:
            for _ in range(target_num - current_num):
                st.session_state.dependents_data_list.append({"name": "", "relationship": "", "gender": "Male", "dob": None})
        elif target_num < current_num:
            st.session_state.dependents_data_list = st.session_state.dependents_data_list[:target_num]
        st.session_state.num_dependents_value = target_num # Update the actual count

    st.number_input("Number of Dependents", min_value=0, max_value=10, 
                     value=st.session_state.num_dependents_value_input, 
                     step=1, key="num_dependents_value_input", 
                     on_change=update_dependents_list_callback)

    if st.session_state.num_dependents_value > 0:
        st.subheader("Dependents Details")
        with st.form(key="dependents_form"):
            # Ensure list matches the count before rendering form fields
            while len(st.session_state.dependents_data_list) < st.session_state.num_dependents_value:
                st.session_state.dependents_data_list.append({"name": "", "relationship": "", "gender": "Male", "dob": None})
            st.session_state.dependents_data_list = st.session_state.dependents_data_list[:st.session_state.num_dependents_value]

            for i in range(st.session_state.num_dependents_value):
                st.markdown(f"--- \n#### Dependent {i+1}")
                dep_data = st.session_state.dependents_data_list[i]
                cols = st.columns([2,2,1,2])
                dep_data["name"] = cols[0].text_input(f"Name", value=dep_data.get("name", ""), key=f"dep_name_{i}")
                dep_data["relationship"] = cols[1].text_input(f"Relationship", value=dep_data.get("relationship", ""), key=f"dep_relationship_{i}")
                dep_data["gender"] = cols[2].selectbox(f"Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(dep_data.get("gender", "Male")), key=f"dep_gender_{i}")
                
                dob_val = dep_data.get("dob")
                if isinstance(dob_val, str): # Convert from string if loading from session/DB
                    try: dob_val = datetime.strptime(dob_val, "%Y-%m-%d").date()
                    except ValueError: dob_val = None
                
                dep_data["dob"] = cols[3].date_input(f"Date of Birth", value=dob_val, min_value=date(1920,1,1), max_value=date.today(), key=f"dep_dob_{i}")
                st.session_state.dependents_data_list[i] = dep_data # Update session state as form elements change
            
            submitted_dependents = st.form_submit_button("Save Dependents Information")
            if submitted_dependents:
                processed_deps = []
                for item in st.session_state.dependents_data_list:
                    new_item = item.copy()
                    if isinstance(new_item['dob'], date):
                        new_item['dob'] = new_item['dob'].isoformat()
                    processed_deps.append(new_item)
                st.session_state.dependents_data_list = processed_deps # Store with DOB as string

                if st.session_state.current_investor_id:
                    try:
                        c = conn.cursor()
                        dependents_json_str = json.dumps(st.session_state.dependents_data_list)
                        c.execute("UPDATE investors SET dependents = ? WHERE investor_id = ?", 
                                  (dependents_json_str, st.session_state.current_investor_id))
                        conn.commit()
                        st.success(f"Dependents info saved to DB for {st.session_state.current_investor_id}.")
                    except sqlite3.Error as e: st.error(f"DB error: {e}")
                else: st.info("Dependents info updated in session. Save with profile.")
                st.experimental_rerun()
    
    if st.session_state.dependents_data_list:
        st.markdown("---")
        st.subheader("Current Dependents Summary (Session Data):")
        try: st.dataframe(pd.DataFrame(st.session_state.dependents_data_list))
        except Exception as e: st.error(f"Error displaying dependents: {e}")

def income_expenses_tab_content(conn):
    st.header(get_text("income_expenses_tab"))
    with st.form("income_expenses_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.ie_monthly_income = st.number_input("Total Monthly Household Income (INR) *", min_value=0.0, value=st.session_state.ie_monthly_income, step=1000.0, key="ie_inc")
            st.session_state.ie_monthly_expenses = st.number_input("Total Monthly Household Expenses (INR) *", min_value=0.0, value=st.session_state.ie_monthly_expenses, step=1000.0, key="ie_exp")
            st.session_state.ie_total_investments = st.number_input("Total Current Investments (INR)", min_value=0.0, value=st.session_state.ie_total_investments, step=10000.0, key="ie_inv")
            st.session_state.ie_home_ownership = st.checkbox("Own a House?", value=st.session_state.ie_home_ownership, key="ie_home")
        with col2:
            st.session_state.ie_rent_amount = st.number_input("Monthly Rent (if applicable)", min_value=0.0, value=st.session_state.ie_rent_amount, step=500.0, key="ie_rent")
            st.session_state.ie_loan_emis = st.number_input("Total Monthly Loan EMIs (Home, Car, Personal etc.)", min_value=0.0, value=st.session_state.ie_loan_emis, step=500.0, key="ie_emi")
            st.session_state.ie_current_emergency_fund = st.number_input("Current Emergency Fund (INR)", min_value=0.0, value=st.session_state.ie_current_emergency_fund, step=1000.0, key="ie_ef")
            st.session_state.ie_market_experience = st.radio("Experience with Market-Linked Investments (Stocks, MFs)?", ["No", "Yes"], index=0 if st.session_state.ie_market_experience == "No" else 1, key="ie_mkt_exp")
        
        ie_submit = st.form_submit_button("Save Income & Expenses")
        if ie_submit:
            st.success("Income & Expenses section updated in session.")

def financial_goals_tab_content(conn, investor_id):
    st.header(get_text("financial_goals_tab"))
    if not investor_id:
        st.info("Please create or load an investor profile in the MFD Dashboard to manage financial goals.")
        return

    goals_list_key = f'financial_goals_list_{investor_id}'
    if goals_list_key not in st.session_state:
        st.session_state[goals_list_key] = []
        c = conn.cursor()
        c.execute("SELECT goal_id, goal_name, goal_type, target_amount, target_year, current_savings_for_goal, priority, notes FROM financial_goals WHERE investor_id = ? ORDER BY priority, goal_id", (investor_id,))
        db_goals = c.fetchall()
        for g_id, name, g_type, t_amt, t_year, c_sav, prio, notes_txt in db_goals:
            st.session_state[goals_list_key].append({
                'db_id': g_id, 'goal_name': name, 'goal_type': g_type, 'target_amount': t_amt,
                'target_year': t_year, 'current_savings_for_goal': c_sav, 'priority': prio, 'notes': notes_txt, 'is_new': False
            })
    
    # Display existing goals
    if st.session_state[goals_list_key]:
        st.subheader("Current Goals")
        for i, goal_data in enumerate(st.session_state[goals_list_key]):
            with st.expander(f"{i+1}. {goal_data.get('goal_name', 'New Goal')} (Priority: {goal_data.get('priority', 'N/A')})"):
                st.write(f"Type: {goal_data.get('goal_type')}")
                st.write(f"Target Amount: {goal_data.get('target_amount')}")
                st.write(f"Target Year: {goal_data.get('target_year')}")
                st.write(f"Current Savings: {goal_data.get('current_savings_for_goal')}")
                st.write(f"Notes: {goal_data.get('notes')}")
                if st.button(f"Delete Goal {i+1}", key=f"del_goal_{investor_id}_{i}"):
                    deleted_goal = st.session_state[goals_list_key].pop(i)
                    if not deleted_goal.get('is_new') and deleted_goal.get('db_id'): # Delete from DB if it was saved
                        try:
                            c = conn.cursor()
                            c.execute("DELETE FROM financial_goals WHERE goal_id = ?", (deleted_goal['db_id'],))
                            conn.commit()
                            st.success(f"Goal '{deleted_goal['goal_name']}' deleted from database.")
                        except sqlite3.Error as e: st.error(f"DB Error deleting goal: {e}")
                    st.experimental_rerun()
    else: st.write("No financial goals defined yet.")
    st.markdown("---")

    # Form to add a new goal
    st.subheader("Add New Financial Goal")
    with st.form(key=f"add_goal_form_{investor_id}", clear_on_submit=True):
        goal_name = st.text_input("Goal Name (e.g., Retirement, Child's Education)")
        goal_type = st.selectbox("Goal Type", ["Retirement", "Education", "Home Purchase", "Vacation", "Vehicle", "Other"])
        target_amount = st.number_input("Target Amount (INR)", min_value=0.0, step=10000.0)
        target_year = st.number_input("Target Year", min_value=datetime.now().year + 1, max_value=datetime.now().year + 50, step=1)
        current_savings = st.number_input("Current Savings for this Goal (INR)", min_value=0.0, step=1000.0)
        priority = st.slider("Priority (1=Highest)", 1, 10, 5)
        notes = st.text_area("Notes (Optional)")
        
        add_goal_submitted = st.form_submit_button("Add Goal")
        if add_goal_submitted and goal_name and target_amount > 0:
            new_goal = {
                'goal_name': goal_name, 'goal_type': goal_type, 'target_amount': target_amount,
                'target_year': target_year, 'current_savings_for_goal': current_savings, 
                'priority': priority, 'notes': notes, 'is_new': True, 'db_id': None
            }
            try:
                c = conn.cursor()
                c.execute("""INSERT INTO financial_goals 
                             (investor_id, goal_name, goal_type, target_amount, target_year, current_savings_for_goal, priority, notes, creation_date)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                          (investor_id, goal_name, goal_type, target_amount, target_year, current_savings, priority, notes, date.today().isoformat()))
                conn.commit()
                new_goal['db_id'] = c.lastrowid
                new_goal['is_new'] = False
                st.session_state[goals_list_key].append(new_goal)
                st.success(f"Goal '{goal_name}' added and saved to database!")
                st.experimental_rerun()
            except sqlite3.Error as e:
                st.error(f"Database error adding goal: {e}")
        elif add_goal_submitted:
            st.warning("Please provide at least Goal Name and Target Amount.")

def risk_assessment_tab_content(conn):
    st.header(get_text("risk_assessment_tab"))
    questions = [
        "How would you react to a sudden 20% drop in your investment portfolio value?",
        "What is your primary goal for these investments?",
        "How long do you plan to keep your money invested?",
        "How comfortable are you with taking financial risks?",
        "What percentage of your income are you willing to invest in high-risk, high-reward assets?"
    ]
    options = [
        ["Sell all investments immediately", "Sell some investments and wait", "Hold and wait for recovery", "Hold and monitor closely", "Invest more during the dip"],
        ["Capital Preservation", "Regular Income", "Moderate Growth", "Aggressive Growth"],
        ["Less than 1 year", "1-3 years", "3-5 years", "5-10 years", "More than 10 years"],
        ["Not comfortable at all", "Slightly comfortable", "Moderately comfortable", "Very comfortable"],
        ["0-10%", "10-25%", "25-50%", "More than 50%"]
    ]
    with st.form("risk_assessment_form", clear_on_submit=False):
        for i, q_text in enumerate(questions):
            st.session_state.ra_answers[i] = st.radio(q_text, options[i], index=0, key=f"ra_q_{i}")
        risk_submit = st.form_submit_button("Submit Risk Assessment")
        if risk_submit:
            st.success("Risk assessment responses recorded in session.")
            # Risk score calculation would happen when full profile is processed

def mfd_dashboard_tab_content(conn):
    st.header(get_text("mfd_dashboard_tab"))
    st.subheader("Investor Management")
    investor_list = pd.read_sql_query("SELECT investor_id, name, dob, pan_number FROM investors", conn)
    if not investor_list.empty:
        st.dataframe(investor_list)
        selected_investor_id = st.selectbox("Select Investor to View/Edit", options=investor_list['investor_id'], format_func=lambda x: f"{x} - {investor_list[investor_list['investor_id']==x]['name'].iloc[0]}")
        if st.button("Load Selected Investor Data") and selected_investor_id:
            st.session_state.current_investor_id = selected_investor_id
            # Load data from DB into session state for all tabs
            c = conn.cursor()
            c.execute("SELECT * FROM investors WHERE investor_id = ?", (selected_investor_id,))
            data = c.fetchone()
            if data:
                cols = [desc[0] for desc in c.description]
                investor_db_data = dict(zip(cols, data))
                st.session_state.p_name = investor_db_data.get('name', '')
                st.session_state.p_dob = datetime.strptime(investor_db_data['dob'], '%Y-%m-%d').date() if investor_db_data.get('dob') else None
                st.session_state.p_pan_number = investor_db_data.get('pan_number', '')
                st.session_state.p_email = investor_db_data.get('email_address', '')
                st.session_state.p_mobile = investor_db_data.get('mobile_number', '')
                st.session_state.p_occupation = investor_db_data.get('occupation', 'Salaried - White-Collar')
                st.session_state.p_urban_rural = investor_db_data.get('urban_rural_status', 'Urban (Metro/Tier I)')
                
                financial_details = decrypt_data(investor_db_data.get('financial_details')) if investor_db_data.get('financial_details') else {}
                st.session_state.ie_monthly_income = financial_details.get('total_household_income', 0.0)
                st.session_state.ie_monthly_expenses = financial_details.get('monthly_household_expenses', 0.0)
                st.session_state.ie_total_investments = financial_details.get('total_investments', 0.0)
                st.session_state.ie_home_ownership = investor_db_data.get('home_ownership', False)
                st.session_state.ie_rent_amount = investor_db_data.get('rent_amount', 0.0)
                st.session_state.ie_loan_emis = investor_db_data.get('emi_amount', 0.0)
                st.session_state.ie_current_emergency_fund = investor_db_data.get('emergency_fund', 0.0)
                st.session_state.ie_market_experience = investor_db_data.get('market_linked_experience', 'No')
                
                dependents_json = investor_db_data.get('dependents')
                st.session_state.dependents_data_list = json.loads(dependents_json) if dependents_json else []
                st.session_state.num_dependents_value = len(st.session_state.dependents_data_list)
                st.session_state.num_dependents_value_input = st.session_state.num_dependents_value

                risk_answers_json = investor_db_data.get('risk_answers')
                st.session_state.ra_answers = json.loads(risk_answers_json) if risk_answers_json else [None]*5
                
                # Clear and reload financial goals for this investor
                goals_list_key = f'financial_goals_list_{selected_investor_id}'
                if goals_list_key in st.session_state: del st.session_state[goals_list_key]

                st.success(f"Data for {selected_investor_id} loaded into session. Navigate to other tabs to view/edit.")
                st.experimental_rerun()
            else: st.error("Could not load investor data.")
    else: st.info("No investors found in the database.")

    st.markdown("---")
    st.subheader("Create New Investor Profile")
    if st.button("Start New Investor Profile"):
        # Clear session state for a new entry
        new_investor_id = generate_investor_id(conn)
        st.session_state.current_investor_id = new_investor_id # Tentative ID
        # Reset all form fields in session state
        initialize_session_state() # This will reset to defaults, but keep current_investor_id if we set it after
        st.session_state.current_investor_id = new_investor_id # Re-set after init
        st.session_state.p_name = "" # Clear specific fields not covered by simple init
        # ... clear other relevant session state fields for a new form ...
        st.success(f"New investor profile started with temporary ID: {new_investor_id}. Please fill data in tabs.")
        st.experimental_rerun()

    if st.session_state.current_investor_id:
        st.markdown("---")
        st.subheader(f"Finalize and Save Profile for: {st.session_state.current_investor_id}")
        if st.button("Save All Information for Current Investor to Database"):
            # Consolidate all data from session state
            investor_id_to_save = st.session_state.current_investor_id
            name = st.session_state.p_name
            dob_obj = st.session_state.p_dob
            dob_str = dob_obj.isoformat() if dob_obj else None
            pan = st.session_state.p_pan_number
            email = st.session_state.p_email
            mobile = st.session_state.p_mobile
            occupation = st.session_state.p_occupation
            urban_rural = st.session_state.p_urban_rural
            
            dependents_list_final = st.session_state.dependents_data_list
            dependents_json_final = json.dumps(dependents_list_final)
            num_dependents_final = len(dependents_list_final)

            financial_details_dict = {
                'total_household_income': st.session_state.ie_monthly_income,
                'monthly_household_expenses': st.session_state.ie_monthly_expenses,
                'total_investments': st.session_state.ie_total_investments
            }
            financial_details_encrypted = encrypt_data(financial_details_dict)

            home_ownership = st.session_state.ie_home_ownership
            rent_amount = st.session_state.ie_rent_amount
            emi_amount = st.session_state.ie_loan_emis
            emergency_fund = st.session_state.ie_current_emergency_fund
            market_experience = st.session_state.ie_market_experience
            risk_answers_json_final = json.dumps(st.session_state.ra_answers)

            # Calculate risk score and profile
            # Prepare investor_data_dict for calculations
            temp_investor_data_for_calc = {
                'dob': dob_str, 'occupation': occupation, 'total_household_income': st.session_state.ie_monthly_income,
                'urban_rural_status': urban_rural, 'owns_home': home_ownership, 
                'loan_emis': emi_amount, 'current_emergency_fund': emergency_fund,
                'market_experience': market_experience, 'num_dependents': num_dependents_final
            }
            calculated_risk_score = calculate_risk_score(conn, investor_id_to_save, temp_investor_data_for_calc, st.session_state.ra_answers)
            investor_profile_code = assign_profile(temp_investor_data_for_calc)

            try:
                c = conn.cursor()
                # Check if investor exists for INSERT OR REPLACE
                c.execute("SELECT 1 FROM investors WHERE investor_id = ?", (investor_id_to_save,))
                exists = c.fetchone()
                sql_query = """
                INSERT INTO investors (investor_id, name, dob, pan_number, email_address, mobile_number, occupation, urban_rural_status, 
                                     dependents, financial_details, home_ownership, rent_amount, emi_amount, emergency_fund, 
                                     market_linked_experience, risk_answers, risk_score, investor_profile, plan_in_action_date, consent_log,
                                     total_investments, total_loans, monthly_household_expenses) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(investor_id) DO UPDATE SET
                    name=excluded.name, dob=excluded.dob, pan_number=excluded.pan_number, email_address=excluded.email_address, mobile_number=excluded.mobile_number,
                    occupation=excluded.occupation, urban_rural_status=excluded.urban_rural_status, dependents=excluded.dependents, financial_details=excluded.financial_details,
                    home_ownership=excluded.home_ownership, rent_amount=excluded.rent_amount, emi_amount=excluded.emi_amount, emergency_fund=excluded.emergency_fund,
                    market_linked_experience=excluded.market_linked_experience, risk_answers=excluded.risk_answers, risk_score=excluded.risk_score, 
                    investor_profile=excluded.investor_profile, plan_in_action_date=excluded.plan_in_action_date, consent_log=excluded.consent_log,
                    total_investments=excluded.total_investments, total_loans=excluded.total_loans, monthly_household_expenses=excluded.monthly_household_expenses;
                """
                # These last 3 are not in the form, so use placeholders or derive if possible
                # total_investments from ie_total_investments
                # total_loans (outstanding) - not directly collected, maybe sum of EMIs * tenure if available, or a new field
                # monthly_household_expenses from ie_monthly_expenses

                c.execute(sql_query, (investor_id_to_save, name, dob_str, pan, email, mobile, occupation, urban_rural, 
                                   dependents_json_final, financial_details_encrypted, home_ownership, rent_amount, emi_amount, emergency_fund,
                                   market_experience, risk_answers_json_final, calculated_risk_score, investor_profile_code, 
                                   date.today().isoformat(), "User consent recorded", 
                                   st.session_state.ie_total_investments, emi_amount, st.session_state.ie_monthly_expenses # Using emi_amount as proxy for total_loans for now
                                   ))
                conn.commit()
                st.success(f"All information for Investor ID {investor_id_to_save} saved to database!")
                # Optionally clear session state for this investor or reload to confirm
            except sqlite3.Error as e:
                st.error(f"Database error saving investor profile: {e}")

def investor_dashboard_tab_content(conn, investor_id):
    st.header(get_text("investor_dashboard_tab"))
    if not investor_id:
        st.info("Please select or create an investor profile from the MFD Dashboard.")
        return
    # Fetch and display investor data, calculated summaries, recommendations, etc.
    st.write(f"Displaying dashboard for Investor ID: {investor_id}")
    # Placeholder - This would involve fetching full profile, goals, calculating SIPs, showing charts etc.

def investor_guide_tab_content(conn, investor_id):
    st.header(get_text("investor_guide_tab"))
    if not investor_id:
        st.info("Please select or create an investor profile.")
        return
    st.write(f"Displaying financial guide for Investor ID: {investor_id}")
    # Placeholder - This would show the generated PDF or HTML guide content.

# --- Main Application Structure with Tabs ---
if 'current_investor_id' not in st.session_state: 
    st.session_state.current_investor_id = None

if st.session_state.current_investor_id:
    st.sidebar.success(f"Active Investor ID: {st.session_state.current_investor_id}")
else:
    st.sidebar.info("No active investor. Use MFD Dashboard to load or create.")

tab_titles = [
    get_text("personal_info_tab"), 
    get_text("family_structure_tab"), 
    get_text("income_expenses_tab"), 
    get_text("financial_goals_tab"), 
    get_text("risk_assessment_tab"), 
    get_text("investor_dashboard_tab"),
    get_text("investor_guide_tab"),
    get_text("mfd_dashboard_tab")
]
tabs = st.tabs(tab_titles)

with tabs[0]: personal_info_tab_content(conn)
with tabs[1]: family_structure_tab_content(conn)
with tabs[2]: income_expenses_tab_content(conn)
with tabs[3]: financial_goals_tab_content(conn, st.session_state.current_investor_id)
with tabs[4]: risk_assessment_tab_content(conn)
with tabs[5]: investor_dashboard_tab_content(conn, st.session_state.current_investor_id)
with tabs[6]: investor_guide_tab_content(conn, st.session_state.current_investor_id)
with tabs[7]: mfd_dashboard_tab_content(conn)

