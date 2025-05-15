import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
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
    /* Custom styles for sidebar radio to look more like tabs */
    div[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
        padding: 0.5rem 0.75rem;
        border-radius: 0.375rem;
        margin-bottom: 0.25rem;
        font-weight: 500;
    }
    div[data-testid="stSidebar"] div[role="radiogroup"] > label > input:checked + div {
        background-color: #007AFF;
        color: white;
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

# --- Investor Profile Definitions (from Master Document) ---
# Simplified for brevity, expand with all 30 profiles and details
INVESTOR_PROFILES_MASTER = {
    "W1": {"desc": "Young Adult, White-Collar, Low Income", "age_min": 22, "age_max": 30, "income_level": "Low", "occupation_type": "White-Collar", "dependents_max": 1},
    "W2": {"desc": "Young Adult, White-Collar, Sufficient Income", "age_min": 22, "age_max": 30, "income_level": "Sufficient", "occupation_type": "White-Collar", "dependents_max": 1},
    "W3": {"desc": "Young Adult, White-Collar, Good Income", "age_min": 22, "age_max": 30, "income_level": "Good", "occupation_type": "White-Collar", "dependents_max": 1},
    "W4": {"desc": "Young Family, White-Collar, Low Income", "age_min": 28, "age_max": 35, "income_level": "Low", "occupation_type": "White-Collar", "dependents_min": 1, "dependents_max": 2, "child_age_max": 7},
    # ... Add all W profiles
    "B1": {"desc": "Young Adult, Blue-Collar, Low Income", "age_min": 22, "age_max": 30, "income_level": "Low", "occupation_type": "Blue-Collar", "dependents_max": 1},
    # ... Add all B profiles
    # Example for Mid-Career Family
    "W8": {"desc": "Mid-Career Family, White-Collar, Sufficient Income", "age_min": 35, "age_max": 50, "income_level": "Sufficient", "occupation_type": "White-Collar", "dependents_min": 2, "dependents_max": 3, "child_age_min": 8, "child_age_max": 18},
    "B8": {"desc": "Mid-Career Family, Blue-Collar, Sufficient Income", "age_min": 35, "age_max": 50, "income_level": "Sufficient", "occupation_type": "Blue-Collar", "dependents_min": 2, "dependents_max": 3, "child_age_min": 8, "child_age_max": 18},
}

# Database setup
def init_db():
    conn = sqlite3.connect('financial_planning.db', check_same_thread=False)
    c = conn.cursor()
    # Investors table schema updates
    try: c.execute("ALTER TABLE investors ADD COLUMN investor_profile_id TEXT") # Stores W1, B8 etc.
    except sqlite3.OperationalError: pass 
    try: c.execute("ALTER TABLE investors ADD COLUMN pan_number TEXT")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE investors ADD COLUMN email_address TEXT")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE investors ADD COLUMN mobile_number TEXT")
    except sqlite3.OperationalError: pass
    try: c.execute("ALTER TABLE investors ADD COLUMN gender TEXT")
    except sqlite3.OperationalError: pass

    c.execute('''CREATE TABLE IF NOT EXISTS investors (
        investor_id TEXT PRIMARY KEY,
        name TEXT,
        dob TEXT,
        gender TEXT,
        financial_details TEXT, 
        occupation TEXT,
        urban_rural_status TEXT,
        dependents TEXT,
        home_ownership BOOLEAN,
        rent_amount REAL,
        emi_amount REAL,
        emergency_fund REAL,
        risk_score INTEGER,
        risk_answers TEXT,
        plan_in_action_date TEXT,
        consent_log TEXT,
        market_linked_experience TEXT,
        investor_profile_id TEXT, 
        pan_number TEXT, 
        email_address TEXT,
        mobile_number TEXT,
        total_investments REAL,
        total_loans REAL,
        monthly_household_expenses REAL
    )''')
    
    # Economic indicators table schema update
    try: c.execute("ALTER TABLE economic_indicators ADD COLUMN is_fallback BOOLEAN DEFAULT FALSE")
    except sqlite3.OperationalError: pass # Column likely already exists
    
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
        goal_type TEXT, -- e.g., Education, Retirement, Home Purchase, Debt Reduction, Emergency Fund
        target_amount REAL,
        target_year INTEGER,
        current_savings_for_goal REAL DEFAULT 0,
        priority INTEGER, -- Lower number means higher priority
        notes TEXT,
        creation_date TEXT,
        is_auto_generated BOOLEAN DEFAULT FALSE,
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
    # Try to get non-fallback data for today first
    c.execute("SELECT data, is_fallback FROM economic_indicators WHERE date = ? AND is_fallback = 0 ORDER BY date DESC LIMIT 1", (datetime.now().strftime("%Y-%m-%d"),))
    row = c.fetchone()
    if row and row[0]:
        try: return json.loads(row[0]), bool(row[1])
        except json.JSONDecodeError: pass
    # If not found, get the latest available data (could be fallback or older)
    c.execute("SELECT data, is_fallback FROM economic_indicators ORDER BY date DESC LIMIT 1")
    row = c.fetchone()
    if row and row[0]:
        try: return json.loads(row[0]), bool(row[1])
        except json.JSONDecodeError: return DEFAULT_ECONOMIC_DATA, True # Error decoding, use fallback
    return DEFAULT_ECONOMIC_DATA, True # No data at all, use fallback

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
        else: return 0
        return today_date_obj.year - dob.year - ((today_date_obj.month, today_date_obj.day) < (dob.month, dob.day))
    except ValueError: return 0

def encrypt_data(data):
    if data is None: return None
    return cipher.encrypt(json.dumps(data).encode()).decode()

def decrypt_data(encrypted_data):
    if not encrypted_data: return None
    try: return json.loads(cipher.decrypt(encrypted_data.encode()).decode())
    except: return None

# --- Investor Profile Assignment Logic (Based on Master Document) ---
def get_investor_life_cycle_stage(age, num_dependents, children_ages=None):
    # children_ages: list of ages of children, if available
    # This is a simplified version. The master doc has more nuanced definitions.
    if 22 <= age <= 30:
        if num_dependents <= 1: return "Young Adult"
    if 28 <= age <= 35:
        # Check if young children (0-7 years) - requires more data than just num_dependents
        return "Young Family" # Simplified for now
    if 35 <= age <= 50:
        return "Mid-Career Family" # Simplified
    if 50 <= age <= 60:
        return "Pre-Retirement"
    if age > 60:
        return "Retirement"
    return "Unknown"

def get_income_level_thresholds(occupation_type, life_cycle_stage):
    # Based on Section 4 of Master Document Part 1
    # Base thresholds for Young Adult
    base_low_wc = 30000  # White-Collar Low income upper limit per month
    base_low_bc = 12000  # Blue-Collar Low income upper limit per month

    multiplier = 1.0
    if life_cycle_stage == "Young Family": multiplier = 1.5
    elif life_cycle_stage == "Mid-Career Family": multiplier = 1.5 * 1.5
    elif life_cycle_stage == "Pre-Retirement" or life_cycle_stage == "Retirement": multiplier = 1.5 * 1.5 * 1.5

    if occupation_type == "White-Collar":
        low_upper = base_low_wc * multiplier
        sufficient_upper = low_upper * 2
    elif occupation_type == "Blue-Collar":
        # Blue-Collar: Low < X, Sufficient X to Y, Good > Y
        # From doc: Low < 12k, Suff 12k-20k, Good >20k for Young Adult
        # This needs more precise band definition from the master doc for scaling.
        # For now, using a simplified scaling similar to White-Collar for structure.
        low_upper = base_low_bc * multiplier
        sufficient_upper = low_upper * (20000/12000) # Approx ratio from Young Adult BC
    else: # Other/Unknown
        low_upper = base_low_wc * multiplier # Default to WC for structure
        sufficient_upper = low_upper * 2

    return low_upper, sufficient_upper

def get_income_level_from_value(monthly_income, occupation_type_raw, age, num_dependents):
    # This function determines Low, Sufficient, Good based on the master doc's methodology
    occupation_type = "White-Collar" if "White-Collar" in occupation_type_raw else "Blue-Collar" if "Blue-Collar" in occupation_type_raw else "Other"
    life_cycle = get_investor_life_cycle_stage(age, num_dependents)
    
    low_threshold, sufficient_threshold = get_income_level_thresholds(occupation_type, life_cycle)

    if monthly_income <= low_threshold: return "Low"
    elif monthly_income <= sufficient_threshold: return "Sufficient"
    else: return "Good"

