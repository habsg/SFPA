# risk_assessment_logic.py

from datetime import datetime, date
import json

# Assuming profiling_logic.calculate_age can be imported or is available
# For now, let's redefine it here if it's simple enough or assume it's passed.

def calculate_age(dob_str: str, reference_date_str: str = None) -> int:
    """
    Calculates age based on date of birth string and an optional reference date string.
    Args:
        dob_str: Date of birth as "YYYY-MM-DD".
        reference_date_str: Reference date as "YYYY-MM-DD". Defaults to today if None.
    Returns:
        Age in years.
    """
    try:
        dob = date.fromisoformat(dob_str)
    except (ValueError, TypeError):
        raise ValueError("Invalid Date of Birth format or value. Expected YYYY-MM-DD.")

    if reference_date_str:
        try:
            reference_date = date.fromisoformat(reference_date_str)
        except (ValueError, TypeError):
            raise ValueError("Invalid Reference Date format or value. Expected YYYY-MM-DD.")
    else:
        reference_date = date.today()
    
    if dob > reference_date:
        raise ValueError("Date of Birth cannot be in the future relative to the reference date.")

    age = reference_date.year - dob.year - ((reference_date.month, reference_date.day) < (dob.month, dob.day))
    return age

def calculate_required_emergency_fund(
    total_household_monthly_income: float,
    occupation: str,
    monthly_rent: float,
    monthly_emi: float,
    # Framework implies essential expenses. Using a simplified proxy for now.
    # A more detailed approach would be: total_household_monthly_income - (rent + emi + other_essential_non_discretionary_expenses)
    # For now, let's use a percentage of income as proxy for essential expenses if rent/emi are not comprehensive.
    # The framework (Part 1, Sec 10) mentions 3-6 months of expenses.
    # The app.py used: total_income - (total_income * 0.2) as monthly_expenses proxy.
    # Let's use a simple proxy: (total_household_monthly_income - monthly_rent - monthly_emi) if this is positive, else a fraction of income.
    # Or, more directly, the framework says X months of *expenses*. If we assume savings rate of Y%, then expenses are (1-Y%) * income.
    # Let's use a simple proxy for monthly expenses: 70% of total household income, or income - rent - emi if that's lower and positive.
    # Framework (Part 1, Sec 10) suggests 3 months for White-Collar, 6 months for Blue-Collar.
) -> float:
    """
    Calculates the required emergency fund based on framework guidelines (simplified).
    """
    if total_household_monthly_income <= 0:
        return 0.0

    # Simplified monthly expenses proxy
    # Option 1: Fixed percentage (e.g., 70% of income)
    # monthly_expenses_proxy = total_household_monthly_income * 0.70
    # Option 2: Income net of major fixed costs, if substantial
    net_income_after_housing = total_household_monthly_income - monthly_rent - monthly_emi
    if net_income_after_housing > (total_household_monthly_income * 0.20): # Ensure it's a reasonable amount for expenses
        monthly_expenses_proxy = net_income_after_housing * 0.8 # Assuming 80% of this remainder is essential
    else:
        monthly_expenses_proxy = total_household_monthly_income * 0.60 # Fallback to 60% of gross as essential
    
    if monthly_expenses_proxy < 0: monthly_expenses_proxy = 0

    required_months = 0
    if occupation == "Blue-Collar":
        required_months = 6
    elif occupation == "White-Collar":
        required_months = 3
    else: # Default or unknown
        required_months = 4 # Average
        
    return required_months * monthly_expenses_proxy

