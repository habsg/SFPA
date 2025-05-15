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
    /* Ensure radio buttons are stacked vertically */
    .stRadio > div {
        flex-direction: column;
    }
    .stRadio > div > label {
        display: block; /* Make each radio option take full width */
        margin-bottom: 8px; /* Add some space between radio options */
    }
    .stRadio > div > label > div { /* Styling for the radio item itself */
        background-color: #F3F4F6; /* Light grey for radio items */
        border-radius: 6px;
        padding: 10px 15px; /* Adjusted padding */
        border: 1px solid transparent;
        transition: background-color 0.2s ease, border-color 0.2s ease;
    }
    .stRadio > div > label > input:checked + div { /* Styling for selected radio item */
        background-color: #E0EFFF; /* Lighter blue for selected */
        color: #007AFF; /* Apple blue text */
        border-color: #007AFF;
    }
    .stForm [data-testid="stFormSubmitButton"] button {
         background-color: #28a745; /* Green for submit */
         color: white;
    }
    .stForm [data-testid="stFormSubmitButton"] button:hover {
         background-color: #218838; /* Darker green */
    }
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

INVESTOR_PROFILES_MASTER = {
    "W1": {"desc": "Young Adult, White-Collar, Low Income", "age_min": 22, "age_max": 30, "income_level": "Low", "occupation_type": "White-Collar", "dependents_max": 1},
    "W2": {"desc": "Young Adult, White-Collar, Sufficient Income", "age_min": 22, "age_max": 30, "income_level": "Sufficient", "occupation_type": "White-Collar", "dependents_max": 1},
    "W3": {"desc": "Young Adult, White-Collar, Good Income", "age_min": 22, "age_max": 30, "income_level": "Good", "occupation_type": "White-Collar", "dependents_max": 1},
    "W4": {"desc": "Young Family, White-Collar, Low Income", "age_min": 28, "age_max": 35, "income_level": "Low", "occupation_type": "White-Collar", "dependents_min": 1, "dependents_max": 2, "child_age_max": 7},
    "B1": {"desc": "Young Adult, Blue-Collar, Low Income", "age_min": 22, "age_max": 30, "income_level": "Low", "occupation_type": "Blue-Collar", "dependents_max": 1},
    "W8": {"desc": "Mid-Career Family, White-Collar, Sufficient Income", "age_min": 35, "age_max": 50, "income_level": "Sufficient", "occupation_type": "White-Collar", "dependents_min": 2, "dependents_max": 3, "child_age_min": 8, "child_age_max": 18},
    "B8": {"desc": "Mid-Career Family, Blue-Collar, Sufficient Income", "age_min": 35, "age_max": 50, "income_level": "Sufficient", "occupation_type": "Blue-Collar", "dependents_min": 2, "dependents_max": 3, "child_age_min": 8, "child_age_max": 18},
}

def init_db():
    conn = sqlite3.connect('financial_planning.db', check_same_thread=False)
    c = conn.cursor()
    
    # Create table if it doesn't exist (includes risk_answers)
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
        monthly_household_expenses REAL,
        individual_income REAL, 
        spouse_income REAL 
    )''')

    # Add columns if they don't exist (idempotent ALTER TABLE)
    columns_to_add = {
        "investor_profile_id": "TEXT",
        "pan_number": "TEXT",
        "email_address": "TEXT",
        "mobile_number": "TEXT",
        "gender": "TEXT", # Already in CREATE TABLE, but good for consistency if schema evolved
        "individual_income": "REAL",
        "spouse_income": "REAL",
        "risk_answers": "TEXT", # Explicitly ensure this column exists
        "market_linked_experience": "TEXT",
        "total_investments": "REAL",
        "total_loans": "REAL",
        "monthly_household_expenses": "REAL"
    }
    
    c.execute("PRAGMA table_info(investors)")
    existing_columns = [row[1] for row in c.fetchall()]
    
    for col_name, col_type in columns_to_add.items():
        if col_name not in existing_columns:
            try:
                c.execute(f"ALTER TABLE investors ADD COLUMN {col_name} {col_type}")
                print(f"Added column {col_name} to investors table.") # For logging/debugging
            except sqlite3.OperationalError as e:
                # This might happen             except sqlite3.OperationalError as e:
                print(f"Could not add column {col_name}: {e}") 

    # Specific check and addition for risk_answers to be absolutely sure
    c.execute("PRAGMA table_info(investors)")
    current_investor_columns_after_loop = [row[1] for row in c.fetchall()]
    if "risk_answers" not in current_investor_columns_after_loop:
        print("Attempting a specific ALTER TABLE for 'risk_answers' in 'investors' table.")
        try:
            c.execute("ALTER TABLE investors ADD COLUMN risk_answers TEXT")
            conn.commit() # Commit this change immediately
            print("SUCCESS: Specifically added 'risk_answers' column to 'investors' table and committed.")
        except sqlite3.Error as e: # Catch generic sqlite3.Error
            print(f"CRITICAL FAILURE during specific ALTER for 'risk_answers': {e}")
    else:
        print("'risk_answers' column confirmed to exist in 'investors' table.")

    try: c.execute("ALTER TABLE economic_indicators ADD COLUMN is_fallback BOOLEAN DEFAULT FALSE")
    except sqlite3.OperationalError: pass
    
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
        is_auto_generated BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (investor_id) REFERENCES investors(investor_id)
    )''')
    conn.commit()
    return conn

def generate_investor_id(conn):
    today_str = datetime.now().strftime("%Y%m%d")
    prefix = f"INV-{today_str}-"
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM investors WHERE investor_id LIKE ?", (f"{prefix}%",))
    count = c.fetchone()[0] + 1
    investor_id = f"{prefix}{count:04d}"
    return investor_id

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

def get_investor_life_cycle_stage(age, num_dependents, children_ages=None):
    if 22 <= age <= 30:
        if num_dependents <= 1: return "Young Adult"
    if 28 <= age <= 35:
        return "Young Family"
    if 35 <= age <= 50:
        return "Mid-Career Family"
    if 50 <= age <= 60:
        return "Pre-Retirement"
    if age > 60:
        return "Retirement"
    return "Unknown"

def get_income_level_thresholds(occupation_type, life_cycle_stage):
    base_low_wc = 30000
    base_low_bc = 12000
    multiplier = 1.0
    if life_cycle_stage == "Young Family": multiplier = 1.5
    elif life_cycle_stage == "Mid-Career Family": multiplier = 1.5 * 1.5
    elif life_cycle_stage == "Pre-Retirement" or life_cycle_stage == "Retirement": multiplier = 1.5 * 1.5 * 1.5

    if occupation_type == "White-Collar":
        low_upper = base_low_wc * multiplier
        sufficient_upper = low_upper * 2
    elif occupation_type == "Blue-Collar":
        low_upper = base_low_bc * multiplier
        sufficient_upper = low_upper * (20000/12000)
    else:
        low_upper = base_low_wc * multiplier 
        sufficient_upper = low_upper * 2
    return low_upper, sufficient_upper