def assign_investor_profile_id(investor_data_dict):
    age = calculate_age(investor_data_dict.get('dob'), date.today())
    occupation_raw = investor_data_dict.get('occupation', 'Other')
    occupation_type = "White-Collar" if "White-Collar" in occupation_raw else "Blue-Collar" if "Blue-Collar" in occupation_raw else "Other"
    num_total_dependents = investor_data_dict.get('num_children', 0) + investor_data_dict.get('num_other_dependents', 0)
    
    # Determine income level based on individual income (assuming 'total_household_income' is individual for now, or needs adjustment)
    # The master doc specifies "individual monthly income" for profile income levels.
    # For simplicity, using total_household_income. This might need refinement if individual income is captured separately.
    individual_monthly_income = investor_data_dict.get('total_household_income', 0) 
    income_level_str = get_income_level_from_value(individual_monthly_income, occupation_raw, age, num_total_dependents)

    # Iterate through INVESTOR_PROFILES_MASTER to find a match
    # This is a basic matching logic, can be made more sophisticated
    for profile_id, profile_details in INVESTOR_PROFILES_MASTER.items():
        if profile_details["occupation_type"] == occupation_type and \
           profile_details["income_level"] == income_level_str and \
           profile_details["age_min"] <= age <= profile_details["age_max"]:
            # Further refine by dependents if specified in profile_details
            if "dependents_max" in profile_details and num_total_dependents > profile_details["dependents_max"]: continue
            if "dependents_min" in profile_details and num_total_dependents < profile_details["dependents_min"]: continue
            # Add child age checks if relevant for the profile category (e.g., Young Family)
            return profile_id
    return "UnknownProfile" # Fallback if no specific profile matches

# --- Financial Goal Automation (Based on Master Document) ---
DEFAULT_GOALS_BY_PROFILE_TYPE = {
    # Profile Type can be a combination like "Young Adult_White-Collar_Low"
    # Or more general like "Young Adult"
    # This needs to be mapped from the 30 profiles in the master doc
    "Young Adult": [
        {"name": "Emergency Fund Creation", "type": "Emergency Fund", "priority": 1, "target_months_expenses": 3},
        {"name": "Debt Reduction (if any)", "type": "Debt Reduction", "priority": 2},
        {"name": "Short-term Savings (e.g., Skill Upgradation)", "type": "Short-Term Savings", "priority": 3, "target_years": 2},
        {"name": "Retirement Planning (Start Early)", "type": "Retirement", "priority": 4}
    ],
    "Young Family": [
        {"name": "Emergency Fund (Maintain/Increase)", "type": "Emergency Fund", "priority": 1, "target_months_expenses": 4},
        {"name": "Children's Education Fund", "type": "Education", "priority": 2, "child_ref": "oldest"}, # Needs logic for target year/amount
        {"name": "Home Purchase (Down Payment)", "type": "Home Purchase", "priority": 3, "target_years": 5},
        {"name": "Retirement Planning", "type": "Retirement", "priority": 4}
    ],
    "Mid-Career Family": [
        {"name": "Emergency Fund (Maintain)", "type": "Emergency Fund", "priority": 1, "target_months_expenses": 6},
        {"name": "Children's Higher Education", "type": "Education", "priority": 2, "child_ref": "all"},
        {"name": "Children's Marriage (Optional)", "type": "Marriage", "priority": 3},
        {"name": "Retirement Corpus Building", "type": "Retirement", "priority": 4, "target_age": 60},
        {"name": "Wealth Creation", "type": "Wealth Creation", "priority": 5}
    ],
    # Add more profile types and their default goals
}

