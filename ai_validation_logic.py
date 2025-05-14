# ai_validation_logic.py

import re
from datetime import datetime

PROFILES_DATA_EXAMPLE = {
    "W1": {"min_income": 0, "max_income": 30000, "typical_income": 20000, "occupation_type": "White-Collar"},
    "B1": {"min_income": 0, "max_income": 12000, "typical_income": 8000, "occupation_type": "Blue-Collar"},
    "W8": {"min_income": 67501, "max_income": 135000, "typical_income": 100000, "occupation_type": "White-Collar"},
    "B8": {"min_income": 27001, "max_income": 45000, "typical_income": 35000, "occupation_type": "Blue-Collar"}
}

def validate_mobile_number(mobile: str) -> tuple[bool, str]:
    """Validates Indian mobile number format."""
    if not mobile:
        return False, "Mobile number cannot be empty."
    pattern = r"^[6-9][0-9]{9}$"
    if re.match(pattern, mobile):
        return True, "Valid mobile number."
    return False, "Invalid mobile number format. Should be 10 digits starting with 6, 7, 8, or 9."

def validate_email(email: str) -> tuple[bool, str]:
    """Validates basic email format."""
    if not email:
        return True, "Email is optional."
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, email):
        return True, "Valid email address."
    return False, "Invalid email address format."

def validate_dob(dob_str: str) -> tuple[bool, str]:
    """Validates DOB format and ensures it's not in the future."""
    try:
        dob_date = datetime.strptime(dob_str, "%Y-%m-%d").date()
        if dob_date > datetime.now().date():
            return False, "Date of Birth cannot be in the future."
        min_age_for_planning = 18
        age = datetime.now().year - dob_date.year - ((datetime.now().month, datetime.now().day) < (dob_date.month, dob_date.day))
        if age < min_age_for_planning:
            return False, f"Investor must be at least {min_age_for_planning} years old."
        return True, "Valid Date of Birth."
    except ValueError:
        return False, "Invalid Date of Birth format. Expected YYYY-MM-DD."

def validate_income_against_profile(
    income: float,
    occupation: str,
    profile_id: str = None,
    all_profiles_data = PROFILES_DATA_EXAMPLE
) -> tuple[bool, str]:
    """Validates if the income is broadly consistent with the occupation or a specific profile."""
    if income < 0:
        return False, "Income cannot be negative."
    
    suggestions = []
    is_consistent = True

    if occupation == "Blue-Collar" and income > 70000:
        suggestions.append(f"Income {income:,.0f} seems high for a Blue-Collar profile. Please verify.")
        is_consistent = False
    elif occupation == "White-Collar" and income < 15000 and income > 0:
        suggestions.append(f"Income {income:,.0f} seems low for a White-Collar profile. Please verify.")
        is_consistent = False

    if profile_id and profile_id in all_profiles_data:
        profile_info = all_profiles_data[profile_id]
        min_prof_income = profile_info["min_income"]
        max_prof_income = profile_info["max_income"]
        typical_prof_income = profile_info.get("typical_income", (min_prof_income + max_prof_income * 0.5) if max_prof_income != float("inf") else min_prof_income * 2)

        if not (min_prof_income <= income <= max_prof_income):
            suggestions.append(f"Income {income:,.0f} is outside the typical range ({min_prof_income:,.0f}-{max_prof_income:,.0f}) for profile {profile_id}. Consider typical income around {typical_prof_income:,.0f}. Please verify.")
            is_consistent = False
    
    if not suggestions:
        return True, "Income appears consistent with the provided details."
    
    return is_consistent, " ".join(suggestions)

def validate_income_with_economic_context(
    income: float,
    occupation: str,
    economic_indicators: dict = None
) -> tuple[bool, str]:
    """Provides suggestions if income seems unusually high/low given economic context."""
    if economic_indicators is None:
        return True, "Economic context not available for income validation."

    gdp_growth = economic_indicators.get("gdp_growth_rate")
    suggestions = []
    is_consistent = True

    if gdp_growth is not None and gdp_growth < 4.0:
        if occupation == "Blue-Collar" and income > 50000:
            suggestions.append(f"Given current economic slowdown (GDP growth: {gdp_growth}%), income {income:,.0f} for Blue-Collar profile is notably high. Please double-check.")
            is_consistent = False
        elif occupation == "White-Collar" and income > 200000:
             suggestions.append(f"Given current economic slowdown (GDP growth: {gdp_growth}%), income {income:,.0f} for White-Collar profile is notably high. Please double-check.")
             is_consistent = False
    
    if not suggestions:
        return True, "Income seems plausible within the current economic context."
    
    return is_consistent, " ".join(suggestions)

