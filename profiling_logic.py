# profiling_logic.py

from datetime import datetime, date

# --- Profile Definitions (from Framework Part 1, Section 3) ---
# Each entry: (ProfileID, LifeCycleStage, AgeMin, AgeMax, IncomeLevel, IncomeMin, IncomeMax, DependentsMin, DependentsMax, Description)
# IncomeMax = float("inf") for ">X" ranges. DependentsMax can also be float("inf").

WHITE_COLLAR_PROFILES = [
    ("W1", "Young Adult", 22, 30, "Low", 0, 30000, 0, 1, "Limited savings; starting career, possible debt."),
    ("W2", "Young Adult", 22, 30, "Sufficient", 30001, 60000, 0, 1, "Moderate savings; building emergency fund."),
    ("W3", "Young Adult", 22, 30, "Good", 60001, float("inf"), 0, 1, "High savings; early retirement planning."),
    ("W4", "Young Family", 28, 35, "Low", 0, 45000, 1, 2, "Tight budget; focus on emergency fund, education."),
    ("W5", "Young Family", 28, 35, "Sufficient", 45001, 90000, 1, 2, "Balanced savings; home purchase, education goals."),
    ("W6", "Young Family", 28, 35, "Good", 90001, float("inf"), 1, 2, "Strong savings; aggressive education, retirement."),
    ("W7", "Mid-Career Family", 35, 50, "Low", 0, 67500, 2, 3, "High expenses; education, marriage, debt challenges."),
    ("W8", "Mid-Career Family", 35, 50, "Sufficient", 67501, 135000, 2, 3, "Stable savings; education, marriage, retirement focus."),
    ("W9", "Mid-Career Family", 35, 50, "Good", 135001, float("inf"), 2, 3, "High savings; multiple goals, early retirement."),
    ("W10", "Pre-Retirement", 50, 60, "Low", 0, 101250, 0, 2, "Limited savings; urgent retirement planning."),
    ("W11", "Pre-Retirement", 50, 60, "Sufficient", 101251, 202500, 0, 2, "Moderate savings; retirement, marriage goals."),
    ("W12", "Pre-Retirement", 50, 60, "Good", 202501, float("inf"), 0, 2, "Strong savings; robust retirement planning."),
    ("W13", "Retirement", 60, float("inf"), "Low", 0, 101250, 0, 1, "Reliant on savings/pension; preservation focus."),
    ("W14", "Retirement", 60, float("inf"), "Sufficient", 101251, 202500, 0, 1, "Stable income; balanced retirement spending."),
    ("W15", "Retirement", 60, float("inf"), "Good", 202501, float("inf"), 0, 1, "High savings; comfortable retirement lifestyle.")
]

BLUE_COLLAR_PROFILES = [
    ("B1", "Young Adult", 22, 30, "Low", 0, 12000, 0, 1, "Minimal savings; high debt risk."),
    ("B2", "Young Adult", 22, 30, "Sufficient", 12001, 20000, 0, 1, "Limited savings; emergency fund, small retirement."),
    ("B3", "Young Adult", 22, 30, "Good", 20001, float("inf"), 0, 1, "Moderate savings; home purchase, retirement plans."),
    ("B4", "Young Family", 28, 35, "Low", 0, 18000, 1, 2, "Tight budget; debt reduction, emergency fund focus."),
    ("B5", "Young Family", 28, 35, "Sufficient", 18001, 30000, 1, 2, "Modest savings; education, home purchase goals."),
    ("B6", "Young Family", 28, 35, "Good", 30001, float("inf"), 1, 2, "Decent savings; education, home, retirement planning."),
    ("B7", "Mid-Career Family", 35, 50, "Low", 0, 27000, 2, 3, "High debt risk; education, marriage focus."),
    ("B8", "Mid-Career Family", 35, 50, "Sufficient", 27001, 45000, 2, 3, "Balanced savings; education, marriage, retirement."),
    ("B9", "Mid-Career Family", 35, 50, "Good", 45001, float("inf"), 2, 3, "Strong savings; multiple goals."),
    ("B10", "Pre-Retirement", 50, 60, "Low", 0, 40500, 0, 2, "Minimal savings; urgent retirement, debt challenges."),
    ("B11", "Pre-Retirement", 50, 60, "Sufficient", 40501, 67500, 0, 2, "Modest savings; retirement, marriage goals."),
    ("B12", "Pre-Retirement", 50, 60, "Good", 67501, float("inf"), 0, 2, "Decent savings; comfortable retirement planning."),
    ("B13", "Retirement", 60, float("inf"), "Low", 0, 40500, 0, 1, "Limited savings; preservation focus."),
    ("B14", "Retirement", 60, float("inf"), "Sufficient", 40501, 67500, 0, 1, "Stable savings; modest retirement lifestyle."),
    ("B15", "Retirement", 60, float("inf"), "Good", 67501, float("inf"), 0, 1, "High savings; secure retirement lifestyle.")
]