def auto_generate_financial_goals(conn, investor_id, investor_data_dict, investor_profile_id):
    c = conn.cursor()
    # Check if auto-generated goals already exist to prevent duplication
    c.execute("SELECT COUNT(*) FROM financial_goals WHERE investor_id = ? AND is_auto_generated = 1", (investor_id,))
    if c.fetchone()[0] > 0:
        st.info(f"Automatic financial goals already exist for {investor_id}. Skipping generation.")
        return

    # Determine profile type for goal mapping (e.g., "Young Adult", "Young Family")
    # This is a simplification; the master doc implies goals might be specific to the 30 profiles.
    age = calculate_age(investor_data_dict.get('dob'), date.today())
    num_dependents = investor_data_dict.get('num_children', 0) + investor_data_dict.get('num_other_dependents', 0)
    profile_category_for_goals = get_investor_life_cycle_stage(age, num_dependents) # Using life cycle for now

    default_goals_template = DEFAULT_GOALS_BY_PROFILE_TYPE.get(profile_category_for_goals, [])
    
    generated_goals_count = 0
    for goal_template in default_goals_template:
        goal_name = goal_template["name"]
        goal_type = goal_template["type"]
        priority = goal_template["priority"]
        target_amount = 0  # Placeholder, needs calculation logic
        target_year = date.today().year + (goal_template.get("target_years", 10)) # Default 10 years if not specified
        notes = "Automatically generated based on investor profile."

        # --- Add specific calculation logic for target_amount and target_year ---
        if goal_type == "Emergency Fund":
            # Use calculate_required_emergency_fund if available and suitable, or simplify
            monthly_expenses = investor_data_dict.get('monthly_household_expenses', 20000) # Default if not available
            target_months = goal_template.get("target_months_expenses", 3)
            target_amount = monthly_expenses * target_months
            target_year = date.today().year + 1 # Typically a short-term goal
        
        elif goal_type == "Retirement":
            # Simplified: Target corpus = 20 * current annual expenses. Target year = age 60.
            annual_expenses = investor_data_dict.get('monthly_household_expenses', 20000) * 12
            target_amount = annual_expenses * 20 
            retirement_age = goal_template.get("target_age", 60)
            target_year = datetime.strptime(investor_data_dict.get('dob'), "%Y-%m-%d").year + retirement_age
            if target_year <= date.today().year: target_year = date.today().year + 20 # Ensure future

        elif goal_type == "Education" and "child_ref" in goal_template:
            # This needs data on children's ages. For now, a placeholder.
            # Assume a generic education goal if no specific child data is processed here.
            target_amount = 500000 # Placeholder amount
            target_year = date.today().year + 10 + (priority * 2) # Stagger based on priority
            goal_name = f"{goal_name} (Child {priority-1 if priority > 1 else 1})" # Make name unique if multiple education goals

        # Add more goal-specific logic here based on master document rules

        if target_amount > 0:
            try:
                c.execute("""INSERT INTO financial_goals 
                             (investor_id, goal_name, goal_type, target_amount, target_year, priority, notes, creation_date, is_auto_generated)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                          (investor_id, goal_name, goal_type, target_amount, target_year, priority, notes, date.today().isoformat(), True))
                generated_goals_count += 1
            except sqlite3.Error as e:
                st.error(f"Error saving auto-generated goal '{goal_name}': {e}")
        
    if generated_goals_count > 0:
        conn.commit()
        st.success(f"{generated_goals_count} financial goals automatically generated for {investor_id}.")
    else:
        st.info(f"No applicable automatic financial goals generated for {investor_id} based on current profile/rules.")

# --- Risk Score Calculation (incorporating goal adjustments placeholder) ---
def calculate_risk_score(db_conn, investor_id_for_log, investor_data_dict, answers):
    base_score_100 = 0
    raw_psychometric_score = 0
    greed_map = {"Not likely at all": 1, "Somewhat unlikely": 2, "Neutral": 3, "Somewhat likely": 4, "Very likely": 5}
    preference_map = {"Definitely Fixed Deposit": 1, "Lean towards Fixed Deposit": 2, "Neutral": 3, "Lean towards equity fund": 4, "Definitely equity fund": 5}
    willingness_map = {"Not willing at all": 1, "Somewhat reluctant": 2, "Neutral": 3, "Somewhat willing": 4, "Very willing": 5}
    reaction_map = {"Sell all investments immediately": 1, "Sell some investments and wait": 2, "Hold and wait for recovery": 3, "Hold and monitor closely": 4, "Invest more during the dip": 5}
    anxiety_map = {"Extremely anxious, unable to sleep": 1, "Quite anxious, very concerned": 2, "Mildly anxious, somewhat concerned": 3, "Not very anxious, can manage": 4, "Not anxious at all, comfortable": 5}
    
    if isinstance(answers, list) and len(answers) == 5:
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
    total_emi = investor_data_dict.get('loan_emis', 0) 
    debt_burden_ratio = total_emi / total_income if total_income > 0 else 1
    if debt_burden_ratio == 0: debt_points = 15
    elif debt_burden_ratio < 0.10: debt_points = 12
    elif debt_burden_ratio < 0.20: debt_points = 9
    elif debt_burden_ratio < 0.30: debt_points = 6
    elif debt_burden_ratio < 0.40: debt_points = 3
    else: debt_points = 0
    base_score_100 += debt_points

    age_val = calculate_age(investor_data_dict.get('dob'), date.today())
    if age_val < 25: age_points = 15
    elif age_val < 35: age_points = 12
    elif age_val < 45: age_points = 9
    elif age_val < 55: age_points = 6
    else: age_points = 3
    base_score_100 += age_points

    occupation_type_raw = investor_data_dict.get('occupation', 'Other')
    # Use the refined get_income_level_from_value function
    income_level_str = get_income_level_from_value(total_income, occupation_type_raw, age_val, investor_data_dict.get('num_children',0) + investor_data_dict.get('num_other_dependents',0))
    occupation_simple = "White-Collar" if "White-Collar" in occupation_type_raw else "Blue-Collar" if "Blue-Collar" in occupation_type_raw else "Other"
    income_points = 0
    if (occupation_simple == "White-Collar" and income_level_str == "Good") or \
       (occupation_simple == "Blue-Collar" and income_level_str == "Good"): income_points = 10
    elif (occupation_simple == "White-Collar" and income_level_str == "Sufficient") or \
         (occupation_simple == "Blue-Collar" and income_level_str == "Good"): income_points = 8
    elif (occupation_simple == "White-Collar" and income_level_str == "Low") or \
         (occupation_simple == "Blue-Collar" and income_level_str == "Sufficient"): income_points = 6
    elif (occupation_simple == "Blue-Collar" and income_level_str == "Low"): income_points = 4
    base_score_100 += income_points

    market_experience_raw = investor_data_dict.get('market_linked_experience', 'No Experience')
    experience_points = 0
    if "No Experience" in market_experience_raw: experience_points = 0
    elif "Less than 1 year" in market_experience_raw: experience_points = 2
    elif "1-3 years" in market_experience_raw: experience_points = 4
    elif "3-5 years" in market_experience_raw: experience_points = 6
    elif "More than 5 years" in market_experience_raw: experience_points = 10
    base_score_100 += experience_points

    base_score_100 = max(0, min(100, base_score_100))

    # Economic Adjustment
    latest_economic_data, is_fallback = get_latest_economic_data_from_db(db_conn)
    gdp_growth = latest_economic_data.get("gdp_growth", {}).get("value", 6.5) 
    cpi_inflation = latest_economic_data.get("cpi_inflation", {}).get("value", 5.0)
    economic_conditions_summary = f"GDP Growth: {gdp_growth}%, CPI Inflation: {cpi_inflation}%"
    economic_adjustment_factor = 0
    if gdp_growth > 7 and cpi_inflation < 4: economic_adjustment_factor = 2
    elif gdp_growth < 5 or cpi_inflation > 7: economic_adjustment_factor = -2
    elif gdp_growth < 6 or cpi_inflation > 6: economic_adjustment_factor = -1
    elif gdp_growth > 6 and cpi_inflation < 5: economic_adjustment_factor = 1

    # Goal-based Adjustment (Placeholder - to be refined with goal data)
    # Fetch investor's high-priority, short-term goals
    c_goals = db_conn.cursor()
    c_goals.execute("SELECT COUNT(*) FROM financial_goals WHERE investor_id = ? AND priority = 1 AND target_year <= ?", 
                    (investor_id_for_log, date.today().year + 3))
    high_priority_short_term_goals_count = c_goals.fetchone()[0]
    
    goal_adjustment_factor = 0
    if high_priority_short_term_goals_count > 0:
        goal_adjustment_factor = -1 # Example: Reduce risk appetite slightly if critical short-term goals exist
        goal_adjustment_details = f"{high_priority_short_term_goals_count} high-priority short-term goal(s) identified. Adjusted risk capacity by {goal_adjustment_factor}."
    else:
        goal_adjustment_details = "No significant short-term, high-priority goals impacting risk capacity adjustment at this time."

    # Final Score Calculation (out of 25)
    adjusted_score_100 = base_score_100 + economic_adjustment_factor + goal_adjustment_factor # Added goal_adjustment_factor
    adjusted_score_100 = max(0, min(100, adjusted_score_100))
    final_risk_score_25 = math.ceil(adjusted_score_100 / 4)

    # Log the adjustment
    c_log = db_conn.cursor()
    c_log.execute("""INSERT INTO risk_adjustment_log 
                 (investor_id, log_timestamp, base_risk_score_100, economic_conditions_summary, 
                  economic_adjustment_factor, goal_adjustment_details, final_risk_score_25, reason)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
              (investor_id_for_log, datetime.now().isoformat(), base_score_100, economic_conditions_summary,
               economic_adjustment_factor, goal_adjustment_details, final_risk_score_25, "Initial Calculation with Goal Adjustment"))
    db_conn.commit()

    return final_risk_score_25, base_score_100, economic_adjustment_factor, goal_adjustment_details


# --- UI Rendering Functions for Tabs ---
def personal_info_tab_content(conn, investor_id):
    st.subheader("👤 Personal Information")
    # Form for personal details
    name = st.text_input("Full Name", key=f"name_{investor_id}", value=st.session_state.form_data_personal.get("name", ""))
    dob_val = st.session_state.form_data_personal.get("dob")
    if isinstance(dob_val, str): dob_val = datetime.strptime(dob_val, "%Y-%m-%d").date()
    dob = st.date_input("Date of Birth", min_value=date(1920,1,1), max_value=date.today(), key=f"dob_{investor_id}", value=dob_val)
    gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], key=f"gender_{investor_id}", index=["Male", "Female", "Other", "Prefer not to say"].index(st.session_state.form_data_personal.get("gender", "Male")) if st.session_state.form_data_personal.get("gender") else 0)
    pan_number = st.text_input("PAN Number (Optional)", key=f"pan_{investor_id}", value=st.session_state.form_data_personal.get("pan_number", ""))
    email_address = st.text_input("Email Address (Optional)", key=f"email_{investor_id}", value=st.session_state.form_data_personal.get("email_address", ""))
    mobile_number = st.text_input("Mobile Number (Optional)", key=f"mobile_{investor_id}", value=st.session_state.form_data_personal.get("mobile_number", ""))
    occupation_options = [
        "Salaried (White-Collar - Private Sector)", 
        "Salaried (White-Collar - Government/PSU)",
        "Self-Employed Professional (e.g., Doctor, Lawyer, CA)",
        "Business Owner/Entrepreneur (White-Collar)",
        "Salaried (Blue-Collar - Skilled, e.g., Technician, Electrician)",
        "Salaried (Blue-Collar - Unskilled, e.g., Laborer, Helper)",
        "Self-Employed (Blue-Collar, e.g., Driver, Plumber, Small Shop Owner)",
        "Agriculture/Farmer",
        "Homemaker",
        "Student",
        "Retired",
        "Unemployed",
        "Other"
    ]
    occupation = st.selectbox("Occupation Category", occupation_options, key=f"occupation_{investor_id}", index=occupation_options.index(st.session_state.form_data_personal.get("occupation")) if st.session_state.form_data_personal.get("occupation") in occupation_options else 0)
    urban_rural_options = [
        "Urban (Metro/Tier I City)", 
        "Urban (Tier II City)", 
        "Urban (Tier III Town)", 
        "Rural (Village)", 
        "Semi-Urban"
    ]
    urban_rural_status = st.selectbox("Residential Status (Urban/Rural)", urban_rural_options, key=f"urban_rural_{investor_id}", index=urban_rural_options.index(st.session_state.form_data_personal.get("urban_rural_status")) if st.session_state.form_data_personal.get("urban_rural_status") in urban_rural_options else 0)

    personal_data = {
        "name": name, "dob": str(dob) if dob else None, "gender": gender,
        "pan_number": pan_number, "email_address": email_address, "mobile_number": mobile_number,
        "occupation": occupation, "urban_rural_status": urban_rural_status
    }
    return personal_data