def run_all_validations(investor_data: dict, economic_indicators: dict = None, profile_id: str = None, all_profiles_master_data=None) -> dict:
    """Runs all validation checks and returns a dictionary of results."""
    validation_summary = {
        "overall_valid": True,
        "issues": [],
        "suggestions_log": []
    }

    valid_mobile, msg_mobile = validate_mobile_number(investor_data.get("mobile_number", ""))
    if not valid_mobile:
        validation_summary["overall_valid"] = False
        validation_summary["issues"].append({"field": "mobile_number", "message": msg_mobile})
    validation_summary["suggestions_log"].append({"field": "mobile_number", "check": "format", "status": "valid" if valid_mobile else "invalid", "message": msg_mobile})

    valid_email, msg_email = validate_email(investor_data.get("email", ""))
    if not valid_email:
        validation_summary["issues"].append({"field": "email", "message": msg_email})
    validation_summary["suggestions_log"].append({"field": "email", "check": "format", "status": "valid" if valid_email else "invalid", "message": msg_email})

    valid_dob, msg_dob = validate_dob(investor_data.get("dob", ""))
    if not valid_dob:
        validation_summary["overall_valid"] = False
        validation_summary["issues"].append({"field": "dob", "message": msg_dob})
    validation_summary["suggestions_log"].append({"field": "dob", "check": "validity", "status": "valid" if valid_dob else "invalid", "message": msg_dob})

    current_profiles_data_source = all_profiles_master_data if all_profiles_master_data else PROFILES_DATA_EXAMPLE
    
    consistent_income_profile, msg_income_profile = validate_income_against_profile(
        investor_data.get("individual_monthly_income", 0.0),
        investor_data.get("occupation", ""),
        profile_id=profile_id,
        all_profiles_data=current_profiles_data_source
    )
    if not consistent_income_profile:
        validation_summary["issues"].append({"field": "individual_monthly_income", "message": msg_income_profile, "type": "consistency_warning"})
    validation_summary["suggestions_log"].append({"field": "individual_monthly_income", "check": "profile_consistency", "status": "consistent" if consistent_income_profile else "warning", "message": msg_income_profile})

    # Check if economic_indicators is not None and, if it's a pandas Series/DataFrame, that it's not empty
    if economic_indicators is not None and not getattr(economic_indicators, "empty", True):
        consistent_income_econ, msg_income_econ = validate_income_with_economic_context(
            investor_data.get("individual_monthly_income", 0.0),
            investor_data.get("occupation", ""),
            economic_indicators
        )
        if not consistent_income_econ:
            validation_summary["issues"].append({"field": "individual_monthly_income", "message": msg_income_econ, "type": "context_warning"})
        validation_summary["suggestions_log"].append({"field": "individual_monthly_income", "check": "economic_context", "status": "plausible" if consistent_income_econ else "warning", "message": msg_income_econ})
        
    return validation_summary

if __name__ == "__main__":
    print("--- Test AI Validation Logic ---")
    sample_investor_valid = {
        "mobile_number": "9876543210",
        "email": "test@example.com",
        "dob": "1990-01-01",
        "individual_monthly_income": 100000,
        "occupation": "White-Collar"
    }
    
    mock_econ_normal = {"gdp_growth_rate": 5.0}
    mock_econ_slowdown = {"gdp_growth_rate": 3.5}

    print("\nTest 1: Valid data, normal economy, profile W8")
    results_valid = run_all_validations(sample_investor_valid, mock_econ_normal, profile_id="W8")
    print(f"Overall Valid: {results_valid['overall_valid']}")
    print(f"Issues: {results_valid['issues']}")

    sample_investor_invalid_income = {
        "mobile_number": "9876543210",
        "email": "test@example.com",
        "dob": "1980-01-01",
        "individual_monthly_income": 10000,
        "occupation": "White-Collar"
    }
    print("\nTest 2: Invalid income for profile W8")
    results_invalid_income = run_all_validations(sample_investor_invalid_income, mock_econ_normal, profile_id="W8")
    print(f"Overall Valid: {results_invalid_income['overall_valid']}")
    print(f"Issues: {results_invalid_income['issues']}")

    sample_investor_high_income_slowdown_bc = {
        "mobile_number": "9876543210",
        "email": "test@example.com",
        "dob": "1985-01-01",
        "individual_monthly_income": 60000,
        "occupation": "Blue-Collar"
    }
    print("\nTest 3: High income for Blue-Collar during slowdown, profile B8")
    results_high_bc = run_all_validations(sample_investor_high_income_slowdown_bc, mock_econ_slowdown, profile_id="B8")
    print(f"Overall Valid: {results_high_bc['overall_valid']}")
    print(f"Issues: {results_high_bc['issues']}")

    sample_investor_bad_mobile_dob = {
        "mobile_number": "12345",
        "email": "",
        "dob": "2050-01-01",
        "individual_monthly_income": 30000,
        "occupation": "Blue-Collar"
    }
    print("\nTest 4: Invalid mobile and DOB")
    results_bad_fields = run_all_validations(sample_investor_bad_mobile_dob, mock_econ_normal, profile_id="B2")
    print(f"Overall Valid: {results_bad_fields['overall_valid']}")
    print(f"Issues: {results_bad_fields['issues']}")

