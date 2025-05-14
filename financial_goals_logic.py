# financial_goals_logic.py

import math

# --- Goal Definitions (from Framework Part 1, Section 7) ---
FUND_TYPE_RETURNS = {
    "Ultra Short/Low Duration": [0.05, 0.065],
    "Liquid Fund": [0.04, 0.06],
    "Balanced Advantage": [0.06, 0.12],
    "Value Fund": [0.07, 0.12],
    "Dividend Yield Fund": [0.07, 0.12],
    "Contra Fund": [0.09, 0.16],
    "Multi Cap Fund": [0.09, 0.16],
    "Aggressive Hybrid": [0.08, 0.14]
}

def get_return_rates_for_fund_type(fund_type: str) -> tuple[float, float, float]:
    """Returns (worst, base, best) annual return rates for a fund type."""
    if fund_type not in FUND_TYPE_RETURNS:
        print(f"Warning: Fund type {fund_type} not found in FUND_TYPE_RETURNS. Using default conservative rates.")
        default_rates = [0.04, 0.07]
        worst_annual = default_rates[0]
        best_annual = default_rates[1]
    else:
        worst_annual = FUND_TYPE_RETURNS[fund_type][0]
        best_annual = FUND_TYPE_RETURNS[fund_type][1]
    
    base_annual = (worst_annual + best_annual) / 2
    return worst_annual, base_annual, best_annual

def calculate_sip(
    target_amount: float,
    timeline_years: int,
    annual_return_rate: float,
    current_corpus: float = 0.0
) -> float:
    """
    Calculates the required monthly SIP to reach a target amount.
    """
    if target_amount <= 0 or timeline_years <= 0:
        return 0.0
    if annual_return_rate <= 0:
        required_from_sip = target_amount - current_corpus
        if required_from_sip <= 0: return 0.0
        return required_from_sip / (timeline_years * 12) if timeline_years * 12 > 0 else float("inf")

    monthly_return_rate = annual_return_rate / 12
    num_months = timeline_years * 12

    fv_current_corpus = current_corpus * ((1 + monthly_return_rate) ** num_months)
    required_fv_from_sip = target_amount - fv_current_corpus

    if required_fv_from_sip <= 0:
        return 0.0

    if monthly_return_rate == 0:
         return required_fv_from_sip / num_months if num_months > 0 else float("inf")

    denominator_part1 = ((1 + monthly_return_rate)**num_months - 1) / monthly_return_rate
    denominator_full = denominator_part1 * (1 + monthly_return_rate)
    
    if denominator_full == 0:
        return float("inf")
        
    monthly_sip = required_fv_from_sip / denominator_full
    return round(max(0, monthly_sip), 2)

def get_sip_scenarios(target_amount: float, timeline_years: int, fund_type: str, current_corpus: float = 0.0) -> dict:
    """Calculates SIP for worst, base, and best-case return scenarios."""
    worst_r, base_r, best_r = get_return_rates_for_fund_type(fund_type)
    
    sip_worst = calculate_sip(target_amount, timeline_years, worst_r, current_corpus)
    sip_base = calculate_sip(target_amount, timeline_years, base_r, current_corpus)
    sip_best = calculate_sip(target_amount, timeline_years, best_r, current_corpus)
    
    return {
        "worst_case_annual_return": round(worst_r * 100, 2),
        "sip_worst_case": sip_worst,
        "base_case_annual_return": round(base_r * 100, 2),
        "sip_base_case": sip_base,
        "best_case_annual_return": round(best_r * 100, 2),
        "sip_best_case": sip_best
    }

GOAL_PRIORITIES = {
    "Debt Reduction": 1,
    "Emergency Fund": 2,
    "Child Education": 3,
    "Child Marriage": 4,
    "Retirement": 5,
    "Home Purchase": 6,
    "Self-Education": 7,
    "Other": 8
}

