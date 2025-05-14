# savings_logic.py

from typing import Dict, Any

# --- Framework Definitions (Part 1, Section 8 & 9) ---

# Recommended Savings Rates - Blue-Collar
BLUE_COLLAR_SAVINGS_SLABS = [
    {"max_disposable_income": 15000, "rate": 0.10},
    {"max_disposable_income": 25000, "rate": 0.15},
    {"max_disposable_income": 30000, "rate": 0.20},
    {"max_disposable_income": float("inf"), "rate": 0.25}
]

# Recommended Savings Rates - White-Collar
WHITE_COLLAR_SAVINGS_SLABS = [
    {"max_disposable_income": 15000, "rate": 0.15},
    {"max_disposable_income": 30000, "rate": 0.17},
    {"max_disposable_income": 45000, "rate": 0.20},
    {"max_disposable_income": float("inf"), "rate": 0.25}
]

RURAL_SAVINGS_BONUS_RATE = 0.03
HOME_OWNERSHIP_BONUS_RATE = 0.02
NO_EMI_BONUS_RATE = 0.01
GOAL_COMPLETED_BONUS_PER_DEPENDENT = 0.01
MAX_GOAL_COMPLETED_BONUS = 0.03

# Spouse Income Ratio Modifiers - White-Collar
WC_SPOUSE_INCOME_MODIFIERS = [
    {"max_ratio": 0.20, "bonus": 0.005},
    {"max_ratio": 0.50, "bonus": 0.01},
    {"max_ratio": float("inf"), "bonus": 0.02}
]

# Spouse Income Ratio Modifiers - Blue-Collar
BC_SPOUSE_INCOME_MODIFIERS = [
    {"max_ratio": 0.20, "bonus": 0.003},
    {"max_ratio": 0.50, "bonus": 0.007},
    {"max_ratio": float("inf"), "bonus": 0.01}
]

# Dependent Deduction Rates (Framework Part 1, Sec 6)
DEPENDENT_DEDUCTION_RATES = [
    {"min_age": 1, "max_age": 5, "rate": 0.05},
    {"min_age": 6, "max_age": 10, "rate": 0.075},
    {"min_age": 11, "max_age": float("inf"), "rate": 0.10} # Assuming 11+ for 10%
]
MAX_TOTAL_DEPENDENT_DEDUCTION_RATE = 0.30
MAX_DISPOSABLE_INCOME_AS_FRACTION_OF_HOUSEHOLD = 0.70
MIN_SAVINGS_RATE_OF_HOUSEHOLD_INCOME = 0.10

# Annual Savings Adjustment Rates (Framework Part 1, Section 9 - simplified placeholder)
ANNUAL_ADJUSTMENT_RATES_PLACEHOLDER: Dict[str, Dict[str, float]] = {
    "default": {"base_rate": 0.05, "fallback_rate": 0.025},
    "W1": {"base_rate": 0.07, "fallback_rate": 0.035},
    "B8": {"base_rate": 0.04, "fallback_rate": 0.02},
}

def get_annual_savings_adjustment_rate(profile_id: str, economic_condition: str = "Normal") -> float:
    """Gets the annual savings adjustment rate for a given profile and economic condition."""
    profile_rates = ANNUAL_ADJUSTMENT_RATES_PLACEHOLDER.get(profile_id, ANNUAL_ADJUSTMENT_RATES_PLACEHOLDER["default"])
    if economic_condition == "Slowdown":
        return profile_rates["fallback_rate"]
    return profile_rates["base_rate"]