def family_dependents_tab_content(conn, investor_id):
    st.subheader("👨‍👩‍👧‍👦 Family & Dependents")
    marital_options = ["Single", "Married", "Divorced", "Widowed"]
    marital_status = st.selectbox("Marital Status", marital_options, key=f"marital_{investor_id}", index=marital_options.index(st.session_state.form_data_family.get("marital_status")) if st.session_state.form_data_family.get("marital_status") in marital_options else 0)
    num_children = st.number_input("Number of Children", min_value=0, step=1, key=f"children_{investor_id}", value=st.session_state.form_data_family.get("num_children", 0))
    num_other_dependents = st.number_input("Number of Other Dependents (e.g., parents)", min_value=0, step=1, key=f"other_dependents_{investor_id}", value=st.session_state.form_data_family.get("num_other_dependents", 0))
    family_data = {"marital_status": marital_status, "num_children": num_children, "num_other_dependents": num_other_dependents}
    return family_data

def income_expenses_assets_tab_content(conn, investor_id):
    st.subheader("💰 Income, Expenses & Assets")
    form_data = st.session_state.form_data_income_expenses
    total_household_income = st.number_input("Total Monthly Household Income (INR)", min_value=0.0, step=1000.0, key=f"income_{investor_id}", value=form_data.get("total_household_income", 0.0))
    monthly_household_expenses = st.number_input("Total Monthly Household Expenses (excluding EMIs) (INR)", min_value=0.0, step=500.0, key=f"expenses_{investor_id}", value=form_data.get("monthly_household_expenses", 0.0))
    loan_emis = st.number_input("Total Monthly Loan EMIs (Home, Car, Personal, etc.) (INR)", min_value=0.0, step=500.0, key=f"emis_{investor_id}", value=form_data.get("loan_emis", 0.0))
    owns_home_val = form_data.get("owns_home", False)
    owns_home_idx = 0 if owns_home_val else 1 # Yes=0, No=1 for radio
    owns_home = st.radio("Do you own your primary residence?", ("Yes", "No"), key=f"owns_home_{investor_id}", index=owns_home_idx) == "Yes"
    rent_amount = 0.0
    if not owns_home:
        rent_amount = st.number_input("Monthly Rent Amount (if applicable) (INR)", min_value=0.0, step=500.0, key=f"rent_{investor_id}", value=form_data.get("rent_amount", 0.0))
    
    st.markdown("---_Assets_---")
    total_bank_savings = st.number_input("Total Bank Savings (Savings A/c, FDs) (INR)", min_value=0.0, step=10000.0, key=f"bank_savings_{investor_id}", value=form_data.get("total_bank_savings", 0.0))
    total_equity_investments = st.number_input("Total Equity Investments (Stocks, MFs excluding ELSS for tax) (INR)", min_value=0.0, step=10000.0, key=f"equity_{investor_id}", value=form_data.get("total_equity_investments", 0.0))
    total_debt_investments = st.number_input("Total Debt Investments (Bonds, Debt MFs, PPF, EPF, NPS Tier I) (INR)", min_value=0.0, step=10000.0, key=f"debt_inv_{investor_id}", value=form_data.get("total_debt_investments", 0.0))
    total_gold_investments = st.number_input("Total Gold Investments (Physical, SGBs, Gold MFs) (INR)", min_value=0.0, step=5000.0, key=f"gold_{investor_id}", value=form_data.get("total_gold_investments", 0.0))
    total_real_estate_value = st.number_input("Approx. Current Market Value of Real Estate (excluding primary residence) (INR)", min_value=0.0, step=100000.0, key=f"real_estate_{investor_id}", value=form_data.get("total_real_estate_value", 0.0))
    other_assets_value = st.number_input("Value of Other Significant Assets (INR)", min_value=0.0, step=10000.0, key=f"other_assets_{investor_id}", value=form_data.get("other_assets_value", 0.0))
    current_emergency_fund = st.number_input("Current Emergency Fund Available (Liquid Cash/Savings) (INR)", min_value=0.0, step=5000.0, key=f"emergency_fund_{investor_id}", value=form_data.get("current_emergency_fund", 0.0))

    st.markdown("---_Liabilities_---")
    home_loan_outstanding = st.number_input("Outstanding Home Loan Amount (INR)", min_value=0.0, step=50000.0, key=f"home_loan_{investor_id}", value=form_data.get("home_loan_outstanding", 0.0))
    vehicle_loan_outstanding = st.number_input("Outstanding Vehicle Loan(s) Amount (INR)", min_value=0.0, step=10000.0, key=f"vehicle_loan_{investor_id}", value=form_data.get("vehicle_loan_outstanding", 0.0))
    personal_loan_outstanding = st.number_input("Outstanding Personal Loan(s) Amount (INR)", min_value=0.0, step=5000.0, key=f"personal_loan_{investor_id}", value=form_data.get("personal_loan_outstanding", 0.0))
    credit_card_debt = st.number_input("Outstanding Credit Card Debt (rolled over) (INR)", min_value=0.0, step=1000.0, key=f"cc_debt_{investor_id}", value=form_data.get("credit_card_debt", 0.0))
    other_loans_outstanding = st.number_input("Other Outstanding Loans Amount (INR)", min_value=0.0, step=5000.0, key=f"other_loans_{investor_id}", value=form_data.get("other_loans_outstanding", 0.0))

    income_expense_data = {
        "total_household_income": total_household_income,
        "monthly_household_expenses": monthly_household_expenses,
        "loan_emis": loan_emis,
        "owns_home": owns_home,
        "rent_amount": rent_amount,
        "total_bank_savings": total_bank_savings,
        "total_equity_investments": total_equity_investments,
        "total_debt_investments": total_debt_investments,
        "total_gold_investments": total_gold_investments,
        "total_real_estate_value": total_real_estate_value,
        "other_assets_value": other_assets_value,
        "current_emergency_fund": current_emergency_fund,
        "home_loan_outstanding": home_loan_outstanding,
        "vehicle_loan_outstanding": vehicle_loan_outstanding,
        "personal_loan_outstanding": personal_loan_outstanding,
        "credit_card_debt": credit_card_debt,
        "other_loans_outstanding": other_loans_outstanding
    }
    return income_expense_data

def risk_assessment_questions_tab_content(conn, investor_id):
    st.subheader("🎯 Risk Assessment Questions")
    st.write("Please answer the following questions to help us understand your risk tolerance.")
    form_data = st.session_state.form_data_risk_questions
    answers = form_data.get("answers", [None]*5)

    q1_options = ["Not likely at all", "Somewhat unlikely", "Neutral", "Somewhat likely", "Very likely"]
    q1_ans = st.radio("1. How likely are you to invest a significant portion of your annual income in a high-risk, high-reward venture?", q1_options, key=f"q1_{investor_id}", index=q1_options.index(answers[0]) if answers[0] in q1_options else 0)
    
    q2_options = ["Definitely Fixed Deposit", "Lean towards Fixed Deposit", "Neutral", "Lean towards equity fund", "Definitely equity fund"]
    q2_ans = st.radio("2. If you were given a choice between a guaranteed return (like a Fixed Deposit) and a potentially higher but uncertain return (like an equity fund), which would you prefer for a major portion of your long-term savings?", q2_options, key=f"q2_{investor_id}", index=q2_options.index(answers[1]) if answers[1] in q2_options else 0)

    q3_options = ["Not willing at all", "Somewhat reluctant", "Neutral", "Somewhat willing", "Very willing"]
    q3_ans = st.radio("3. How willing are you to tolerate short-term losses in your investments for the potential of higher long-term gains?", q3_options, key=f"q3_{investor_id}", index=q3_options.index(answers[2]) if answers[2] in q3_options else 0)

    q4_options = ["Sell all investments immediately", "Sell some investments and wait", "Hold and wait for recovery", "Hold and monitor closely", "Invest more during the dip"]
    q4_ans = st.radio("4. Imagine the stock market drops by 20% in a month. What would be your most likely reaction regarding your equity investments?", q4_options, key=f"q4_{investor_id}", index=q4_options.index(answers[3]) if answers[3] in q4_options else 0)

    q5_options = ["Extremely anxious, unable to sleep", "Quite anxious, very concerned", "Mildly anxious, somewhat concerned", "Not very anxious, can manage", "Not anxious at all, comfortable"]
    q5_ans = st.radio("5. How would you describe your general level of anxiety when thinking about your financial future and investment performance?", q5_options, key=f"q5_{investor_id}", index=q5_options.index(answers[4]) if answers[4] in q5_options else 0)
    
    market_exp_options = ["No Experience", "Less than 1 year", "1-3 years", "3-5 years", "More than 5 years"]
    market_linked_experience = st.selectbox("What is your experience with market-linked investments (stocks, mutual funds, etc.)?",
                                            market_exp_options,
                                            key=f"market_exp_{investor_id}", index=market_exp_options.index(form_data.get("market_linked_experience")) if form_data.get("market_linked_experience") in market_exp_options else 0)

    risk_answers_data = {
        "answers": [q1_ans, q2_ans, q3_ans, q4_ans, q5_ans],
        "market_linked_experience": market_linked_experience
    }
    return risk_answers_data