def calculate_risk_score(
    dob_str: str, # YYYY-MM-DD
    occupation: str, # White-Collar, Blue-Collar
    total_household_monthly_income: float,
    num_dependents: int,
    current_emergency_fund: float,
    monthly_rent: float,
    monthly_emi: float,
    market_linked_experience: str, # "Yes", "No"
    risk_questionnaire_answers: list, # List of answers to risk questions
    plan_in_action_date_str: str = None # YYYY-MM-DD, for age calculation at plan start
) -> tuple[int, dict]:
    """
    Calculates a comprehensive risk score (0-100) based on multiple factors.
    Returns a tuple: (total_score, details_of_scores_by_factor)
    """
    score = 0
    score_details = {}
    current_date_str = datetime.now().strftime("%Y-%m-%d")
    effective_date_for_age = plan_in_action_date_str if plan_in_action_date_str else current_date_str

    try:
        age = calculate_age(dob_str, effective_date_for_age)
    except ValueError:
        # Handle error, e.g., by assigning a neutral score for age factor or raising exception
        age = 35 # Default age if DOB is problematic, for calculation to proceed

    # 1. Stated Risk Preferences (Max 30 points) - Based on app.py logic
    # Answers: [q1_greed, q2_preference, q3_willingness, q4_reaction, q5_anxiety]
    # Each mapped 1-5. Total raw score 5-25.
    raw_stated_score = 0
    if len(risk_questionnaire_answers) == 5:
        greed_map = {"Not likely at all": 1, "Somewhat unlikely": 2, "Neutral": 3, "Somewhat likely": 4, "Very likely": 5}
        preference_map = {"Definitely Fixed Deposit": 1, "Lean towards Fixed Deposit": 2, "Neutral": 3, "Lean towards equity fund": 4, "Definitely equity fund": 5}
        willingness_map = {"Not willing at all": 1, "Somewhat reluctant": 2, "Neutral": 3, "Somewhat willing": 4, "Very willing": 5}
        reaction_map = {"Sell all investments immediately": 1, "Sell some investments and wait": 2, "Hold and wait for recovery": 3, "Hold and monitor closely": 4, "Invest more during the dip": 5}
        anxiety_map = {"Extremely anxious, unable to sleep": 1, "Quite anxious, very concerned": 2, "Mildly anxious, somewhat concerned": 3, "Not very anxious, can manage": 4, "Not anxious at all, comfortable": 5}
        
        raw_stated_score += greed_map.get(risk_questionnaire_answers[0], 1)
        raw_stated_score += preference_map.get(risk_questionnaire_answers[1], 1)
        raw_stated_score += willingness_map.get(risk_questionnaire_answers[2], 1)
        raw_stated_score += reaction_map.get(risk_questionnaire_answers[3], 1)
        raw_stated_score += anxiety_map.get(risk_questionnaire_answers[4], 1)
        
        stated_risk_points = ((raw_stated_score - 5) / 20) * 30 # Scale 0-20 to 0-30
    else:
        stated_risk_points = 15 # Neutral if answers are missing
    score += stated_risk_points
    score_details["stated_risk_preferences"] = round(stated_risk_points, 2)

    # 2. Emergency Fund Adequacy (Max 20 points)
    required_fund = calculate_required_emergency_fund(total_household_monthly_income, occupation, monthly_rent, monthly_emi)
    emergency_points = 0
    if required_fund > 0:
        adequacy_ratio = current_emergency_fund / required_fund
        if adequacy_ratio < 0.25: emergency_points = 2
        elif adequacy_ratio < 0.50: emergency_points = 5
        elif adequacy_ratio < 0.75: emergency_points = 9
        elif adequacy_ratio < 1.00: emergency_points = 13
        elif adequacy_ratio < 1.50: emergency_points = 17
        else: emergency_points = 20
    else: # No income or no required fund means cannot assess, or max points if no fund needed
        emergency_points = 10 if total_household_monthly_income > 0 else 20 # Neutral or Max if no income
    score += emergency_points
    score_details["emergency_fund_adequacy"] = round(emergency_points, 2)
    score_details["calculated_required_emergency_fund"] = round(required_fund, 2)

    # 3. Debt Burden (e.g., LTI or DTI proxy) (Max 15 points)
    # Using monthly Debt Servicing Ratio (DSR) as proxy: (Rent + EMI) / Total Household Monthly Income
    debt_points = 0
    if total_household_monthly_income > 0:
        dsr = (monthly_rent + monthly_emi) / total_household_monthly_income
        if dsr <= 0.10: debt_points = 15 # Very low debt
        elif dsr <= 0.20: debt_points = 12
        elif dsr <= 0.30: debt_points = 9
        elif dsr <= 0.40: debt_points = 6
        elif dsr <= 0.50: debt_points = 3
        else: debt_points = 0 # Very high debt
    else:
        debt_points = 15 # No income, no debt assessment possible, assume high capacity if no EMIs either
        if monthly_emi > 0 : debt_points = 0 # No income but EMIs is worst case
    score += debt_points
    score_details["debt_burden"] = round(debt_points, 2)

    # 4. Life Cycle Stage (Max 15 points)
    lifecycle_points = 0
    # Based on framework's life cycle stages (approximated from app.py logic)
    if 22 <= age <= 30: lifecycle_points = 15    # Young Adult
    elif 31 <= age <= 40: lifecycle_points = 12  # Young Family / Early Mid-Career (approximated)
    elif 41 <= age <= 50: lifecycle_points = 9   # Mid-Career Family
    elif 51 <= age <= 60: lifecycle_points = 6   # Pre-Retirement
    else: lifecycle_points = 3                   # Retirement or very young
    score += lifecycle_points
    score_details["life_cycle_stage"] = round(lifecycle_points, 2)
    score_details["calculated_age"] = age

    # 5. Income Level and Stability (Max 10 points)
    income_points = 0
    # Simplified: Higher income, more points. White-collar more stable.
    if total_household_monthly_income >= 100000: income_points = 8
    elif total_household_monthly_income >= 50000: income_points = 6
    elif total_household_monthly_income >= 25000: income_points = 4
    else: income_points = 2
    if occupation == "White-Collar": income_points += 2
    else: income_points += 0 # Blue-collar base points already set by income level
    score += income_points
    score_details["income_stability"] = round(income_points, 2)

    # 6. Number of Dependents (Max 5 points)
    dependents_points = 0
    if num_dependents == 0: dependents_points = 5
    elif num_dependents == 1: dependents_points = 4
    elif num_dependents == 2: dependents_points = 2
    else: dependents_points = 0 # 3 or more
    score += dependents_points
    score_details["num_dependents_factor"] = round(dependents_points, 2)

    # 7. Market-Linked Investment Experience (Max 5 points)
    market_exp_points = 5 if market_linked_experience == "Yes" else 1
    score += market_exp_points
    score_details["market_experience"] = round(market_exp_points, 2)
    
    final_score = max(0, min(100, int(round(score)))) # Ensure score is between 0 and 100
    return final_score, score_details