# --- Helper Functions ---
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
        # Handle invalid DOB format or None
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

# --- Main Profiling Function ---
def assign_investor_profile(occupation: str, dob_str: str, individual_monthly_income: float, num_dependents: int, plan_in_action_date_str: str = None) -> str | None:
    """
    Assigns an investor profile based on their details as per the framework.
    Args:
        occupation: "White-Collar" or "Blue-Collar".
        dob_str: Date of birth as "YYYY-MM-DD".
        individual_monthly_income: Investor"s individual monthly income.
        num_dependents: Number of dependents.
        plan_in_action_date_str: Plan in action date as "YYYY-MM-DD". If provided, age is calculated based on this date for profile lock.
                                 Otherwise, current date is used.
    Returns:
        The Profile ID (e.g., "W1", "B8") or None if no profile matches.
    """
    try:
        age = calculate_age(dob_str, plan_in_action_date_str)
    except ValueError as e:
        print(f"Error calculating age: {e}") # Or handle more gracefully
        return None

    if not isinstance(individual_monthly_income, (int, float)) or individual_monthly_income < 0:
        print("Invalid individual monthly income.")
        return None
    if not isinstance(num_dependents, int) or num_dependents < 0:
        print("Invalid number of dependents.")
        return None

    profiles_to_check = []
    if occupation == "White-Collar":
        profiles_to_check = WHITE_COLLAR_PROFILES
    elif occupation == "Blue-Collar":
        profiles_to_check = BLUE_COLLAR_PROFILES
    else:
        print(f"Invalid occupation: {occupation}")
        return None

    for profile in profiles_to_check:
        profile_id, _, age_min, age_max, _, income_min, income_max, dep_min, dep_max, _ = profile
        
        # Check age: profile age_max can be float("inf")
        if not (age_min <= age <= (age_max if age_max != float("inf") else float("inf"))):
            continue
            
        # Check income: profile income_max can be float("inf")
        if not (income_min <= individual_monthly_income <= (income_max if income_max != float("inf") else float("inf"))):
            continue
            
        # Check dependents: profile dep_max can be float("inf")
        if not (dep_min <= num_dependents <= (dep_max if dep_max != float("inf") else float("inf"))):
            continue
            
        return profile_id # Found a matching profile
        
    return None # No profile matched