def prioritize_goals(goals: list) -> list:
    """Sorts goals based on predefined priorities. goals is a list of dicts, each with a 'goal_type'."""
    return sorted(goals, key=lambda g: GOAL_PRIORITIES.get(g.get("goal_type"), 99))

def suggest_fund_type_for_goal(goal_type: str, timeline_years: int, risk_profile: str) -> str:
    """
    Suggests a fund type based on goal, timeline, and investor's risk profile.
    """
    if goal_type == "Debt Reduction":
        return "Ultra Short/Low Duration"
    if goal_type == "Emergency Fund":
        if timeline_years <= 1: return "Liquid Fund"
        return "Ultra Short/Low Duration"

    if timeline_years <= 1:
        if risk_profile in ["Very Low", "Low"]:
            return "Ultra Short/Low Duration"
        return "Value Fund"
    elif timeline_years <= 3:
        if risk_profile in ["Very Low", "Low"]:
            return "Value Fund"
        elif risk_profile == "Moderate":
            return "Balanced Advantage"
        else:
            return "Value Fund"
    elif timeline_years <= 7:
        if risk_profile in ["Very Low", "Low"]:
            return "Value Fund"
        elif risk_profile == "Moderate":
            return "Balanced Advantage"
        else:
            return "Multi Cap Fund"
    else:
        if risk_profile in ["Very Low", "Low"]:
            return "Balanced Advantage"
        elif risk_profile == "Moderate":
            return "Multi Cap Fund"
        else:
            return "Contra Fund"

    return "Balanced Advantage" 

if __name__ == "__main__":
    print("--- Test Cases for Financial Goals Logic ---")

    print("\n-- SIP Calculation Tests --")
    target = 500000
    years = 7
    corpus = 50000
    print(f"Goal: Target {target}, Years {years}, Current Corpus {corpus}")
    
    scenarios_value_fund = get_sip_scenarios(target, years, "Value Fund", corpus)
    print(f"SIP Scenarios for Value Fund: {scenarios_value_fund}")

    scenarios_contra_fund = get_sip_scenarios(target, years, "Contra Fund", corpus)
    print(f"SIP Scenarios for Contra Fund: {scenarios_contra_fund}")

    sip_zero_return = calculate_sip(120000, 1, 0, 0)
    print(f"SIP for 120k in 1yr at 0% return: {sip_zero_return}")
    sip_zero_return_corpus = calculate_sip(120000, 1, 0, 60000)
    print(f"SIP for 120k in 1yr at 0% return with 60k corpus: {sip_zero_return_corpus}")

    print("\n-- Goal Prioritization Test --")
    sample_goals = [
        {"goal_type": "Retirement", "details": "..."},
        {"goal_type": "Emergency Fund", "details": "..."},
        {"goal_type": "Child Education", "details": "..."},
        {"goal_type": "Debt Reduction", "details": "..."}
    ]
    prioritized = prioritize_goals(sample_goals)
    # Corrected f-string for list comprehension
    print(f"Prioritized Goals: {[g['goal_type'] for g in prioritized]}")

    print("\n-- Fund Type Suggestion Tests --")
    print(f"Goal: Debt Reduction, 2yrs, Moderate risk: {suggest_fund_type_for_goal('Debt Reduction', 2, 'Moderate')}")
    print(f"Goal: Emergency Fund, 1yr, Low risk: {suggest_fund_type_for_goal('Emergency Fund', 1, 'Low')}")
    print(f"Goal: Education, 10yrs, High risk: {suggest_fund_type_for_goal('Child Education', 10, 'High')}")
    print(f"Goal: Home Purchase, 5yrs, Moderate risk: {suggest_fund_type_for_goal('Home Purchase', 5, 'Moderate')}")
    print(f"Goal: Retirement, 20yrs, Low risk: {suggest_fund_type_for_goal('Retirement', 20, 'Low')}")
    print(f"Goal: Self-Education, 2yrs, Very High risk: {suggest_fund_type_for_goal('Self-Education', 2, 'Very High')}")