def get_risk_rating(score: int) -> str:
    """Determines Risk Rating based on score (0-100)."""
    if score <= 20: return "Very Low (Highly Conservative)"
    elif score <= 40: return "Low (Conservative)"
    elif score <= 60: return "Moderate (Balanced)"
    elif score <= 80: return "High (Growth-Oriented)"
    else: return "Very High (Aggressive)"

if __name__ == "__main__":
    print("--- Test Cases for Risk Assessment ---")
    sample_answers = [
        "Neutral", # Greed
        "Neutral", # Preference
        "Neutral", # Willingness
        "Hold and wait for recovery", # Reaction
        "Mildly anxious, somewhat concerned" # Anxiety
    ] # Raw score = 3+3+3+3+3 = 15. Stated points = ((15-5)/20)*30 = 15

    # Test Case 1: Young, good income, white-collar, no dependents, good emergency fund, low debt, experience
    score1, details1 = calculate_risk_score(
        dob_str="1995-01-01", # Age 30 (approx, depending on current date)
        occupation="White-Collar",
        total_household_monthly_income=120000,
        num_dependents=0,
        current_emergency_fund=500000, # Required for 120k income, WC (3mo) = 3 * (120k*0.6) = 216k. Ratio > 1.5 -> 20pts
        monthly_rent=20000,
        monthly_emi=5000, # DSR = 25k/120k = 0.208 -> 9 pts
        market_linked_experience="Yes", # 5 pts
        risk_questionnaire_answers=sample_answers # 15 pts
        # Age 30 -> 15 pts (Lifecycle)
        # Income 120k, WC -> 8+2 = 10 pts (Income Stability)
        # Dependents 0 -> 5 pts
        # Total = 15(stated) + 20(emergency) + 9(debt) + 15(lifecycle) + 10(income) + 5(deps) + 5(exp) = 79
    )
    rating1 = get_risk_rating(score1)
    print(f"Test 1 Score: {score1}, Rating: {rating1}")
    print(f"Details 1: {json.dumps(details1, indent=2)}")
    # Expected around 79 (High)

    # Test Case 2: Older, lower income, blue-collar, many dependents, low emergency fund, high debt, no experience
    score2, details2 = calculate_risk_score(
        dob_str="1970-01-01", # Age 55 (approx)
        occupation="Blue-Collar",
        total_household_monthly_income=25000,
        num_dependents=3,
        current_emergency_fund=10000, # Required for 25k income, BC (6mo) = 6 * (25k*0.6) = 90k. Ratio <0.25 -> 2pts
        monthly_rent=5000,
        monthly_emi=8000, # DSR = 13k/25k = 0.52 -> 0 pts
        market_linked_experience="No", # 1 pt
        risk_questionnaire_answers=["Not likely at all", "Definitely Fixed Deposit", "Not willing at all", "Sell all investments immediately", "Extremely anxious, unable to sleep"]
        # Raw stated = 1+1+1+1+1 = 5. Stated points = ((5-5)/20)*30 = 0 pts
        # Age 55 -> 6 pts (Lifecycle)
        # Income 25k, BC -> 4+0 = 4 pts (Income Stability)
        # Dependents 3 -> 0 pts
        # Total = 0(stated) + 2(emergency) + 0(debt) + 6(lifecycle) + 4(income) + 0(deps) + 1(exp) = 13
    )
    rating2 = get_risk_rating(score2)
    print(f"Test 2 Score: {score2}, Rating: {rating2}")
    print(f"Details 2: {json.dumps(details2, indent=2)}")
    # Expected around 13 (Very Low)

    # Test Case 3: Edge case, no income
    score3, details3 = calculate_risk_score(
        dob_str="1980-01-01",
        occupation="White-Collar",
        total_household_monthly_income=0,
        num_dependents=1,
        current_emergency_fund=50000,
        monthly_rent=0,
        monthly_emi=0,
        market_linked_experience="No",
        risk_questionnaire_answers=sample_answers
        # Stated: 15
        # Emergency: Required 0 -> 20 pts (as per current logic for 0 income)
        # Debt: DSR undefined (income 0) -> 15 pts (no EMIs)
        # Lifecycle (Age 45 approx): 9 pts
        # Income (0, WC): 2+2 = 4 pts
        # Dependents (1): 4 pts
        # Experience (No): 1 pt
        # Total = 15 + 20 + 15 + 9 + 4 + 4 + 1 = 68
    )
    rating3 = get_risk_rating(score3)
    print(f"Test 3 Score (No Income): {score3}, Rating: {rating3}")
    print(f"Details 3: {json.dumps(details3, indent=2)}")
    # Expected around 68 (High) - This might need refinement for 0 income cases.
    # The high score for 0 income is due to maxing out emergency fund and debt burden factors by current logic.
    # This should be reviewed; perhaps 0 income should lead to a very low capacity score unless substantial assets.

    # Test Case 4: Missing risk answers
    score4, details4 = calculate_risk_score(
        dob_str="1990-01-01", occupation="Blue-Collar",
        total_household_monthly_income=40000, num_dependents=1,
        current_emergency_fund=100000, monthly_rent=8000, monthly_emi=2000,
        market_linked_experience="Yes", risk_questionnaire_answers=[] # Missing answers
        # Stated: 15 (neutral)
    )
    rating4 = get_risk_rating(score4)
    print(f"Test 4 Score (Missing Answers): {score4}, Rating: {rating4}")
    print(f"Details 4: {json.dumps(details4, indent=2)}")