def create_investor_profile_tab_content(conn):
    st.header("📝 Create/Edit Investor Profile")

    if 'current_investor_id' not in st.session_state or not st.session_state.current_investor_id:
        if st.button("Start New Investor Profile", key="start_new_profile_direct"):
            st.session_state.current_investor_id = generate_investor_id(conn)
            # Initialize form data for a new profile
            st.session_state.form_data_personal = {}
            st.session_state.form_data_family = {}
            st.session_state.form_data_income_expenses = {}
            st.session_state.form_data_risk_questions = {"answers": [None]*5, "market_linked_experience": "No Experience"}
            st.rerun()
        st.info("Click 'Start New Investor Profile' to begin or select an existing investor from the MFD Dashboard to edit.")
        return

    investor_id = st.session_state.current_investor_id
    st.subheader(f"Investor ID: {investor_id}")

    # Ensure form data states exist (they should if profile is loaded or new one started)
    if 'form_data_personal' not in st.session_state: st.session_state.form_data_personal = {}
    if 'form_data_family' not in st.session_state: st.session_state.form_data_family = {}
    if 'form_data_income_expenses' not in st.session_state: st.session_state.form_data_income_expenses = {}
    if 'form_data_risk_questions' not in st.session_state: st.session_state.form_data_risk_questions = {"answers": [None]*5, "market_linked_experience": "No Experience"}

    profile_tabs = ["Personal Info", "Family & Dependents", "Income, Expenses & Assets", "Risk Assessment Questions"]
    selected_profile_tab = st.tabs(profile_tabs)

    with selected_profile_tab[0]:
        st.session_state.form_data_personal = personal_info_tab_content(conn, investor_id)
    with selected_profile_tab[1]:
        st.session_state.form_data_family = family_dependents_tab_content(conn, investor_id)
    with selected_profile_tab[2]:
        st.session_state.form_data_income_expenses = income_expenses_assets_tab_content(conn, investor_id)
    with selected_profile_tab[3]:
        st.session_state.form_data_risk_questions = risk_assessment_questions_tab_content(conn, investor_id)

    if st.button("💾 Finalize and Save Profile", key=f"save_profile_{investor_id}"):
        full_investor_data = {
            **st.session_state.form_data_personal,
            **st.session_state.form_data_family,
            **st.session_state.form_data_income_expenses,
            "market_linked_experience": st.session_state.form_data_risk_questions.get("market_linked_experience"),
        }
        
        assigned_profile_id = assign_investor_profile_id(full_investor_data)
        encrypted_financial_details = encrypt_data(full_investor_data)
        risk_answers_list = st.session_state.form_data_risk_questions.get("answers", [])
        calculated_risk_score, base_score, econ_adj, goal_adj_details = calculate_risk_score(conn, investor_id, full_investor_data, risk_answers_list)

        c = conn.cursor()
        try:
            c.execute("""INSERT OR REPLACE INTO investors 
                         (investor_id, name, dob, gender, financial_details, occupation, urban_rural_status, 
                          dependents, home_ownership, rent_amount, emi_amount, emergency_fund, 
                          risk_score, risk_answers, plan_in_action_date, consent_log, market_linked_experience, 
                          investor_profile_id, pan_number, email_address, mobile_number, 
                          total_investments, total_loans, monthly_household_expenses)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                      (investor_id, 
                       full_investor_data.get('name'), 
                       full_investor_data.get('dob'),
                       full_investor_data.get('gender'),
                       encrypted_financial_details, 
                       full_investor_data.get('occupation'), 
                       full_investor_data.get('urban_rural_status'),
                       json.dumps({"children": full_investor_data.get('num_children'), "other": full_investor_data.get('num_other_dependents')}),
                       full_investor_data.get('owns_home'),
                       full_investor_data.get('rent_amount'),
                       full_investor_data.get('loan_emis'),
                       full_investor_data.get('current_emergency_fund'),
                       calculated_risk_score,
                       json.dumps(risk_answers_list),
                       datetime.now().strftime("%Y-%m-%d"), # plan_in_action_date
                       json.dumps({"consent_given_on": datetime.now().isoformat()}),
                       full_investor_data.get('market_linked_experience'),
                       assigned_profile_id, 
                       full_investor_data.get('pan_number'),
                       full_investor_data.get('email_address'),
                       full_investor_data.get('mobile_number'),
                       full_investor_data.get('total_equity_investments',0) + full_investor_data.get('total_debt_investments',0) + full_investor_data.get('total_gold_investments',0),
                       full_investor_data.get('home_loan_outstanding',0) + full_investor_data.get('vehicle_loan_outstanding',0) + full_investor_data.get('personal_loan_outstanding',0) + full_investor_data.get('credit_card_debt',0) + full_investor_data.get('other_loans_outstanding',0),
                       full_investor_data.get('monthly_household_expenses')
                       )
            )
            conn.commit()
            st.success(f"Investor profile for {investor_id} ({assigned_profile_id}) saved! Risk Score: {calculated_risk_score}/25")
            
            # Auto-generate financial goals after saving profile
            auto_generate_financial_goals(conn, investor_id, full_investor_data, assigned_profile_id)
            
            # Clear session state for new profile
            del st.session_state.current_investor_id
            # Clear form data states
            for key in ['form_data_personal', 'form_data_family', 'form_data_income_expenses', 'form_data_risk_questions']:
                if key in st.session_state: del st.session_state[key]
            st.rerun()
        except sqlite3.Error as e:
            st.error(f"Database error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

def financial_goals_tab_content(conn):
    st.header("🎯 Financial Goals Management")
    st.write("View, add, or modify financial goals for investors.")

    c = conn.cursor()
    c.execute("SELECT investor_id, name FROM investors ORDER BY name")
    investors = c.fetchall()
    investor_options = {f"{name} ({inv_id})": inv_id for inv_id, name in investors}
    
    selected_investor_display = st.selectbox("Select Investor to Manage Goals", options=list(investor_options.keys()), index=None, placeholder="Search or select an investor...", key="goal_investor_select")

    if selected_investor_display:
        investor_id = investor_options[selected_investor_display]
        st.subheader(f"Goals for: {selected_investor_display}")

        # Display existing goals
        c.execute("SELECT goal_id, goal_name, goal_type, target_amount, target_year, priority, notes, is_auto_generated FROM financial_goals WHERE investor_id = ? ORDER BY priority, target_year", (investor_id,))
        goals = c.fetchall()
        if goals:
            goals_df = pd.DataFrame(goals, columns=["ID", "Goal Name", "Type", "Target Amount (₹)", "Target Year", "Priority", "Notes", "Auto-Generated"])
            goals_df["Target Amount (₹)"] = goals_df["Target Amount (₹)"].apply(lambda x: f"{x:,.0f}")
            st.dataframe(goals_df, use_container_width=True, hide_index=True)
        else:
            st.info("No financial goals recorded for this investor yet.")

        if st.button(f"🔄 Re-Trigger Automatic Goal Generation for {selected_investor_display}", key=f"retrigger_goals_{investor_id}"):
            # Fetch latest investor data for re-generation
            c.execute("SELECT financial_details, investor_profile_id FROM investors WHERE investor_id = ?", (investor_id,))
            investor_row = c.fetchone()
            if investor_row:
                financial_details_encrypted, profile_id_for_goals = investor_row
                investor_data_for_goals = decrypt_data(financial_details_encrypted) or {}
                # Optionally clear existing auto-generated goals before re-triggering
                # c.execute("DELETE FROM financial_goals WHERE investor_id = ? AND is_auto_generated = 1", (investor_id,))
                # conn.commit() # If clearing
                auto_generate_financial_goals(conn, investor_id, investor_data_for_goals, profile_id_for_goals)
                st.rerun()
            else:
                st.error("Could not retrieve investor data for goal re-generation.")
        
        # --- Add Manual Goal Form ---
        st.markdown("---_Add/Edit Manual Goal_---")
        with st.form(key=f"manual_goal_form_{investor_id}"):
            goal_name_manual = st.text_input("Goal Name")
            goal_type_manual = st.selectbox("Goal Type", ["Education", "Retirement", "Home Purchase", "Vehicle Purchase", "Travel", "Marriage", "Debt Reduction", "Emergency Fund", "Wealth Creation", "Other"])
            target_amount_manual = st.number_input("Target Amount (₹)", min_value=0.0, step=1000.0)
            target_year_manual = st.number_input("Target Year", min_value=date.today().year, max_value=date.today().year + 50, step=1, value=date.today().year + 5)
            priority_manual = st.number_input("Priority (1=Highest)", min_value=1, step=1, value=5)
            notes_manual = st.text_area("Notes (Optional)")
            submit_manual_goal = st.form_submit_button("Save Manual Goal")

            if submit_manual_goal:
                if goal_name_manual and target_amount_manual > 0:
                    try:
                        c.execute("""INSERT INTO financial_goals 
                                     (investor_id, goal_name, goal_type, target_amount, target_year, priority, notes, creation_date, is_auto_generated)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                  (investor_id, goal_name_manual, goal_type_manual, target_amount_manual, target_year_manual, priority_manual, notes_manual, date.today().isoformat(), False))
                        conn.commit()
                        st.success(f"Manual goal '{goal_name_manual}' saved for {selected_investor_display}.")
                        st.rerun()
                    except sqlite3.Error as e:
                        st.error(f"Error saving manual goal: {e}")
                else:
                    st.warning("Please provide at least Goal Name and Target Amount.")
    else:
        st.info("Select an investor to manage their financial goals.")