if __name__ == "__main__":
    # Test cases
    print("--- Test Cases for Investor Profiling ---")
    # Test 1: White-Collar, Young Adult, Sufficient Income
    profile = assign_investor_profile("White-Collar", "1995-06-15", 50000, 0, "2025-05-14") # Age 29
    print(f"Test 1 (W, 29yo, 50k, 0 dep): Expected W2, Got: {profile}")

    # Test 2: Blue-Collar, Mid-Career Family, Sufficient Income
    profile = assign_investor_profile("Blue-Collar", "1980-01-10", 35000, 2, "2025-05-14") # Age 45
    print(f"Test 2 (B, 45yo, 35k, 2 dep): Expected B8, Got: {profile}")

    # Test 3: White-Collar, Young Family, Good Income (Age 30, 1 dependent)
    profile = assign_investor_profile("White-Collar", "1995-05-01", 100000, 1, "2025-05-14") # Age 30
    print(f"Test 3 (W, 30yo, 100k, 1 dep): Expected W6, Got: {profile}") 
    # W3: Age 22-30, Income >60k, Dep 0-1. (Matches age, income, dep)
    # W6: Age 28-35, Income >90k, Dep 1-2. (Matches age, income, dep)
    # Order matters. W3 is checked before W6. For age 30, 1 dep, 100k income: W3 matches. This is correct as per table structure.

    # Test 4: White-Collar, Age 30, 100k income, 2 dependents (should be W6)
    profile = assign_investor_profile("White-Collar", "1995-05-01", 100000, 2, "2025-05-14") # Age 30
    print(f"Test 4 (W, 30yo, 100k, 2 dep): Expected W6, Got: {profile}")

    # Test 5: Retirement profile
    profile = assign_investor_profile("Blue-Collar", "1960-01-01", 70000, 0, "2025-05-14") # Age 65
    print(f"Test 5 (B, 65yo, 70k, 0 dep): Expected B15, Got: {profile}")

    # Test 6: No match (e.g., too young)
    profile = assign_investor_profile("White-Collar", "2010-01-01", 50000, 0, "2025-05-14") # Age 15
    print(f"Test 6 (W, 15yo, 50k, 0 dep): Expected None, Got: {profile}")

    # Test 7: Invalid occupation
    profile = assign_investor_profile("Farmer", "1980-01-01", 50000, 0, "2025-05-14")
    print(f"Test 7 (Invalid Occupation): Expected None, Got: {profile}")

    # Test 8: White-Collar, Age 29, Income 50000, 1 dependent (should be W2)
    # DOB: 1996-05-01, RefDate: 2025-05-14 -> Age 29
    profile = assign_investor_profile("White-Collar", "1996-05-01", 50000, 1, "2025-05-14")
    print(f"Test 8 (W, 29yo, 50k, 1 dep): Expected W2, Got: {profile}")

    # Test 9: White-Collar, Age 29, Income 70000, 1 dependent (should be W3)
    profile = assign_investor_profile("White-Collar", "1996-05-01", 70000, 1, "2025-05-14")
    print(f"Test 9 (W, 29yo, 70k, 1 dep): Expected W3, Got: {profile}")

    # Test 10: White-Collar, Age 29, Income 70000, 2 dependents (should be W6)
    # W3: dep 0-1 (no match) -> W6: age 28-35, income >90k (no match for 70k) -> W5: income 45k-90k, dep 1-2 (match!)
    # Let's re-evaluate W6 income: >90k. So for 70k, it's W5.
    profile = assign_investor_profile("White-Collar", "1996-05-01", 70000, 2, "2025-05-14")
    print(f"Test 10 (W, 29yo, 70k, 2 dep): Expected W5, Got: {profile}")

    # Test 11: DOB in future
    try:
        profile = assign_investor_profile("White-Collar", "2030-01-01", 50000, 0, "2025-05-14")
        print(f"Test 11 (Future DOB): Expected Error, Got: {profile}")
    except ValueError as e:
        print(f"Test 11 (Future DOB): Expected Error, Got Error: {e}")

    # Test 12: Invalid DOB format
    try:
        profile = assign_investor_profile("White-Collar", "15-06-1995", 50000, 0, "2025-05-14")
        print(f"Test 12 (Invalid DOB format): Expected Error, Got: {profile}")
    except ValueError as e:
        print(f"Test 12 (Invalid DOB format): Expected Error, Got Error: {e}")


