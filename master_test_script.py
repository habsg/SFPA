# master_test_script.py

from datetime import datetime, date
import json

# --- Consolidated Helper Functions (e.g., from profiling_logic or risk_assessment_logic) ---
def calculate_age(dob_str: str, reference_date_str: str = None) -> int:
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

# --- Import logic from other files ---
from profiling_logic import assign_investor_profile, WHITE_COLLAR_PROFILES, BLUE_COLLAR_PROFILES
from risk_assessment_logic import calculate_risk_score as calc_risk_score_external, get_risk_rating as get_risk_rating_external, calculate_required_emergency_fund
from savings_logic import calculate_savings_details, get_annual_savings_adjustment_rate 
from financial_goals_logic import get_sip_scenarios, prioritize_goals, suggest_fund_type_for_goal, GOAL_PRIORITIES
from economic_data_logic import get_latest_economic_data, get_historical_trend, generate_ai_forecast as econ_ai_forecast, check_early_warning_triggers
from ai_validation_logic import run_all_validations
from communication_logic import generate_profile_transition_notification, generate_economic_slowdown_alert, send_app_notification
from report_generation_logic import generate_investor_report_html, format_currency # format_currency is used for action_plan
from compliance_logic import create_audit_log_entry, mask_sensitive_data


# --- Master Test Function ---
def run_comprehensive_test_scenario():
    print("--- Starting Comprehensive Test Scenario ---")

    # 1. Investor Data Input (Sample)
    investor_input_data = {
        "name": "Test Investor One",
        "dob": "1985-07-15", 
        "occupation": "White-Collar",
        "individual_monthly_income": 75000.0,
        "spouse_monthly_income": 25000.0, 
        "num_dependents_form": 2, 
        "dependents_details_form": [{"age": 10}, {"age": 5}], 
        "current_emergency_fund": 150000.0,
        "monthly_rent": 20000.0,
        "monthly_emi": 10000.0,
        "market_linked_experience": "Yes",
        "urban_rural_status": "Urban",
        "home_ownership": False,
        "num_education_marriage_goals_completed_for_dependents": 0,
        "risk_questionnaire_answers": ["Somewhat likely", "Lean towards equity fund", "Somewhat willing", "Hold and monitor closely", "Mildly anxious, somewhat concerned"],
        "mobile_number": "9876543210",
        "email": "test.investor@example.com"
    }
    plan_in_action_date_str = datetime.now().strftime("%Y-%m-%d")

    # 2. AI Validation of Inputs
    print("\n--- 2. AI Input Validation ---")
    all_profile_definitions_for_ai_val = {}
    for prof_list in [WHITE_COLLAR_PROFILES, BLUE_COLLAR_PROFILES]:
        for p_data in prof_list:
            all_profile_definitions_for_ai_val[p_data[0]] = {
                "min_income": p_data[5], "max_income": p_data[6],
                "occupation_type": investor_input_data["occupation"]
            }

    latest_econ_data_for_val = get_latest_economic_data()
    validation_results = run_all_validations(investor_input_data, economic_indicators=latest_econ_data_for_val, all_profiles_master_data=all_profile_definitions_for_ai_val)
    print(f"Input Validation Results: Overall Valid: {validation_results['overall_valid']}")
    if validation_results["issues"]:
        print("Validation Issues:")
        for issue in validation_results["issues"]:
            print(f"  - Field: {issue.get('field')}, Message: {issue.get('message')}")
    if not validation_results["overall_valid"] and any(i.get("type") != "consistency_warning" and i.get("type") != "context_warning" for i in validation_results["issues"]):
        print("Critical input validation failed. Aborting test scenario.")
        return

    # 3. Profiling
    print("\n--- 3. Investor Profiling ---")
    assigned_profile_id = assign_investor_profile(
        occupation=investor_input_data["occupation"],
        dob_str=investor_input_data["dob"],
        individual_monthly_income=investor_input_data["individual_monthly_income"],
        num_dependents=investor_input_data["num_dependents_form"],
        plan_in_action_date_str=plan_in_action_date_str
    )
    print(f"Assigned Profile ID: {assigned_profile_id}")
    if not assigned_profile_id:
        print("Could not assign profile. Aborting.")
        return

    # 4. Risk Assessment
    print("\n--- 4. Risk Assessment ---")
    risk_score, risk_score_details = calc_risk_score_external(
        dob_str=investor_input_data["dob"],
        occupation=investor_input_data["occupation"],
        total_household_monthly_income=investor_input_data["individual_monthly_income"] + investor_input_data["spouse_monthly_income"],
        num_dependents=investor_input_data["num_dependents_form"],
        current_emergency_fund=investor_input_data["current_emergency_fund"],
        monthly_rent=investor_input_data["monthly_rent"],
        monthly_emi=investor_input_data["monthly_emi"],
        market_linked_experience=investor_input_data["market_linked_experience"],
        risk_questionnaire_answers=investor_input_data["risk_questionnaire_answers"],
        plan_in_action_date_str=plan_in_action_date_str
    )
    risk_rating = get_risk_rating_external(risk_score)
    print(f"Calculated Risk Score: {risk_score}, Rating: {risk_rating}")

    # 5. Savings Calculation
    print("\n--- 5. Savings Calculation ---")
    savings_calc_input = {
        "occupation": investor_input_data["occupation"],
        "individual_monthly_income": investor_input_data["individual_monthly_income"],
        "spouse_monthly_income": investor_input_data["spouse_monthly_income"],
        "monthly_rent": investor_input_data["monthly_rent"],
        "monthly_emi": investor_input_data["monthly_emi"],
        "dependents": investor_input_data["dependents_details_form"],
        "urban_rural_status": investor_input_data["urban_rural_status"],
        "home_ownership": investor_input_data["home_ownership"],
        "num_education_marriage_goals_completed_for_dependents": investor_input_data["num_education_marriage_goals_completed_for_dependents"]
    }
    savings_details = calculate_savings_details(savings_calc_input)
    print(f"Recommended Monthly Savings: {format_currency(savings_details.get('final_monthly_savings_amount'))}")
    print(f"Disposable Monthly Income: {format_currency(savings_details.get('disposable_monthly_income'))}")
    print(f"Feasibility Index: {savings_details.get('feasibility_index')}%" )

    # 6. Financial Goals (Example)
    print("\n--- 6. Financial Goals ---")
    investor_goals_input = [
        {"goal_type": "Child Education", "target_amount": 1500000, "timeline_years": 8, "current_corpus": 100000},
        {"goal_type": "Retirement", "target_amount": 10000000, "timeline_years": 20, "current_corpus": 500000}
    ]
    prioritized_investor_goals = prioritize_goals(investor_goals_input)
    print("Prioritized Goals:")
    processed_goals_for_report = []
    for goal in prioritized_investor_goals:
        fund_type = suggest_fund_type_for_goal(goal["goal_type"], goal["timeline_years"], risk_rating)
        sip_scenarios = get_sip_scenarios(goal["target_amount"], goal["timeline_years"], fund_type, goal["current_corpus"])
        print(f"  - Goal: {goal['goal_type']}, Target: {format_currency(goal['target_amount'])}")
        print(f"    Timeline: {goal['timeline_years']} yrs, Suggested Fund: {fund_type}")
        print(f"    SIP (Base Case): {format_currency(sip_scenarios['sip_base_case'])} at {sip_scenarios['base_case_annual_return']}% return")
        goal["recommended_fund_type"] = fund_type
        goal["sip_scenarios"] = sip_scenarios # Ensure sip_scenarios is part of the goal dict for the report
        goal["status"] = "Planning"
        goal["progress_percentage"] = (goal["current_corpus"] / goal["target_amount"]) * 100 if goal["target_amount"] > 0 else 0
        processed_goals_for_report.append(goal)

    # 7. Economic Data & Warnings
    print("\n--- 7. Economic Data & Warnings ---")
    latest_economic_indicators = get_latest_economic_data()
    if latest_economic_indicators is not None:
        gdp_growth_rate = latest_economic_indicators.get("gdp_growth_rate")
        cpi_inflation = latest_economic_indicators.get("cpi_inflation") # Corrected key for inflation
        print(f"Latest GDP Growth: {gdp_growth_rate}%, CPI Inflation: {cpi_inflation}%")
        warnings = check_early_warning_triggers(latest_economic_indicators)
        if warnings:
            print("Economic Warnings:")
            for warning_msg in warnings:
                print(f"  - {warning_msg}")
                if "GDP Growth Rate is low" in warning_msg and gdp_growth_rate is not None:
                    econ_alert = generate_economic_slowdown_alert(gdp_growth=gdp_growth_rate, fund_suggestion="Value Funds", language="en")
                    send_app_notification(investor_id="TEST_INVESTOR_01", notification_payload=econ_alert)

    # 8. Compliance: Audit Log Example
    print("\n--- 8. Compliance: Audit Logging ---")
    audit_entry = create_audit_log_entry(
        user_id="MFD_SystemTest",
        action_type="COMPREHENSIVE_PLAN_GENERATED",
        investor_id_context="TEST_INVESTOR_01",
        details={"profile_id": assigned_profile_id, "risk_score": risk_score, "num_goals": len(processed_goals_for_report)}
    )
    print(f"Audit Logged: {json.dumps(audit_entry)}")

    # 9. Report Generation - Prepare arguments for generate_investor_report_html
    print("\n--- 9. Report Generation ---")

    # Argument 1: investor_data
    investor_data_arg = {
        "name": investor_input_data["name"],
        "dob": investor_input_data["dob"],
        "occupation": investor_input_data["occupation"],
        "mobile_number": investor_input_data["mobile_number"],
        "email": investor_input_data["email"]
    }

    # Argument 2: profile_details
    profile_description = "N/A"
    # Fetch profile description from WHITE_COLLAR_PROFILES or BLUE_COLLAR_PROFILES
    # These are lists of tuples: (profile_id, description, ...)
    all_profiles_master = WHITE_COLLAR_PROFILES + BLUE_COLLAR_PROFILES
    for p_data in all_profiles_master:
        if p_data[0] == assigned_profile_id:
            profile_description = p_data[1] # Second element is description
            break
    profile_details_arg = {
        "profile_id": assigned_profile_id,
        "description": profile_description
    }

    # Argument 3: risk_assessment
    risk_assessment_arg = {
        "total_score": risk_score,
        "risk_rating": risk_rating
    }

    # Argument 4: financial_goals
    # processed_goals_for_report already contains 'sip_scenarios' which has 'sip_base_case'
    financial_goals_arg = processed_goals_for_report 

    # Argument 5: savings_summary
    savings_summary_arg = {
        "final_monthly_savings_amount": savings_details.get("final_monthly_savings_amount"),
        "disposable_monthly_income": savings_details.get("disposable_monthly_income"),
        "final_applicable_savings_rate": savings_details.get("final_applicable_savings_rate"),
        "feasibility_index": savings_details.get("feasibility_index")
    }

    # Argument 6: asset_allocation_summary (Placeholder)
    asset_allocation_summary_arg = {
        "Equity (Large Cap)": "40%", 
        "Equity (Mid/Small Cap)": "20%", 
        "Debt (Long Term)": "30%", 
        "Gold": "10%"
    } # Placeholder, as this is not calculated in the current script flow

    # Argument 7: action_plan
    action_plan_arg = []
    for goal in processed_goals_for_report:
        if goal.get('sip_scenarios') and goal['sip_scenarios'].get('sip_base_case') is not None:
            action_plan_arg.append(f"Initiate SIP of {format_currency(goal['sip_scenarios']['sip_base_case'])} in a {goal.get('recommended_fund_type', 'suggested fund')} for {goal.get('goal_type', 'goal')}.")
    action_plan_arg.append("Review portfolio quarterly and rebalance if necessary.") # Generic action
    action_plan_arg.append("Ensure emergency fund is maintained at the recommended level.")

    # Argument 8: economic_outlook
    economic_outlook_arg = {}
    if latest_economic_indicators is not None:
        economic_outlook_arg["gdp_growth_rate"] = latest_economic_indicators.get("gdp_growth_rate", "N/A")
        economic_outlook_arg["inflation_rate_cpi"] = latest_economic_indicators.get("cpi_inflation", "N/A") # report_generation_logic.py expects 'inflation_rate_cpi'
        economic_outlook_arg["repo_rate"] = latest_economic_indicators.get("repo_rate", "N/A")
    else:
        economic_outlook_arg = {"gdp_growth_rate": "N/A", "inflation_rate_cpi": "N/A", "repo_rate": "N/A"}

    # Call generate_investor_report_html with all 8 arguments
    html_report = generate_investor_report_html(
        investor_data_arg,
        profile_details_arg,
        risk_assessment_arg,
        financial_goals_arg,
        savings_summary_arg,
        asset_allocation_summary_arg,
        action_plan_arg,
        economic_outlook_arg
    )
    
    report_filename = "test_investor_report.html" # Using relative path
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(html_report)
    print(f"Generated Investor Report: {report_filename}")

    print("\n--- Comprehensive Test Scenario Completed ---")

if __name__ == "__main__":
    run_comprehensive_test_scenario()