def risk_profile_tab_content(conn):
    st.header("⚖️ Risk Profile (Calculated)")
    st.write("This section displays the calculated risk profile of the selected investor. (Read-only)")
    # Fetch selected investor (e.g., from MFD Dashboard or a selector here)
    # For now, let's assume an investor_id is available in session_state or passed
    if 'selected_investor_for_risk_profile' in st.session_state and st.session_state.selected_investor_for_risk_profile:
        investor_id = st.session_state.selected_investor_for_risk_profile
        c = conn.cursor()
        c.execute("SELECT name, risk_score, risk_answers, financial_details FROM investors WHERE investor_id = ?", (investor_id,))
        investor_record = c.fetchone()
        if investor_record:
            name, risk_score, risk_answers_json, financial_details_encrypted = investor_record
            st.subheader(f"Risk Profile for: {name} ({investor_id})")
            st.metric(label="Calculated Risk Score (out of 25)", value=risk_score if risk_score is not None else "N/A")
            
            # Display adjustment log
            c.execute("""SELECT base_risk_score_100, economic_conditions_summary, economic_adjustment_factor, goal_adjustment_details, final_risk_score_25, reason, log_timestamp 
                         FROM risk_adjustment_log WHERE investor_id = ? ORDER BY log_timestamp DESC LIMIT 1""", (investor_id,))
            log_entry = c.fetchone()
            if log_entry:
                st.markdown("**Risk Score Components (Latest Calculation):**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"- Base Score (out of 100): {log_entry[0]:.2f}")
                    st.write(f"- Economic Adjustment: {log_entry[2]:.2f}")
                with col2:
                    st.write(f"- Final Score (out of 25): {log_entry[4]}")
                    st.caption(f"_Calculation as of: {datetime.fromisoformat(log_entry[6]).strftime('%Y-%m-%d %H:%M')}_ ")
                st.markdown(f"**Economic Conditions Considered:** {log_entry[1]}")
                st.markdown(f"**Goal Adjustments:** {log_entry[3]}")
                st.markdown(f"**Reason/Notes:** {log_entry[5]}")
            else:
                st.info("No detailed risk calculation log found for this investor.")

            # Risk Profile Implications (Example)
            st.markdown("---_**Risk Profile Implications (Illustrative)**_---")
            if risk_score is not None:
                if risk_score <= 5: st.info("**Conservative:** Investor has a very low risk tolerance. Prefers capital preservation over growth. Suitable for very low-risk investments like FDs, PPF, Debt Funds (Short Duration).")
                elif risk_score <= 10: st.info("**Moderately Conservative:** Investor is cautious but willing to take minimal risk for slightly better returns. Suitable for a mix of FDs, Debt Funds, and a small allocation to Balanced/Hybrid Funds.")
                elif risk_score <= 15: st.info("**Balanced:** Investor is willing to take moderate risks for moderate returns. Suitable for a diversified portfolio including Debt Funds, Balanced/Hybrid Funds, and some allocation to Large-Cap Equity Funds.")
                elif risk_score <= 20: st.info("**Moderately Aggressive:** Investor is comfortable with taking significant risks for potentially high returns. Suitable for a portfolio with higher allocation to Equity Funds (Large, Mid, Small-Cap) and some alternative investments.")
                else: st.info("**Aggressive:** Investor has a high risk tolerance and is seeking maximum returns, understanding the potential for significant losses. Suitable for a portfolio heavily weighted towards Equities, including Small-Cap and Thematic Funds, and alternative investments.")
            else:
                st.warning("Risk score not yet calculated for this investor.")
        else:
            st.warning(f"No investor record found for ID: {investor_id}")
    else:
        st.info("Select an investor from the MFD Dashboard to view their calculated risk profile.")

def investor_dashboard_tab_content(conn):
    st.header("📊 Investor Dashboard")
    st.write("Select an investor to view their detailed financial summary and plan. (Enhancements in progress)")
    
    c = conn.cursor()
    c.execute("SELECT investor_id, name FROM investors ORDER BY name")
    investors = c.fetchall()
    investor_options = {f"{name} ({inv_id})": inv_id for inv_id, name in investors}
    
    selected_investor_display = st.selectbox("Select Investor", options=list(investor_options.keys()), index=None, placeholder="Search or select an investor...")
    
    if selected_investor_display:
        investor_id = investor_options[selected_investor_display]
        st.session_state.selected_investor_for_risk_profile = investor_id # For Risk Profile tab
        st.session_state.selected_investor_for_mfd_dashboard = investor_id # For MFD Dashboard tab

        c.execute("SELECT * FROM investors WHERE investor_id = ?", (investor_id,))
        investor_data_tuple = c.fetchone()
        if investor_data_tuple:
            cols_desc = [desc[0] for desc in c.description]
            investor_db_data = dict(zip(cols_desc, investor_data_tuple))
            
            st.subheader(f"Details for: {investor_db_data['name']} ({investor_id})")
            
            financial_details_decrypted = decrypt_data(investor_db_data.get('financial_details'))
            if not financial_details_decrypted: financial_details_decrypted = {} 

            detail_tabs_list = ["Summary & Profile", "Income & Expenses", "Assets & Liabilities", "Financial Goals", "Investment Plan (Auto)", "Risk Details"]
            summary_tab, income_tab, assets_tab, goals_tab, plan_tab, risk_details_tab = st.tabs(detail_tabs_list)

            with summary_tab:
                st.markdown(f"**Name:** {investor_db_data.get('name', 'N/A')}")
                st.markdown(f"**DOB:** {investor_db_data.get('dob', 'N/A')} (Age: {calculate_age(investor_db_data.get('dob'), date.today())})")
                st.markdown(f"**Gender:** {investor_db_data.get('gender', 'N/A')}")
                st.markdown(f"**Occupation:** {financial_details_decrypted.get('occupation', 'N/A')}")
                st.markdown(f"**Residential Status:** {financial_details_decrypted.get('urban_rural_status', 'N/A')}")
                st.markdown(f"**Assigned Profile ID:** {investor_db_data.get('investor_profile_id', 'N/A')}")
                st.markdown(f"**Calculated Risk Score:** {investor_db_data.get('risk_score', 'N/A')}/25")

            with income_tab:
                st.subheader("Income & Expenses")
                st.markdown(f"**Total Monthly Household Income:** ₹{financial_details_decrypted.get('total_household_income', 0):,.0f}")
                st.markdown(f"**Total Monthly Household Expenses (excl. EMIs):** ₹{financial_details_decrypted.get('monthly_household_expenses', 0):,.0f}")
                st.markdown(f"**Total Monthly Loan EMIs:** ₹{financial_details_decrypted.get('loan_emis', 0):,.0f}")
                monthly_savings = financial_details_decrypted.get('total_household_income', 0) - financial_details_decrypted.get('monthly_household_expenses', 0) - financial_details_decrypted.get('loan_emis', 0)
                st.metric(label="Estimated Monthly Savings", value=f"₹{monthly_savings:,.0f}")

            with assets_tab:
                st.subheader("Assets")
                st.markdown(f"**Bank Savings (Savings A/c, FDs):** ₹{financial_details_decrypted.get('total_bank_savings', 0):,.0f}")
                st.markdown(f"**Equity Investments:** ₹{financial_details_decrypted.get('total_equity_investments', 0):,.0f}")
                st.markdown(f"**Debt Investments (PPF, EPF, etc.):** ₹{financial_details_decrypted.get('total_debt_investments', 0):,.0f}")
                st.markdown(f"**Gold Investments:** ₹{financial_details_decrypted.get('total_gold_investments', 0):,.0f}")
                st.markdown(f"**Real Estate (excl. primary):** ₹{financial_details_decrypted.get('total_real_estate_value', 0):,.0f}")
                st.markdown(f"**Current Emergency Fund:** ₹{financial_details_decrypted.get('current_emergency_fund', 0):,.0f}")
                required_ef = calculate_required_emergency_fund(financial_details_decrypted)
                st.markdown(f"_Required Emergency Fund (Est.): ₹{required_ef:,.0f}_)")
                
                st.subheader("Liabilities")
                st.markdown(f"**Home Loan Outstanding:** ₹{financial_details_decrypted.get('home_loan_outstanding', 0):,.0f}")
                st.markdown(f"**Vehicle Loan(s) Outstanding:** ₹{financial_details_decrypted.get('vehicle_loan_outstanding', 0):,.0f}")
                st.markdown(f"**Personal Loan(s) Outstanding:** ₹{financial_details_decrypted.get('personal_loan_outstanding', 0):,.0f}")
                st.markdown(f"**Credit Card Debt (Rolled Over):** ₹{financial_details_decrypted.get('credit_card_debt', 0):,.0f}")

            with goals_tab:
                st.subheader("Financial Goals")
                c.execute("SELECT goal_name, goal_type, target_amount, target_year, priority, is_auto_generated FROM financial_goals WHERE investor_id = ? ORDER BY priority, target_year", (investor_id,))
                goals = c.fetchall()
                if goals:
                    goals_df = pd.DataFrame(goals, columns=["Goal Name", "Type", "Target Amount (₹)", "Target Year", "Priority", "Auto-Generated"])
                    goals_df["Target Amount (₹)"] = goals_df["Target Amount (₹)"].apply(lambda x: f"{x:,.0f}")
                    st.dataframe(goals_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No financial goals recorded. They can be auto-generated or added in the 'Financial Goals Management' tab.")
            
            with plan_tab:
                st.subheader("Automated Investment Plan")
                st.write("(Placeholder - This section will show the auto-generated investment plan based on risk profile, goals, and savings.)")

            with risk_details_tab:
                st.subheader("Risk Assessment Details")
                st.metric(label="Calculated Risk Score (out of 25)", value=investor_db_data.get('risk_score', 'N/A'))
                risk_answers_json = investor_db_data.get('risk_answers')
                if risk_answers_json:
                    risk_answers_list = json.loads(risk_answers_json)
                    st.markdown("**Responses to Risk Questions:**")
                    questions_text = [
                        "1. Likelihood to invest significantly in high-risk/high-reward venture?",
                        "2. Preference for guaranteed vs. uncertain returns for long-term savings?",
                        "3. Willingness to tolerate short-term losses for potential long-term gains?",
                        "4. Likely reaction to a 20% stock market drop?",
                        "5. General anxiety level about financial future and investments?"
                    ]
                    for i, ans in enumerate(risk_answers_list):
                        st.markdown(f"- {questions_text[i]}: **{ans}**")
                st.markdown(f"**Market Linked Experience:** {financial_details_decrypted.get('market_linked_experience', 'N/A')}")
                c.execute("""SELECT base_risk_score_100, economic_conditions_summary, economic_adjustment_factor, goal_adjustment_details, final_risk_score_25, reason, log_timestamp 
                             FROM risk_adjustment_log WHERE investor_id = ? ORDER BY log_timestamp DESC LIMIT 1""", (investor_id,))
                log_entry = c.fetchone()
                if log_entry:
                    st.markdown("**Latest Risk Calculation Breakdown:**")
                    st.markdown(f"  - Base Score (raw, out of 100): {log_entry[0]:.2f}")
                    st.markdown(f"  - Economic Conditions Considered: {log_entry[1]}")
                    st.markdown(f"  - Economic Adjustment Factor: {log_entry[2]:.2f}")
                    st.markdown(f"  - Goal Adjustments: {log_entry[3]}")
                    st.markdown(f"  - Final Calculated Score (out of 25): {log_entry[4]}")
                    st.markdown(f"  - Reason/Notes: {log_entry[5]}")
                    st.caption(f"  _Calculation as of: {datetime.fromisoformat(log_entry[6]).strftime('%Y-%m-%d %H:%M')}_ ")
        else:
            st.warning("Could not retrieve investor data.")
    else:
        st.info("Select an investor from the list above to see their details.")

def investor_guide_tab_content(conn):
    st.header("📜 Investor Guide")
    st.write("This section provides general guidance for investors. (Placeholder)")

def mfd_dashboard_tab_content(conn):
    st.header("⚙️ MFD Dashboard")
    
    mfd_sub_tabs = ["Investor Management & Search", "Aggregated Insights", "Print Investor Plans", "MFD Guide Access"]
    mfd_tab1, mfd_tab2, mfd_tab3, mfd_tab4 = st.tabs(mfd_sub_tabs)

    with mfd_tab1:
        st.subheader("Investor Management & Search")
        c = conn.cursor()
        c.execute("SELECT investor_id, name, dob, gender, occupation, urban_rural_status, risk_score, investor_profile_id FROM investors ORDER BY name")
        all_investors = c.fetchall()
        if all_investors:
            df_investors = pd.DataFrame(all_investors, columns=["ID", "Name", "DOB", "Gender", "Occupation", "Location Type", "Risk Score", "Profile ID"])
            st.dataframe(df_investors, use_container_width=True, hide_index=True)
            
            st.markdown("---_Search & Load Investor for Editing_---")
            investor_options_load = {f"{name} ({inv_id})": inv_id for inv_id, name, _,_,_,_,_,_ in all_investors}
            selected_investor_to_load_display = st.selectbox("Select Investor to Load/Edit Profile", options=list(investor_options_load.keys()), index=None, placeholder="Search or select an investor...", key="load_investor_select_mfd")
            if selected_investor_to_load_display:
                investor_id_to_load = investor_options_load[selected_investor_to_load_display]
                if st.button(f"Load Profile for {selected_investor_to_load_display}", key=f"load_btn_{investor_id_to_load}"):
                    c.execute("SELECT * FROM investors WHERE investor_id = ?", (investor_id_to_load,))
                    investor_data_tuple_load = c.fetchone()
                    if investor_data_tuple_load:
                        cols_load = [desc[0] for desc in c.description]
                        investor_db_data_load = dict(zip(cols_load, investor_data_tuple_load))
                        decrypted_details_load = decrypt_data(investor_db_data_load.get('financial_details')) or {}
                        risk_answers_list_load = json.loads(investor_db_data_load.get('risk_answers', '[]'))

                        st.session_state.current_investor_id = investor_id_to_load
                        st.session_state.form_data_personal = {
                            "name": investor_db_data_load.get('name'), 
                            "dob": datetime.strptime(investor_db_data_load.get('dob'), "%Y-%m-%d").date() if investor_db_data_load.get('dob') else None,
                            "gender": investor_db_data_load.get('gender'),
                            "pan_number": decrypted_details_load.get('pan_number'), 
                            "email_address": decrypted_details_load.get('email_address'), 
                            "mobile_number": decrypted_details_load.get('mobile_number'),
                            "occupation": decrypted_details_load.get('occupation'), 
                            "urban_rural_status": decrypted_details_load.get('urban_rural_status')
                        }
                        st.session_state.form_data_family = {
                            "marital_status": decrypted_details_load.get('marital_status'), 
                            "num_children": decrypted_details_load.get('num_children'), 
                            "num_other_dependents": decrypted_details_load.get('num_other_dependents')
                        }
                        st.session_state.form_data_income_expenses = decrypted_details_load 
                        st.session_state.form_data_risk_questions = {
                            "answers": risk_answers_list_load,
                            "market_linked_experience": decrypted_details_load.get('market_linked_experience')
                        }
                        st.success(f"Profile for {investor_db_data_load.get('name')} loaded. Go to 'Create/Edit Investor Profile' tab to modify.")
                        st.session_state.active_tab_label = main_tabs_config["create_profile"]["label"] # Switch to create profile tab
                        st.rerun()
                    else:
                        st.error("Failed to load investor data.")
        else:
            st.info("No investors found in the database. Create one using the 'Create Investor Profile' tab.")

    with mfd_tab2:
        st.subheader("Aggregated Investor Insights")
        if all_investors:
            df_agg = pd.DataFrame(all_investors, columns=["ID", "Name", "DOB", "Gender", "Occupation", "Location Type", "Risk Score", "Profile ID"])
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Investors", len(df_agg))
                gender_counts = df_agg['Gender'].value_counts().reset_index()
                gender_counts.columns = ['Gender', 'Count']
                fig_gender = px.pie(gender_counts, values='Count', names='Gender', title='Investors by Gender')
                st.plotly_chart(fig_gender, use_container_width=True)
            with col2:
                location_counts = df_agg['Location Type'].value_counts().reset_index()
                location_counts.columns = ['Location Type', 'Count']
                fig_location = px.bar(location_counts, x='Location Type', y='Count', title='Investors by Location Type')
                st.plotly_chart(fig_location, use_container_width=True)
            
            df_agg['Occupation_Simple'] = df_agg['Occupation'].apply(lambda x: "White-Collar" if "White-Collar" in str(x) else ("Blue-Collar" if "Blue-Collar" in str(x) else "Other/Unspecified"))
            occupation_counts = df_agg['Occupation_Simple'].value_counts().reset_index()
            occupation_counts.columns = ['Occupation Category', 'Count']
            fig_occupation = px.pie(occupation_counts, values='Count', names='Occupation Category', title='Investors by Occupation Type (Simplified)')
            st.plotly_chart(fig_occupation, use_container_width=True)

            fig_risk = px.histogram(df_agg, x="Risk Score", title="Distribution of Risk Scores (1-25)", nbins=25)
            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.info("No investor data available for aggregation.")

    with mfd_tab3:
        st.subheader("Print Investor Plans")
        st.write("(Placeholder - Functionality to generate and print/download investor plans in bulk or individually)")

    with mfd_tab4:
        st.subheader("MFD Guide Access")
        st.write("(Placeholder - Access to MFD-specific guides and resources)")

def economic_overview_tab_content(conn):
    st.header("📈 Economic Overview")
    latest_data, is_fallback = get_latest_economic_data_from_db(conn)
    
    if is_fallback:
        st.warning("Displaying fallback economic data. Live data might not be available or fetcher failed.")

    if latest_data:
        st.markdown("#### Key Economic Indicators")
        # Determine number of columns based on data items, max 3-4 for readability
        num_items = len(latest_data)
        num_cols = min(num_items, 3) if num_items > 0 else 1 
        cols = st.columns(num_cols)
        idx = 0
        for key, item_data in latest_data.items():
            current_col = cols[idx % num_cols]
            if isinstance(item_data, dict):
                indicator_name = item_data.get("indicator", key.replace("_", " ").title())
                value = item_data.get("value", "N/A")
                year = item_data.get("year", "N/A")
                display_value = f"{value:.2f}%" if isinstance(value, (int, float)) else str(value)
                current_col.metric(label=f"{indicator_name} ({year})", value=display_value)
            else:
                current_col.metric(label=key.replace("_", " ").title(), value=str(item_data))
            idx += 1
        # Get the actual date of the data from the DB if possible, else use current time as fallback for "checked"
        c = conn.cursor()
        c.execute("SELECT date FROM economic_indicators ORDER BY date DESC LIMIT 1")
        db_date_row = c.fetchone()
        data_date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Default to now
        if db_date_row and db_date_row[0]:
            try: data_date_str = datetime.strptime(db_date_row[0], '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError: pass # Keep default if format is unexpected
        st.caption(f"Data as of: {data_date_str} (Refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    else:
        st.info("No economic data available at the moment.")

    if st.button("🔄 Refresh Economic Data"):
        with st.spinner("Fetching latest economic data..."):
            success, fetched_data = fetch_and_store_economic_data(conn)
            if success:
                st.success("Economic data refreshed!")
                st.session_state.latest_economic_data = fetched_data 
            else:
                st.error("Failed to refresh economic data. Displaying last known or fallback data.")
            st.rerun()

# Main application logic
def main_app_logic():
    conn = init_db()

    if 'latest_economic_data' not in st.session_state:
        st.session_state.latest_economic_data, _ = get_latest_economic_data_from_db(conn)
    
    st.sidebar.title("Navigation")
    
    global main_tabs_config # Declare as global to be accessible in MFD dashboard for tab switching
    main_tabs_ordered_keys = [
        "create_profile", 
        "investor_dashboard", 
        "mfd_dashboard", 
        "financial_goals", 
        "risk_profile", 
        "investor_guide", 
        "economic_overview"
    ]
    
    main_tabs_config = {
        "create_profile": {"label": "🚀 Create/Edit Investor Profile", "func": create_investor_profile_tab_content},
        "investor_dashboard": {"label": "📊 Investor Dashboard", "func": investor_dashboard_tab_content},
        "mfd_dashboard": {"label": "⚙️ MFD Dashboard", "func": mfd_dashboard_tab_content},
        "financial_goals": {"label": "🎯 Financial Goals Management", "func": financial_goals_tab_content},
        "risk_profile": {"label": "⚖️ Risk Profile (Calculated)", "func": risk_profile_tab_content},
        "investor_guide": {"label": "📜 Investor Guide", "func": investor_guide_tab_content},
        "economic_overview": {"label": "📈 Economic Overview", "func": economic_overview_tab_content}
    }

    sidebar_tab_labels = {key: config["label"] for key, config in main_tabs_config.items()}
    ordered_radio_labels = [sidebar_tab_labels[key] for key in main_tabs_ordered_keys]

    if 'active_tab_label' not in st.session_state or st.session_state.active_tab_label not in ordered_radio_labels:
        st.session_state.active_tab_label = ordered_radio_labels[0] 

    st.session_state.active_tab_label = st.sidebar.radio(
        "Go to:", 
        options=ordered_radio_labels, 
        key="sidebar_nav",
        label_visibility="collapsed",
        index=ordered_radio_labels.index(st.session_state.active_tab_label)
    )

    active_tab_key = None
    for key, config_label in sidebar_tab_labels.items():
        if config_label == st.session_state.active_tab_label:
            active_tab_key = key
            break
    
    if active_tab_key and active_tab_key in main_tabs_config:
        main_tabs_config[active_tab_key]["func"](conn)
    else:
        st.error("Selected tab not found. Please select a valid tab from the sidebar.")

if __name__ == "__main__":
    main_app_logic()