def get_income_level_from_value(monthly_income, occupation_type_raw, age, num_dependents):
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
    num_total_dependents = investor_data_dict.get('num_dependents', 0)
    individual_monthly_income = investor_data_dict.get('individual_income', 0.0) 
    income_level_str = get_income_level_from_value(individual_monthly_income, occupation_raw, age, num_total_dependents)

    for profile_id, profile_details in INVESTOR_PROFILES_MASTER.items():
        if profile_details["occupation_type"] == occupation_type and \
           profile_details["income_level"] == income_level_str and \
           profile_details["age_min"] <= age <= profile_details["age_max"]:
            if "dependents_max" in profile_details and num_total_dependents > profile_details["dependents_max"]: continue
            if "dependents_min" in profile_details and num_total_dependents < profile_details["dependents_min"]: continue
            return profile_id
    return "UnknownProfile"

DEFAULT_GOALS_BY_PROFILE_TYPE = {
    "Young Adult": [
        {"name": "Emergency Fund Creation", "type": "Emergency Fund", "priority": 1, "target_months_expenses": 3},
        {"name": "Debt Reduction (if any)", "type": "Debt Reduction", "priority": 2},
        {"name": "Short-term Savings (e.g., Skill Upgradation)", "type": "Short-Term Savings", "priority": 3, "target_years": 2},
        {"name": "Retirement Planning (Start Early)", "type": "Retirement", "priority": 4}
    ],
    "Young Family": [
        {"name": "Emergency Fund (Maintain/Increase)", "type": "Emergency Fund", "priority": 1, "target_months_expenses": 4},
        {"name": "Children's Education Fund", "type": "Education", "priority": 2, "child_ref": "oldest"},
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
}

def auto_generate_financial_goals(conn, investor_id, investor_data_dict, investor_profile_id):
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM financial_goals WHERE investor_id = ? AND is_auto_generated = 1", (investor_id,))
    if c.fetchone()[0] > 0:
        st.info(f"Automatic financial goals already exist for {investor_id}. Skipping generation.")
        return

    age = calculate_age(investor_data_dict.get('dob'), date.today())
    num_dependents = investor_data_dict.get('num_dependents', 0)
    profile_category_for_goals = get_investor_life_cycle_stage(age, num_dependents)
    default_goals_template = DEFAULT_GOALS_BY_PROFILE_TYPE.get(profile_category_for_goals, [])
    generated_goals_count = 0
    for goal_template in default_goals_template:
        goal_name = goal_template["name"]
        goal_type = goal_template["type"]
        priority = goal_template["priority"]
        target_amount = 0
        target_year = date.today().year + (goal_template.get("target_years", 10))
        notes = "Automatically generated based on investor profile."
        monthly_expenses_for_goal_calc = investor_data_dict.get('monthly_household_expenses', 20000) 

        if goal_type == "Emergency Fund":
            target_months = goal_template.get("target_months_expenses", 3)
            target_amount = monthly_expenses_for_goal_calc * target_months 
            target_year = date.today().year + 1
        
        elif goal_type == "Retirement":
            annual_expenses = monthly_expenses_for_goal_calc * 12
            target_amount = annual_expenses * 20 
            retirement_age = goal_template.get("target_age", 60)
            target_year = datetime.strptime(investor_data_dict.get('dob'), "%Y-%m-%d").year + retirement_age
            if target_year <= date.today().year: target_year = date.today().year + 20

        elif goal_type == "Education" and "child_ref" in goal_template:
            target_amount = 500000 
            target_year = date.today().year + 10 + (priority * 2) 
            goal_name = f"{goal_name} (Child {priority-1 if priority > 1 else 1})"

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

def calculate_required_emergency_fund(investor_data_dict):
    monthly_household_expenses = investor_data_dict.get('monthly_household_expenses', 0.0)
    total_emis = investor_data_dict.get('loan_emis', 0.0)
    rent = 0.0
    if investor_data_dict.get('owns_home') is False:
        rent = investor_data_dict.get('rent_amount', 0.0)

    essential_monthly_expenses = monthly_household_expenses + total_emis + rent
    occupation_raw = investor_data_dict.get('occupation', 'Other')
    urban_rural = investor_data_dict.get('urban_rural_status', 'Urban')

    num_months = 0
    if "White-Collar" in occupation_raw: num_months = 6
    elif "Blue-Collar" in occupation_raw: num_months = 4
    else: num_months = 3
    if urban_rural == "Rural": num_months += 1
    required_fund = essential_monthly_expenses * num_months
    return max(0, required_fund)

def calculate_risk_score(db_conn, investor_id_for_log, investor_data_dict, answers_psychometric):
    base_score_100 = 0
    market_experience_raw = investor_data_dict.get('market_linked_experience') # New first question
    experience_points = 0
    # Options for new question: "Yes, extensively", "Yes, moderately", "Yes, a little", "No, never"
    if market_experience_raw == "No, never": experience_points = 0
    elif market_experience_raw == "Yes, a little": experience_points = 4
    elif market_experience_raw == "Yes, moderately": experience_points = 7
    elif market_experience_raw == "Yes, extensively": experience_points = 10
    base_score_100 += experience_points

    raw_psychometric_score = 0
    # Psychometric questions are now answers_psychometric[0] to answers_psychometric[4]
    # Original q1 (greed) is now answers_psychometric[0]
    # Original q2 (preference) is now answers_psychometric[1]
    # Original q3 (willingness) is now answers_psychometric[2]
    # Original q4 (reaction) is now answers_psychometric[3]
    # Original q5 (anxiety) is now answers_psychometric[4]
    greed_map = {"Not likely at all": 1, "Somewhat unlikely": 2, "Neutral": 3, "Somewhat likely": 4, "Very likely": 5}
    preference_map = {"Definitely Fixed Deposit": 1, "Lean towards Fixed Deposit": 2, "Neutral": 3, "Lean towards equity fund": 4, "Definitely equity fund": 5}
    willingness_map = {"Not willing at all": 1, "Somewhat reluctant": 2, "Neutral": 3, "Somewhat willing": 4, "Very willing": 5}
    reaction_map = {"Sell all investments immediately": 1, "Sell some investments and wait": 2, "Hold and wait for recovery": 3, "Hold and monitor closely": 4, "Invest more during the dip": 5}
    anxiety_map = {"Extremely anxious, unable to sleep": 1, "Quite anxious, very concerned": 2, "Mildly anxious, somewhat concerned": 3, "Not very anxious, can manage": 4, "Not anxious at all, comfortable": 5}
    
    if isinstance(answers_psychometric, list) and len(answers_psychometric) == 5 and all(answers_psychometric):
        raw_psychometric_score += greed_map.get(answers_psychometric[0], 1)
        raw_psychometric_score += preference_map.get(answers_psychometric[1], 1)
        raw_psychometric_score += willingness_map.get(answers_psychometric[2], 1)
        raw_psychometric_score += reaction_map.get(answers_psychometric[3], 1)
        raw_psychometric_score += anxiety_map.get(answers_psychometric[4], 1)
        stated_risk_points = ((raw_psychometric_score - 5) / 20) * 30
        base_score_100 += stated_risk_points
    else: stated_risk_points = 0

    current_emergency_fund_saved = investor_data_dict.get('current_emergency_fund', 0.0)
    required_emergency_fund_calculated = calculate_required_emergency_fund(investor_data_dict) 
    adequacy_ratio = current_emergency_fund_saved / required_emergency_fund_calculated if required_emergency_fund_calculated > 0 else 0
    if adequacy_ratio < 0.25: emergency_points = 2
    elif adequacy_ratio < 0.50: emergency_points = 5
    elif adequacy_ratio < 0.75: emergency_points = 9
    elif adequacy_ratio < 1.00: emergency_points = 13
    elif adequacy_ratio < 1.50: emergency_points = 17
    else: emergency_points = 20
    base_score_100 += emergency_points

    individual_income_val = investor_data_dict.get('individual_income', 0.0)
    total_emi_val = investor_data_dict.get('loan_emis', 0.0) 
    debt_burden_ratio = total_emi_val / individual_income_val if individual_income_val > 0 else 1
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
    num_deps_for_income_level = investor_data_dict.get('num_dependents', 0)
    income_level_str = get_income_level_from_value(individual_income_val, occupation_type_raw, age_val, num_deps_for_income_level)
    occupation_simple = "White-Collar" if "White-Collar" in occupation_type_raw else "Blue-Collar" if "Blue-Collar" in occupation_type_raw else "Other"
    income_occupation_points = 0
    if (occupation_simple == "White-Collar" and income_level_str == "Good") or \
       (occupation_simple == "Blue-Collar" and income_level_str == "Good"): income_occupation_points = 10
    elif (occupation_simple == "White-Collar" and income_level_str == "Sufficient") or \
         (occupation_simple == "Blue-Collar" and income_level_str == "Good"): income_occupation_points = 8
    elif (occupation_simple == "White-Collar" and income_level_str == "Low") or \
         (occupation_simple == "Blue-Collar" and income_level_str == "Sufficient"): income_occupation_points = 6
    elif (occupation_simple == "Blue-Collar" and income_level_str == "Low"): income_occupation_points = 4
    base_score_100 += income_occupation_points
    base_score_100 = max(0, min(100, base_score_100))

    latest_economic_data, is_fallback = get_latest_economic_data_from_db(db_conn)
    gdp_growth = latest_economic_data.get("gdp_growth", {}).get("value", 6.5) 
    cpi_inflation = latest_economic_data.get("cpi_inflation", {}).get("value", 5.0)
    economic_conditions_summary = f"GDP Growth: {gdp_growth}%, CPI Inflation: {cpi_inflation}%"
    economic_adjustment_factor = 0
    if gdp_growth > 7 and cpi_inflation < 4: economic_adjustment_factor = 2
    elif gdp_growth < 5 or cpi_inflation > 7: economic_adjustment_factor = -2
    elif gdp_growth < 6 or cpi_inflation > 6: economic_adjustment_factor = -1
    elif gdp_growth > 6 and cpi_inflation < 5: economic_adjustment_factor = 1
    
    adjusted_score_100 = base_score_100 + economic_adjustment_factor
    goal_adjustment_details_str = "No specific goal adjustments applied in this version."
    final_risk_score_25 = math.ceil(max(1, min(25, (adjusted_score_100 / 4))))

    log_reason = "Standard calculation."
    if is_fallback: log_reason += " Economic data is fallback."
    if not all(answers_psychometric or []): log_reason += " Psychometric risk questions incomplete."
    if not investor_data_dict.get('market_linked_experience'): log_reason += " Market experience question incomplete."

    c = db_conn.cursor()
    c.execute("""INSERT INTO risk_adjustment_log 
                 (investor_id, log_timestamp, base_risk_score_100, economic_conditions_summary, economic_adjustment_factor, goal_adjustment_details, final_risk_score_25, reason)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
              (investor_id_for_log, datetime.now().isoformat(), base_score_100, economic_conditions_summary, economic_adjustment_factor, goal_adjustment_details_str, final_risk_score_25, log_reason))
    db_conn.commit()
    return final_risk_score_25, base_score_100, economic_adjustment_factor, goal_adjustment_details_str

def personal_info_tab_content(conn, investor_id):
    data = st.session_state.form_data_personal
    name = st.text_input("Full Name", key=f"name_{investor_id}", value=data.get("name", ""))
    dob_val = data.get("dob")
    if isinstance(dob_val, str): 
        try: dob_val = datetime.strptime(dob_val, "%Y-%m-%d").date()
        except ValueError: dob_val = None
    dob = st.date_input("Date of Birth", key=f"dob_{investor_id}", value=dob_val, min_value=date(1920,1,1), max_value=date.today() - timedelta(days=365*18))
    gender_options = ["Male", "Female", "Other", "Prefer not to say"]
    gender = st.selectbox("Gender", gender_options, key=f"gender_{investor_id}", index=gender_options.index(data.get("gender")) if data.get("gender") in gender_options else 0)
    pan_number = st.text_input("PAN Number (Optional)", key=f"pan_{investor_id}", value=data.get("pan_number", ""))
    email_address = st.text_input("Email Address (Optional)", key=f"email_{investor_id}", value=data.get("email_address", ""))
    mobile_number = st.text_input("Mobile Number (Optional)", key=f"mobile_{investor_id}", value=data.get("mobile_number", ""))
    occupation_options = [
        "Salaried (White-Collar - Private Sector)", "Salaried (White-Collar - Government/PSU)",
        "Self-Employed Professional (e.g., Doctor, Lawyer, CA)", "Business Owner/Entrepreneur (White-Collar)",
        "Salaried (Blue-Collar - Skilled, e.g., Technician, Electrician)", "Salaried (Blue-Collar - Unskilled, e.g., Laborer, Helper)",
        "Self-Employed (Blue-Collar, e.g., Driver, Plumber, Small Shop Owner)", "Agriculture/Farmer",
        "Homemaker", "Student", "Retired", "Unemployed", "Other"
    ]
    occupation = st.selectbox("Occupation Category", occupation_options, key=f"occupation_{investor_id}", index=occupation_options.index(data.get("occupation")) if data.get("occupation") in occupation_options else 0)
    urban_rural_options = ["Urban", "Rural"]
    urban_rural_status = st.selectbox("Residential Status", urban_rural_options, key=f"urban_rural_{investor_id}", index=urban_rural_options.index(data.get("urban_rural_status")) if data.get("urban_rural_status") in urban_rural_options else 0)
    
    st.session_state.form_data_personal = {
        "name": name, "dob": str(dob) if dob else None, "gender": gender,
        "pan_number": pan_number, "email_address": email_address, "mobile_number": mobile_number,
        "occupation": occupation, "urban_rural_status": urban_rural_status
    }

def family_dependents_tab_content(conn, investor_id):
    if 'form_data_family' not in st.session_state or not isinstance(st.session_state.form_data_family, dict):
        st.session_state.form_data_family = {'marital_status': "Single", 'num_dependents': 0, 'dependents_details': []}
    
    data = st.session_state.form_data_family
    
    marital_options = ["Single", "Married", "Divorced", "Widowed"]
    marital_status_val = data.get("marital_status", "Single")
    marital_status = st.selectbox(
        "Marital Status", 
        marital_options, 
        key=f"marital_status_{investor_id}", 
        index=marital_options.index(marital_status_val) if marital_status_val in marital_options else 0
    )

    num_dependents_val = data.get("num_dependents", 0)
    num_dependents = st.number_input(
        "Number of Dependents", 
        min_value=0, 
        max_value=5, 
        step=1, 
        key=f"num_dependents_{investor_id}", 
        value=int(num_dependents_val)
    )

    dependents_details_list = data.get('dependents_details', [])
    if len(dependents_details_list) != num_dependents:
        new_details_list = []
        for i in range(num_dependents):
            if i < len(dependents_details_list) and isinstance(dependents_details_list[i], dict):
                new_details_list.append(dependents_details_list[i])
            else:
                new_details_list.append({'age': None, 'gender': "Male"})
        dependents_details_list = new_details_list[:num_dependents]

    current_dependents_data_to_save = []
    if num_dependents > 0:
        st.markdown("---_Dependent Details_---")
        for i in range(num_dependents):
            dep_data_item = dependents_details_list[i] if i < len(dependents_details_list) and isinstance(dependents_details_list[i], dict) else {'age': None, 'gender': "Male"}
            
            col1, col2 = st.columns(2)
            with col1:
                dep_age_val = dep_data_item.get('age')
                dep_age = st.number_input(
                    f"Age of Dependent {i+1}", 
                    min_value=0, 
                    max_value=120, 
                    step=1, 
                    key=f"dep_age_{investor_id}_{i}", 
                    value=dep_age_val,
                    placeholder="Enter age"
                )
            with col2:
                dep_gender_val = dep_data_item.get('gender', "Male")
                dep_gender_options = ["Male", "Female", "Other"]
                dep_gender = st.selectbox(
                    f"Gender of Dependent {i+1}", 
                    dep_gender_options, 
                    key=f"dep_gender_{investor_id}_{i}",
                    index=dep_gender_options.index(dep_gender_val) if dep_gender_val in dep_gender_options else 0
                )
            current_dependents_data_to_save.append({'age': dep_age, 'gender': dep_gender})
    
    st.session_state.form_data_family = {
        "marital_status": marital_status,
        "num_dependents": num_dependents,
        "dependents_details": current_dependents_data_to_save
    }

def finance_tab_content(conn, investor_id):
    data = st.session_state.form_data_finance
    individual_income = st.number_input("Individual Monthly Income (INR)", min_value=0.0, step=1000.0, key=f"individual_income_{investor_id}", value=data.get("individual_income", 0.0))
    spouse_income = st.number_input("Spouse Monthly Income (INR, fill 0 if not applicable)", min_value=0.0, step=1000.0, key=f"spouse_income_{investor_id}", value=data.get("spouse_income", 0.0))
    monthly_household_expenses = st.number_input("Monthly Household Expenses (Non-discretionary, excluding EMIs) (INR)", min_value=0.0, step=500.0, key=f"monthly_household_expenses_{investor_id}", value=data.get("monthly_household_expenses", 0.0))
    current_emergency_fund_saved = st.number_input("Emergency Fund Saved (INR)", min_value=0.0, step=5000.0, key=f"current_emergency_fund_{investor_id}", value=data.get("current_emergency_fund", 0.0))
    loan_emis = st.number_input("Total Monthly Loan EMIs (Home, Car, Personal, etc.) (INR)", min_value=0.0, step=500.0, key=f"loan_emis_{investor_id}", value=data.get("loan_emis", 0.0))
    owns_home_val = data.get("owns_home", False)
    owns_home_idx = 0 if owns_home_val else 1
    owns_home_radio = st.radio("Do you own your primary residence?", ("Yes", "No"), key=f"owns_home_{investor_id}", index=owns_home_idx, horizontal=True)
    owns_home = owns_home_radio == "Yes"
    rent_amount = 0.0
    if not owns_home:
        rent_amount = st.number_input("Monthly Rent Amount (if applicable) (INR)", min_value=0.0, step=500.0, key=f"rent_{investor_id}", value=data.get("rent_amount", 0.0))
    
    st.session_state.form_data_finance = {
        "individual_income": individual_income, "spouse_income": spouse_income,
        "monthly_household_expenses": monthly_household_expenses,
        "current_emergency_fund": current_emergency_fund_saved,
        "loan_emis": loan_emis, "owns_home": owns_home, "rent_amount": rent_amount
    }

def risk_assessment_questions_tab_content(conn, investor_id):
    if 'form_data_risk_questions' not in st.session_state or not isinstance(st.session_state.form_data_risk_questions, dict):
        st.session_state.form_data_risk_questions = {"market_linked_experience": None, "answers": [None]*5}

    data = st.session_state.form_data_risk_questions
    market_exp_val = data.get("market_linked_experience")
    psychometric_answers_val = data.get("answers", [None]*5)
    if not isinstance(psychometric_answers_val, list) or len(psychometric_answers_val) != 5:
        psychometric_answers_val = [None]*5 # Ensure it's a list of 5

    st.info("Please answer all the following questions to help us understand your risk tolerance. All questions are mandatory.")
    st.markdown("<br>", unsafe_allow_html=True) # Add some space

    # Question 1 (New first question)
    q_market_exp_options = ["No, never", "Yes, a little", "Yes, moderately", "Yes, extensively"]
    market_linked_experience_ans = st.radio(
        "**1. Have you ever invested in market-linked investments (stocks, mutual funds, etc.)?**", 
        q_market_exp_options, 
        key=f"market_exp_new_{investor_id}", 
        index=q_market_exp_options.index(market_exp_val) if market_exp_val in q_market_exp_options else None,
        horizontal=False # Vertical layout for options
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Psychometric Questions (Now Q2 to Q6)
    psychometric_questions_config = [
        {"label": "How likely are you to invest a significant portion of your annual income in a high-risk, high-reward venture?", 
         "options": ["Not likely at all", "Somewhat unlikely", "Neutral", "Somewhat likely", "Very likely"], "key_suffix": "q_greed"},
        {"label": "If you were given a choice between a guaranteed return (like a Fixed Deposit) and a potentially higher but uncertain return (like an equity fund), which would you prefer for a major portion of your long-term savings?", 
         "options": ["Definitely Fixed Deposit", "Lean towards Fixed Deposit", "Neutral", "Lean towards equity fund", "Definitely equity fund"], "key_suffix": "q_preference"},
        {"label": "How willing are you to tolerate short-term losses in your investments for the potential of higher long-term gains?", 
         "options": ["Not willing at all", "Somewhat reluctant", "Neutral", "Somewhat willing", "Very willing"], "key_suffix": "q_willingness"},
        {"label": "Imagine the stock market drops by 20% in a month. What would be your most likely reaction regarding your equity investments?", 
         "options": ["Sell all investments immediately", "Sell some investments and wait", "Hold and wait for recovery", "Hold and monitor closely", "Invest more during the dip"], "key_suffix": "q_reaction"},
        {"label": "How would you describe your general level of anxiety when thinking about your financial future and investment performance?", 
         "options": ["Extremely anxious, unable to sleep", "Quite anxious, very concerned", "Mildly anxious, somewhat concerned", "Not very anxious, can manage", "Not anxious at all, comfortable"], "key_suffix": "q_anxiety"}
    ]

    current_psychometric_answers = []
    for i, q_config in enumerate(psychometric_questions_config):
        ans = st.radio(
            f"**{i+2}. {q_config['label']}**", 
            q_config['options'], 
            key=f"{q_config['key_suffix']}_{investor_id}", 
            index=q_config['options'].index(psychometric_answers_val[i]) if psychometric_answers_val[i] in q_config['options'] else None,
            horizontal=False # Vertical layout for options
        )
        current_psychometric_answers.append(ans)
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.session_state.form_data_risk_questions = {
        "market_linked_experience": market_linked_experience_ans,
        "answers": current_psychometric_answers
    }


def create_investor_profile_tab_content(conn):
    st.header("📝 Create/Edit Investor Profile")

    if 'current_investor_id' not in st.session_state or not st.session_state.current_investor_id:
        if st.button("Start New Investor Profile", key="start_new_profile_direct"):
            st.session_state.current_investor_id = generate_investor_id(conn)
            st.session_state.current_profile_creator_step = 0
            st.session_state.form_data_personal = {}
            st.session_state.form_data_family = {'marital_status': "Single", 'num_dependents': 0, 'dependents_details': []}
            st.session_state.form_data_finance = {}
            st.session_state.form_data_risk_questions = {"market_linked_experience": None, "answers": [None]*5}
            st.rerun()
        st.info("Click 'Start New Investor Profile' to begin or select an existing investor from the MFD Dashboard to edit.")
        return

    investor_id = st.session_state.current_investor_id
    st.subheader(f"Investor ID: {investor_id}")

    if 'current_profile_creator_step' not in st.session_state: st.session_state.current_profile_creator_step = 0
    if 'form_data_personal' not in st.session_state: st.session_state.form_data_personal = {}
    if 'form_data_family' not in st.session_state or not isinstance(st.session_state.form_data_family, dict): 
        st.session_state.form_data_family = {'marital_status': "Single", 'num_dependents': 0, 'dependents_details': []}
    if 'form_data_finance' not in st.session_state: st.session_state.form_data_finance = {}
    if 'form_data_risk_questions' not in st.session_state or not isinstance(st.session_state.form_data_risk_questions, dict): 
        st.session_state.form_data_risk_questions = {"market_linked_experience": None, "answers": [None]*5}

    profile_steps_config = [
        {"name": "Personal Info", "content_func": personal_info_tab_content, "data_key": "form_data_personal", 
         "mandatory_fields": {"name": "Full Name", "dob": "Date of Birth", "gender": "Gender", "occupation": "Occupation Category", "urban_rural_status": "Residential Status"}},
        {"name": "Family & Dependents", "content_func": family_dependents_tab_content, "data_key": "form_data_family", 
         "mandatory_fields": {"marital_status": "Marital Status"}},
        {"name": "Finance Tab", "content_func": finance_tab_content, "data_key": "form_data_finance", 
         "mandatory_fields": {"individual_income": "Individual Monthly Income", "monthly_household_expenses": "Monthly Household Expenses", "current_emergency_fund": "Emergency Fund Saved", "loan_emis": "Total Monthly Loan EMIs", "owns_home": "Owns Home Status"}},
        {"name": "Risk Assessment Questions", "content_func": risk_assessment_questions_tab_content, "data_key": "form_data_risk_questions", 
         "mandatory_fields": {}} # Custom validation for all questions
    ]

    current_step_index = st.session_state.current_profile_creator_step
    if current_step_index >= len(profile_steps_config): 
        st.session_state.current_profile_creator_step = 0
        current_step_index = 0
        
    current_step = profile_steps_config[current_step_index]

    st.markdown(f"### Step {current_step_index + 1} of {len(profile_steps_config)}: {current_step['name']}")
    current_step["content_func"](conn, investor_id)

    is_current_step_valid = True
    missing_fields_display = []
    current_data_for_validation = st.session_state[current_step['data_key']]

    for field_key, field_name in current_step['mandatory_fields'].items():
        value = current_data_for_validation.get(field_key)
        if value is None or (isinstance(value, str) and not value.strip()):
            if not (field_key == "owns_home" and value is False): 
                 is_current_step_valid = False
                 if field_name not in missing_fields_display: missing_fields_display.append(field_name)
    
    if current_step['name'] == "Family & Dependents":
        family_data_val = st.session_state.form_data_family
        if family_data_val.get("num_dependents") is None: 
            is_current_step_valid = False
            if "Number of Dependents" not in missing_fields_display: missing_fields_display.append("Number of Dependents")
        else:
            num_deps = family_data_val.get("num_dependents", 0)
            if num_deps > 0:
                dependents_details_val = family_data_val.get("dependents_details", [])
                if len(dependents_details_val) == num_deps:
                    for i in range(num_deps):
                        dep_detail = dependents_details_val[i]
                        if dep_detail.get('age') is None:
                            is_current_step_valid = False
                            if f"Age of Dependent {i+1}" not in missing_fields_display: missing_fields_display.append(f"Age of Dependent {i+1}")
                        if not dep_detail.get('gender'):
                            is_current_step_valid = False
                            if f"Gender of Dependent {i+1}" not in missing_fields_display: missing_fields_display.append(f"Gender of Dependent {i+1}")
                else: 
                    is_current_step_valid = False
                    if "Details for all dependents" not in missing_fields_display: missing_fields_display.append("Details for all dependents")

    if current_step['name'] == "Risk Assessment Questions":
        risk_data = st.session_state.form_data_risk_questions
        if not risk_data.get("market_linked_experience"):
            is_current_step_valid = False
            if "1. Market Linked Experience question" not in missing_fields_display: missing_fields_display.append("1. Market Linked Experience question")
        
        psychometric_answers = risk_data.get("answers", [None]*5)
        if not isinstance(psychometric_answers, list) or len(psychometric_answers) != 5 or not all(psychometric_answers):
            is_current_step_valid = False
            if "All 5 psychometric risk questions (Questions 2-6)" not in missing_fields_display: 
                missing_fields_display.append("All 5 psychometric risk questions (Questions 2-6)")

    if not is_current_step_valid and missing_fields_display:
        st.error(f"Please fill in the following mandatory fields: {', '.join(sorted(list(set(missing_fields_display))))}.")

    button_label = "Save & Next" if current_step_index < len(profile_steps_config) - 1 else "Save & Submit Profile"
    
    cols_nav_button = st.columns([3,1])
    with cols_nav_button[1]:
        if st.button(button_label, key=f"nav_button_{current_step_index}", disabled=not is_current_step_valid, use_container_width=True):
            if current_step_index < len(profile_steps_config) - 1:
                st.session_state.current_profile_creator_step += 1
                st.rerun()
            else:
                try:
                    personal_data = st.session_state.form_data_personal
                    family_data = st.session_state.form_data_family
                    finance_data = st.session_state.form_data_finance
                    risk_data = st.session_state.form_data_risk_questions

                    full_investor_data_for_calc_and_encrypt = {
                        **personal_data,
                        "marital_status": family_data.get("marital_status"),
                        "num_dependents": family_data.get("num_dependents", 0),
                        "dependents_details": family_data.get("dependents_details", []),
                        **finance_data,
                        "market_linked_experience": risk_data.get("market_linked_experience"),
                    }
                    
                    assigned_profile_id = assign_investor_profile_id(full_investor_data_for_calc_and_encrypt)
                    encrypted_financial_details = encrypt_data(full_investor_data_for_calc_and_encrypt)
                    psychometric_answers_list = risk_data.get("answers", [None]*5)
                    calculated_risk_score, base_s, econ_adj, goal_adj = calculate_risk_score(conn, investor_id, full_investor_data_for_calc_and_encrypt, psychometric_answers_list)
                    db_dependents_json = json.dumps(family_data)
                    db_risk_answers_json = json.dumps(psychometric_answers_list)

                    c = conn.cursor()
                    c.execute("""INSERT OR REPLACE INTO investors 
                                 (investor_id, name, dob, gender, financial_details, occupation, urban_rural_status, 
                                  dependents, home_ownership, rent_amount, emi_amount, emergency_fund, 
                                  risk_score, risk_answers, plan_in_action_date, consent_log, market_linked_experience, 
                                  investor_profile_id, pan_number, email_address, mobile_number, 
                                  total_investments, total_loans, monthly_household_expenses, individual_income, spouse_income)
                                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (investor_id, 
                               personal_data.get('name'), personal_data.get('dob'), personal_data.get('gender'),
                               encrypted_financial_details, personal_data.get('occupation'), personal_data.get('urban_rural_status'),
                               db_dependents_json, 
                               finance_data.get('owns_home'), finance_data.get('rent_amount'), finance_data.get('loan_emis'), finance_data.get('current_emergency_fund'),
                               calculated_risk_score, db_risk_answers_json, 
                               None, None, 
                               full_investor_data_for_calc_and_encrypt.get('market_linked_experience'), 
                               assigned_profile_id,
                               personal_data.get('pan_number'), personal_data.get('email_address'), personal_data.get('mobile_number'),
                               finance_data.get('total_investments', 0.0), finance_data.get('total_loans', 0.0), 
                               finance_data.get('monthly_household_expenses'), finance_data.get('individual_income'), finance_data.get('spouse_income')
                               ))
                    conn.commit()
                    st.success(f"Investor profile for {personal_data.get('name')} ({investor_id}) saved successfully!")
                    st.balloons()
                    auto_generate_financial_goals(conn, investor_id, full_investor_data_for_calc_and_encrypt, assigned_profile_id)
                    st.session_state.current_investor_id = None 
                    st.session_state.current_profile_creator_step = 0
                    st.session_state.active_tab_label = main_tabs_config["mfd_dashboard"]["label"]
                    st.rerun()
                except sqlite3.Error as e:
                    st.error(f"Database error saving profile: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred during save: {e}")
                    st.exception(e)

def financial_goals_tab_content(conn):
    st.header("🎯 Financial Goals Management")
    st.write("This section will allow MFDs to manage financial goals for investors. (Under Construction)")
    if 'selected_investor_for_mfd_dashboard' in st.session_state and st.session_state.selected_investor_for_mfd_dashboard:
        investor_id = st.session_state.selected_investor_for_mfd_dashboard
        st.write(f"Managing goals for Investor ID: {investor_id}")
    else:
        st.info("Please select an investor from the MFD Dashboard first.")

def risk_profile_tab_content(conn):
    st.header("⚖️ Risk Profile (Calculated)")
    if 'selected_investor_for_mfd_dashboard' in st.session_state and st.session_state.selected_investor_for_mfd_dashboard:
        investor_id = st.session_state.selected_investor_for_mfd_dashboard
        c = conn.cursor()
        c.execute("SELECT name, risk_score, risk_answers, financial_details, market_linked_experience FROM investors WHERE investor_id = ?", (investor_id,))
        investor_record = c.fetchone()
        if investor_record:
            name, risk_score_val, risk_answers_json, financial_details_encrypted, market_exp_val_db = investor_record
            st.subheader(f"Risk Profile for: {name} ({investor_id})")
            st.metric(label="Calculated Risk Score (out of 25)", value=risk_score_val if risk_score_val is not None else "N/A")
            
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

            st.markdown("---_**Risk Profile Implications (Illustrative)**_---")
            if risk_score_val is not None:
                if risk_score_val <= 5: st.info("**Conservative:** Investor has a very low risk tolerance. Prefers capital preservation over growth. Suitable for very low-risk investments like FDs, PPF, Debt Funds (Short Duration).")
                elif risk_score_val <= 10: st.info("**Moderately Conservative:** Investor is cautious but willing to take minimal risk for slightly better returns. Suitable for a mix of FDs, Debt Funds, and a small allocation to Balanced/Hybrid Funds.")
                elif risk_score_val <= 15: st.info("**Balanced:** Investor is willing to take moderate risks for moderate returns. Suitable for a diversified portfolio including Debt Funds, Balanced/Hybrid Funds, and some allocation to Large-Cap Equity Funds.")
                elif risk_score_val <= 20: st.info("**Moderately Aggressive:** Investor is comfortable with taking significant risks for potentially high returns. Suitable for a portfolio with higher allocation to Equity Funds (Large, Mid, Small-Cap) and some alternative investments.")
                else: st.info("**Aggressive:** Investor has a high risk tolerance and is seeking maximum returns, understanding the potential for significant losses. Suitable for a portfolio heavily weighted towards Equities, including Small-Cap and Thematic Funds, and alternative investments.")
            else:
                st.warning("Risk score not yet calculated for this investor.")
        else:
            st.warning(f"No investor record found for ID: {investor_id}")
    else:
        st.info("Select an investor from the MFD Dashboard to view their calculated risk profile.")

def investor_dashboard_tab_content(conn):
    st.header("📊 Investor Dashboard")
    st.write("Select an investor to view their detailed financial summary and plan.")
    c = conn.cursor()
    c.execute("SELECT investor_id, name FROM investors ORDER BY name")
    investors = c.fetchall()
    investor_options = {f"{name} ({inv_id})": inv_id for inv_id, name in investors}
    selected_investor_display = st.selectbox("Select Investor", options=list(investor_options.keys()), index=None, placeholder="Search or select an investor...")
    
    if selected_investor_display:
        investor_id = investor_options[selected_investor_display]
        st.session_state.selected_investor_for_mfd_dashboard = investor_id
        c.execute("SELECT * FROM investors WHERE investor_id = ?", (investor_id,))
        investor_data_tuple = c.fetchone()
        if investor_data_tuple:
            cols_desc = [desc[0] for desc in c.description]
            investor_db_data = dict(zip(cols_desc, investor_data_tuple))
            st.subheader(f"Details for: {investor_db_data['name']} ({investor_id})")
            financial_details_decrypted = decrypt_data(investor_db_data.get('financial_details'))
            if not financial_details_decrypted: financial_details_decrypted = {} 
            
            family_data_display = {} 
            dependents_json_str = investor_db_data.get('dependents')
            if dependents_json_str:
                try: family_data_display = json.loads(dependents_json_str)
                except: pass

            detail_tabs_list = ["Summary & Profile", "Family Details", "Finance Overview", "Financial Goals", "Investment Plan (Auto)", "Risk Details"]
            summary_tab, family_display_tab, finance_display_tab, goals_tab, plan_tab, risk_details_tab = st.tabs(detail_tabs_list)
            with summary_tab:
                st.markdown(f"**Name:** {investor_db_data.get('name', 'N/A')}")
                st.markdown(f"**DOB:** {investor_db_data.get('dob', 'N/A')} (Age: {calculate_age(investor_db_data.get('dob'), date.today())})")
                st.markdown(f"**Gender:** {investor_db_data.get('gender', 'N/A')}")
                st.markdown(f"**Occupation:** {financial_details_decrypted.get('occupation', 'N/A')}")
                st.markdown(f"**Residential Status:** {financial_details_decrypted.get('urban_rural_status', 'N/A')}")
                st.markdown(f"**Assigned Profile ID:** {investor_db_data.get('investor_profile_id', 'N/A')}")
                st.markdown(f"**Calculated Risk Score:** {investor_db_data.get('risk_score', 'N/A')}/25")
            with family_display_tab:
                st.subheader("Family Information")
                st.markdown(f"**Marital Status:** {family_data_display.get('marital_status', 'N/A')}")
                num_deps_display = family_data_display.get('num_dependents', 0)
                st.markdown(f"**Number of Dependents:** {num_deps_display}")
                if num_deps_display > 0:
                    deps_details_display = family_data_display.get('dependents_details', [])
                    for i, dep in enumerate(deps_details_display):
                        st.markdown(f"  - Dependent {i+1}: Age {dep.get('age', 'N/A')}, Gender {dep.get('gender', 'N/A')}")
            with finance_display_tab:
                st.subheader("Finance Overview")
                st.markdown(f"**Individual Monthly Income:** ₹{investor_db_data.get("individual_income", 0):,.0f}")
                st.markdown(f"**Spouse Monthly Income:** ₹{investor_db_data.get("spouse_income", 0):,.0f}")
                st.markdown(f"**Monthly Household Expenses (Non-discretionary):** ₹{investor_db_data.get("monthly_household_expenses", 0):,.0f}")
                st.markdown(f"**Total Monthly Loan EMIs:** ₹{investor_db_data.get("emi_amount", 0):,.0f}")
                st.markdown(f"**Owns Home:** {"Yes" if investor_db_data.get("home_ownership") else "No"}")
                if not investor_db_data.get("home_ownership"):
                    st.markdown(f"**Monthly Rent:** ₹{investor_db_data.get("rent_amount", 0):,.0f}")
                st.markdown(f"**Emergency Fund Saved:** ₹{investor_db_data.get("emergency_fund", 0):,.0f}")
                # Prepare a dictionary for calculate_required_emergency_fund using direct DB fields
                finance_data_for_calc = {
                    "individual_income": investor_db_data.get("individual_income", 0),
                    "spouse_income": investor_db_data.get("spouse_income", 0),
                    "monthly_household_expenses": investor_db_data.get("monthly_household_expenses", 0),
                    "loan_emis": investor_db_data.get("emi_amount", 0)
                }
                required_ef = calculate_required_emergency_fund(finance_data_for_calc)
                st.markdown(f"_Required Emergency Fund (Est.): ₹{required_ef:,.0f}_)")
            with goals_tab:
                st.subheader("Financial Goals")
                c.execute("SELECT goal_name, goal_type, target_amount, target_year, priority, is_auto_generated FROM financial_goals WHERE investor_id = ? ORDER BY priority, target_year", (investor_id,))
                goals = c.fetchall()
                if goals:
                    goals_df = pd.DataFrame(goals, columns=["Goal Name", "Type", "Target Amount (₹)", "Target Year", "Priority", "Auto-Generated"])
                    goals_df["Target Amount (₹)"] = goals_df["Target Amount (₹)"].apply(lambda x: f"{x:,.0f}")
                    st.dataframe(goals_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No financial goals recorded.")
            with plan_tab:
                st.subheader("Automated Investment Plan")
                st.write("(Placeholder - This section will show the auto-generated investment plan.)")
            with risk_details_tab:
                st.subheader("Risk Assessment Details")
                st.metric(label="Calculated Risk Score (out of 25)", value=investor_db_data.get('risk_score', 'N/A'))
                market_exp_display_db = investor_db_data.get('market_linked_experience') # This is the direct DB value
                st.markdown(f"**1. Experience with market-linked products:** {market_exp_display_db if market_exp_display_db else 'N/A'}")
                
                risk_answers_json_display = investor_db_data.get('risk_answers')
                if risk_answers_json_display:
                    try: risk_answers_list_display = json.loads(risk_answers_json_display)
                    except json.JSONDecodeError: risk_answers_list_display = []
                    st.markdown("**Responses to Psychometric Questions (2-6):**")
                    questions_text_psychometric = [
                        "Likelihood to invest significantly in high-risk/high-reward venture?",
                        "Preference for guaranteed vs. uncertain returns for long-term savings?",
                        "Willingness to tolerate short-term losses for potential long-term gains?",
                        "Likely reaction to a 20% stock market drop?",
                        "General anxiety level about financial future and investments?"
                    ]
                    if isinstance(risk_answers_list_display, list) and len(risk_answers_list_display) == 5:
                        for i, ans in enumerate(risk_answers_list_display):
                            st.markdown(f"- {i+2}. {questions_text_psychometric[i]}: **{ans}**")
                    else: st.warning("Psychometric risk answers format incorrect or incomplete.")
                else: st.warning("No psychometric risk answers recorded.")

                c.execute("""SELECT base_risk_score_100, economic_conditions_summary, economic_adjustment_factor, goal_adjustment_details, final_risk_score_25, reason, log_timestamp 
                             FROM risk_adjustment_log WHERE investor_id = ? ORDER BY log_timestamp DESC LIMIT 1""", (investor_id,))
                log_entry_display = c.fetchone()
                if log_entry_display:
                    st.markdown("**Latest Risk Calculation Breakdown:**")
                    st.markdown(f"  - Base Score (raw, out of 100): {log_entry_display[0]:.2f}")
                    st.markdown(f"  - Economic Conditions Considered: {log_entry_display[1]}")
                    st.markdown(f"  - Economic Adjustment Factor: {log_entry_display[2]:.2f}")
                    st.markdown(f"  - Goal Adjustments: {log_entry_display[3]}")
                    st.markdown(f"  - Final Calculated Score (out of 25): {log_entry_display[4]}")
                    st.markdown(f"  - Reason/Notes: {log_entry_display[5]}")
                    st.caption(f"  _Calculation as of: {datetime.fromisoformat(log_entry_display[6]).strftime('%Y-%m-%d %H:%M')}_ ")
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
        c.execute("SELECT investor_id, name, dob, gender, occupation, urban_rural_status AS location_type, risk_score, investor_profile_id, individual_income AS indiv_income, spouse_income FROM investors ORDER BY name")
        all_investors = c.fetchall()
        if all_investors:
            df_investors = pd.DataFrame(all_investors, columns=["ID", "Name", "DOB", "Gender", "Occupation", "Location Type", "Risk Score", "Profile ID", "Indiv. Income", "Spouse Income"])
            st.dataframe(df_investors, use_container_width=True, hide_index=True)
            st.markdown("---_Search & Load Investor for Editing_---")
            investor_options_load = {f"{name} ({inv_id})": inv_id for inv_id, name, *_ in all_investors}
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
                        
                        # Load risk answers (psychometric)
                        risk_answers_list_load = []
                        try: risk_answers_list_load = json.loads(investor_db_data_load.get('risk_answers', '[]'))
                        except: pass
                        if not isinstance(risk_answers_list_load, list) or len(risk_answers_list_load) != 5: risk_answers_list_load = [None]*5
                        
                        # Load market linked experience (new first question)
                        market_exp_load = investor_db_data_load.get('market_linked_experience') # Direct from DB column
                        if market_exp_load is None: # Fallback if it was stored in financial_details before
                            market_exp_load = decrypted_details_load.get('market_linked_experience')

                        st.session_state.current_investor_id = investor_id_to_load
                        st.session_state.current_profile_creator_step = 0
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
                        
                        family_data_json_load = investor_db_data_load.get('dependents')
                        loaded_family_data = {'marital_status': "Single", 'num_dependents': 0, 'dependents_details': []}
                        if family_data_json_load:
                            try:
                                parsed_family_data = json.loads(family_data_json_load)
                                loaded_family_data['marital_status'] = parsed_family_data.get('marital_status', "Single")
                                loaded_family_data['num_dependents'] = parsed_family_data.get('num_dependents', 0)
                                loaded_details = parsed_family_data.get('dependents_details', [])
                                num_deps_parsed = loaded_family_data['num_dependents']
                                valid_details = []
                                for i in range(num_deps_parsed):
                                    if i < len(loaded_details) and isinstance(loaded_details[i], dict):
                                        valid_details.append(loaded_details[i])
                                    else:
                                        valid_details.append({'age': None, 'gender': 'Male'})
                                loaded_family_data['dependents_details'] = valid_details
                            except json.JSONDecodeError:
                                pass 
                        st.session_state.form_data_family = loaded_family_data
                        
                        st.session_state.form_data_finance = { 
                            "individual_income": decrypted_details_load.get('individual_income'),
                            "spouse_income": decrypted_details_load.get('spouse_income'),
                            "monthly_household_expenses": decrypted_details_load.get('monthly_household_expenses'),
                            "current_emergency_fund": decrypted_details_load.get('current_emergency_fund'),
                            "loan_emis": decrypted_details_load.get('loan_emis'),
                            "owns_home": decrypted_details_load.get('owns_home'),
                            "rent_amount": decrypted_details_load.get('rent_amount')
                        }
                        st.session_state.form_data_risk_questions = {
                            "answers": risk_answers_list_load,
                            "market_linked_experience": market_exp_load
                        }
                        st.session_state.active_tab_label = main_tabs_config["create_profile"]["label"]
                        st.rerun()
        else: st.info("No investors found.")
    with mfd_tab2: st.subheader("Aggregated Insights"); st.write("(Placeholder)")
    with mfd_tab3: st.subheader("Print Investor Plans"); st.write("(Placeholder)")
    with mfd_tab4: st.subheader("MFD Guide Access"); st.write("(Placeholder)")

def economic_overview_tab_content(conn):
    st.header("📈 Economic Overview")
    if st.button("Refresh Economic Data"): fetch_and_store_economic_data(conn); st.rerun()
    latest_data, is_fallback = get_latest_economic_data_from_db(conn)
    if is_fallback: st.warning("Displaying fallback economic data.")
    gdp = latest_data.get("gdp_growth", {}); cpi = latest_data.get("cpi_inflation", {})
    st.metric(label=f"GDP Growth ({gdp.get('indicator', '')} - {gdp.get('year', 'N/A')})", value=f"{gdp.get('value', 'N/A')}")
    st.metric(label=f"CPI Inflation ({cpi.get('indicator', '')} - {cpi.get('year', 'N/A')})", value=f"{cpi.get('value', 'N/A')}")

main_tabs_config = {}
def main_app_logic():
    conn = init_db()
    if 'latest_economic_data' not in st.session_state: st.session_state.latest_economic_data, _ = get_latest_economic_data_from_db(conn)
    st.sidebar.title("Navigation")
    global main_tabs_config 
    main_tabs_ordered_keys = ["create_profile", "investor_dashboard", "mfd_dashboard", "financial_goals", "risk_profile", "investor_guide", "economic_overview"]
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
    st.session_state.active_tab_label = st.sidebar.radio("Go to:", options=ordered_radio_labels, key="sidebar_nav", label_visibility="collapsed", index=ordered_radio_labels.index(st.session_state.active_tab_label))
    active_tab_key = next((key for key, config_label in sidebar_tab_labels.items() if config_label == st.session_state.active_tab_label), None)
    if active_tab_key: main_tabs_config[active_tab_key]["func"](conn)
    else: st.error("Selected tab not found.")

if __name__ == "__main__":
    main_app_logic()