def calculate_savings_details(investor_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates detailed savings information based on investor data and framework rules.
    """
    results = {}
    household_income = investor_data.get("individual_monthly_income", 0.0) + investor_data.get("spouse_monthly_income", 0.0)
    results["household_monthly_income"] = household_income
    if household_income <= 0:
        results.update({
            "dependent_deduction_amount": 0,
            "disposable_monthly_income": 0,
            "base_savings_rate_from_slab": 0,
            "total_modifiers_bonus_rate": 0,
            "final_applicable_savings_rate": 0,
            "calculated_savings_from_disposable": 0,
            "min_savings_based_on_household_income": 0,
            "final_monthly_savings_amount": 0,
            "blended_savings_rate_of_household_income": 0,
            "feasibility_index": 0
        })
        return results

    total_dependent_deduction_rate = 0
    if investor_data.get("dependents"):
        for dep in investor_data["dependents"]:
            dep_age = dep.get("age", 0)
            for rate_info in DEPENDENT_DEDUCTION_RATES:
                if rate_info["min_age"] <= dep_age <= rate_info["max_age"]:
                    total_dependent_deduction_rate += rate_info["rate"]
                    break
    total_dependent_deduction_rate = min(total_dependent_deduction_rate, MAX_TOTAL_DEPENDENT_DEDUCTION_RATE)
    dependent_deduction_amount = household_income * total_dependent_deduction_rate
    results["total_dependent_deduction_rate"] = total_dependent_deduction_rate
    results["dependent_deduction_amount"] = round(dependent_deduction_amount, 2)

    disposable_income = household_income - investor_data.get("monthly_rent", 0.0) - investor_data.get("monthly_emi", 0.0) - dependent_deduction_amount
    disposable_income = max(0, min(disposable_income, household_income * MAX_DISPOSABLE_INCOME_AS_FRACTION_OF_HOUSEHOLD))
    results["disposable_monthly_income"] = round(disposable_income, 2)

    slabs = WHITE_COLLAR_SAVINGS_SLABS if investor_data["occupation"] == "White-Collar" else BLUE_COLLAR_SAVINGS_SLABS
    base_savings_rate = 0
    for slab in slabs:
        if disposable_income <= slab["max_disposable_income"]:
            base_savings_rate = slab["rate"]
            break
    results["base_savings_rate_from_slab"] = base_savings_rate

    modifier_bonus_rate = 0
    if investor_data.get("urban_rural_status") == "Rural":
        modifier_bonus_rate += RURAL_SAVINGS_BONUS_RATE
    if investor_data.get("home_ownership", False):
        modifier_bonus_rate += HOME_OWNERSHIP_BONUS_RATE
    if investor_data.get("monthly_emi", 0.0) == 0:
        modifier_bonus_rate += NO_EMI_BONUS_RATE
    
    goals_completed_bonus = min(
        investor_data.get("num_education_marriage_goals_completed_for_dependents", 0) * GOAL_COMPLETED_BONUS_PER_DEPENDENT,
        MAX_GOAL_COMPLETED_BONUS
    )
    modifier_bonus_rate += goals_completed_bonus

    spouse_income = investor_data.get("spouse_monthly_income", 0.0)
    if household_income > 0 and spouse_income > 0:
        spouse_income_ratio = spouse_income / household_income
        spouse_modifiers = WC_SPOUSE_INCOME_MODIFIERS if investor_data["occupation"] == "White-Collar" else BC_SPOUSE_INCOME_MODIFIERS
        for mod in spouse_modifiers:
            if spouse_income_ratio <= mod["max_ratio"]:
                modifier_bonus_rate += mod["bonus"]
                break
    results["total_modifiers_bonus_rate"] = modifier_bonus_rate

    final_applicable_savings_rate = base_savings_rate + modifier_bonus_rate
    results["final_applicable_savings_rate"] = final_applicable_savings_rate

    calculated_savings = disposable_income * final_applicable_savings_rate
    results["calculated_savings_from_disposable"] = round(calculated_savings, 2)

    min_savings_household = household_income * MIN_SAVINGS_RATE_OF_HOUSEHOLD_INCOME
    results["min_savings_based_on_household_income"] = round(min_savings_household, 2)

    final_savings = 0
    if disposable_income > 0:
        final_savings = max(calculated_savings, min_savings_household)
    
    if final_savings < 4000:
        final_savings = round(final_savings / 100) * 100
    else:
        final_savings = round(final_savings / 500) * 500
    results["final_monthly_savings_amount"] = round(final_savings, 2)

    blended_rate = (final_savings / household_income) * 100 if household_income > 0 else 0
    results["blended_savings_rate_of_household_income"] = round(blended_rate, 2)

    feasibility_index = ((disposable_income - final_savings) / disposable_income) * 100 if disposable_income > 0 else 0
    feasibility_index = max(0, feasibility_index)
    results["feasibility_index"] = round(feasibility_index, 2)

    return results

if __name__ == "__main__":
    print("--- Test Cases for Savings Logic ---")

    priya_patel_data = {
        "occupation": "Blue-Collar",
        "individual_monthly_income": 27000,
        "spouse_monthly_income": 10000,
        "monthly_rent": 12000,
        "monthly_emi": 12500,
        "dependents": [{"age": 8}, {"age": 10}],
        "urban_rural_status": "Urban",
        "home_ownership": False, 
        "num_education_marriage_goals_completed_for_dependents": 0
    }
    priya_results = calculate_savings_details(priya_patel_data)
    print("Priya Patel Example Results:")
    for key, value in priya_results.items():
        print(f"  {key}: {value}")

    wc_rural_data = {
        "occupation": "White-Collar",
        "individual_monthly_income": 80000,
        "spouse_monthly_income": 40000, 
        "monthly_rent": 0,
        "monthly_emi": 0,
        "dependents": [{"age": 3}], 
        "urban_rural_status": "Rural",
        "home_ownership": True,
        "num_education_marriage_goals_completed_for_dependents": 1
    }
    wc_rural_results = calculate_savings_details(wc_rural_data)
    print("\nWhite-Collar Rural Example Results:")
    for key, value in wc_rural_results.items():
        print(f"  {key}: {value}")

    no_income_data = {
        "occupation": "Blue-Collar",
        "individual_monthly_income": 0,
        "spouse_monthly_income": 0,
        "monthly_rent": 5000,
        "monthly_emi": 1000,
        "dependents": [],
        "urban_rural_status": "Urban",
        "home_ownership": False,
        "num_education_marriage_goals_completed_for_dependents": 0
    }
    no_income_results = calculate_savings_details(no_income_data)
    print("\nNo Income Example Results:")
    for key, value in no_income_results.items():
        print(f"  {key}: {value}")

    print("\nAnnual Adjustment Rate Tests:")
    print(f"Default Normal: {get_annual_savings_adjustment_rate('WXYZ', 'Normal')}")
    print(f"Default Slowdown: {get_annual_savings_adjustment_rate('WXYZ', 'Slowdown')}")
    print(f"W1 Normal: {get_annual_savings_adjustment_rate('W1', 'Normal')}")
    print(f"B8 Slowdown: {get_annual_savings_adjustment_rate('B8', 'Slowdown')}")

