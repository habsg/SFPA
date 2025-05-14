# Comprehensive Financial Planning Framework (2025) (MFD version) - Part 1

## Table of Contents
1. [Introduction](#introduction)
2. [Purpose of the Framework](#purpose-of-the-framework)
3. [Investor Profiles](#investor-profiles)
4. [Income Level Methodology for 2025](#income-level-methodology-for-2025)
5. [Investor Profiling and Data Collection](#investor-profiling-and-data-collection)
   - 5.1 Investor Profile and Risk Assessment Form
   - 5.2 Profile Assignment
   - 5.3 Income Updates and Profile Transitions
   - 5.4 Error Handling
6. [Financial Goals and Prioritization](#financial-goals-and-prioritization)
7. [Specific Financial Goals](#specific-financial-goals)
8. [Recommended Savings Rates for Investors](#recommended-savings-rates-for-investors)
9. [Annual Savings Adjustment Rates](#annual-savings-adjustment-rates)
10. [Emergency Fund Requirements](#emergency-fund-requirements)
11. [Risk Tolerance Assessment](#risk-tolerance-assessment)
    - 11.1 Overview
    - 11.2 AI Integration
    - 11.3 Dynamic Risk Scoring
    - 11.4 Stress Testing
    - 11.5 Historical Risk Score Tracking
    - 11.6 Error Handling
12. [Indicative Returns of Mutual Fund Schemes](#indicative-returns-of-mutual-fund-schemes)
13. [Mutual Fund Investment Options Based on Goals](#mutual-fund-investment-options-based-on-goals)
14. [Plan Lock Mechanism](#plan-lock-mechanism)
15. [Feasibility Analysis](#feasibility-analysis)
16. [Annual Health Checks](#annual-health-checks)
    - 16.1 Overview
    - 16.2 Components
    - 16.3 Version Control for Annual Updates
    - 16.4 Automated Update Triggers
    - 16.5 Backward Compatibility
    - 16.6 Error Handling
17. [App Integration Logic Flow](#app-integration-logic-flow)
    - 17.1 Data Collection
    - 17.2 Real-Time Validation
    - 17.3 Scenario Analysis Tool
    - 17.4 AI API Resilience
    - 17.5 Plan Generation and UI/UX
    - 17.6 Error Handling

---

### 1. Introduction
This document, Part 1 of the **Comprehensive Financial Planning Framework (2025) (MFD version)**, outlines a standalone financial planning system for Indian investors, managed by Mutual Fund Distributors (MFDs) via an intuitive application. It defines 30 investor profiles (W1–W15 White-Collar, B1–B15 Blue-Collar), covering profiling, risk assessment, goal prioritization, savings calculations, investment selection, a three-year plan lock mechanism, and sensitivity analysis for market volatility and economic slowdowns. The framework integrates **AI features** (Goal Adjustments, Predictive Insights, Error Detection, Dynamic Risk Scoring) and an **enhanced AI prompt system** to optimize plans, anticipate life events, and ensure data accuracy. It supports capturing and updating income changes (self and spouse), profile transitions, automated annual updates, multilingual communication, visual aids, real-time validation, scenario analysis, and API resilience, adhering to the **Digital Personal Data Protection Act (DPDP Act, 2023)** and SEBI regulations.

Part 1 focuses on foundational elements, including investor profiling, income updates, risk assessment, annual health checks, and app integration with enhanced documentation (glossary, flowcharts, error handling). Part 2 covers communication, MFD guidance, data storage, and additional components, including the Economic Update section for tracking economic indicators. In the **Combined Version**, investors access a read-only portal (`/investor-login`) using Investor ID and OTP to view reports (e.g., Investor Guide), with MFDs controlling access and sensitive data masked.

**Current Date**: May 12, 2025. The framework supports continuous updates to reflect economic conditions and investor needs.

**Combined Version Note**: Investors view personalized reports but cannot edit plans or interact with AI prompts.

---

### 2. Purpose of the Framework
The framework aims to:
- **Personalize Financial Plans**: Tailor plans based on investor profiles, goals, savings, and investments, with a three-year lock for stability, sensitivity analysis for robustness, and AI-driven optimizations.
- **Assess Risk Tolerance**: Evaluate risk profiles dynamically with stress testing and AI validation to recommend suitable investments, including value, dividend yield, and contra funds during economic slowdowns.
- **Prioritize Financial Goals**: Sequence goals (e.g., debt reduction, emergency fund, education) with AI-driven trade-offs.
- **Guide Investment Decisions**: Recommend mutual fund schemes, including value, dividend yield, and contra funds, with scenario-based savings calculations (best-case, base-case, worst-case), enhanced by AI suggestions.
- **Capture Income Changes**: Update income (self and spouse) via annual health checks, ad-hoc updates, and Consolidated Account Statement (CAS) triggers, with profile transitions communicated clearly.
- **Ensure Plan Stability**: Lock plan structure for three years, allowing savings adjustments via version-controlled annual updates, automated triggers, and backward compatibility, with optional dynamic adjustments based on economic indicators.
- **Streamline Communication**: Support English, Hindi, Tamil, Bengali, Telugu, Marathi with infographics for low-literacy investors (Part 2).
- **Optimize App Integration**: Implement real-time validation, scenario analysis tools, economic dashboards, and API resilience for seamless functionality.
- **Enhance Documentation**: Provide a glossary, flowcharts, and error-handling procedures for clarity.
- **Ensure Privacy and Compliance**: Protect data through encryption and audit logging.

**Combined Version Note**: Investors view AI-driven recommendations in reports but cannot edit plans or access AI prompts.

---

### 3. Investor Profiles
#### Purpose
The Investor Profiles define 30 categories (W1–W15 White-Collar, B1–B15 Blue-Collar) to standardize financial planning based on life cycle stage, income level, and financial context. Profiles are locked for three years from the Plan in Action Date to ensure plan stability, with transitions handled post-lock or on significant income changes.

#### Data Points
- **Monthly Income**: Determines income level (Low, Sufficient, Good) based on individual income.
- **Date of Birth (DOB)**: Derives age dynamically for life cycle stage assignment.
- **Number and DOB of Dependents**: Assesses family responsibilities, fixed at Plan in Action Date during lock.
- **Occupation**: White-Collar or Blue-Collar.
- **Urban/Rural Status**: Adjusts savings rates (+3% for rural) and goal costs.
- **Rent Amount**: Monthly rent paid (₹0 if none).
- **EMI Amount**: Total monthly EMI for loans (₹0 if none).
- **Spouse’s Monthly Income**: Contributes to Household Income for savings calculations.
- **Plan in Action Date**: Date the plan is activated, defaulting to Plan Creation Date.
- **Predictive Signals**: Optional, for AI-driven life event forecasting (e.g., family planning intentions, job stability).

#### Life Cycle Stages
- **Young Adult**: Age 22–30, 0–1 dependents.
- **Young Family**: Age 28–35, young children (0–7 years).
- **Mid-Career Family**: Age 35–50, children 8–18 years.
- **Pre-Retirement**: Age 50–60, adult children (>18 years).
- **Retirement**: Age 60+, typically no minor dependents.

#### White-Collar Profiles
| Category ID | Life Cycle Stage       | Age Range | Income Level | Income Range (₹/month) | Sufficiency | Dependents                | Financial Context                                      |
|-------------|------------------------|-----------|--------------|------------------------|-------------|---------------------------|-------------------------------------------------------|
| W1          | Young Adult            | 22–30     | Low          | 0–30,000               | -           | 0–1 (none or spouse)      | Limited savings; starting career, possible debt.      |
| W2          | Young Adult            | 22–30     | Sufficient   | 30,001–60,000          | 0           | 0–1 (none or spouse)      | Moderate savings; building emergency fund.            |
| W3          | Young Adult            | 22–30     | Good         | >60,000                | +           | 0–1 (none or spouse)      | High savings; early retirement planning.              |
| W4          | Young Family           | 28–35     | Low          | 0–45,000               | -           | 1–2 (children, 0–7)       | Tight budget; focus on emergency fund, education.     |
| W5          | Young Family           | 28–35     | Sufficient   | 45,001–90,000          | 0           | 1–2 (children, 0–7)       | Balanced savings; home purchase, education goals.     |
| W6          | Young Family           | 28–35     | Good         | >90,000                | +           | 1–2 (children, 0–7)       | Strong savings; aggressive education, retirement.     |
| W7          | Mid-Career Family      | 35–50     | Low          | 0–67,500               | -           | 2–3 (children, 8–18)      | High expenses; education, marriage, debt challenges.  |
| W8          | Mid-Career Family      | 35–50     | Sufficient   | 67,501–135,000         | 0           | 2–3 (children, 8–18)      | Stable savings; education, marriage, retirement focus.|
| W9          | Mid-Career Family      | 35–50     | Good         | >135,000               | +           | 2–3 (children, 8–18)      | High savings; multiple goals, early retirement.       |
| W10         | Pre-Retirement         | 50–60     | Low          | 0–101,250              | -           | 0–2 (adult children, >18) | Limited savings; urgent retirement planning.          |
| W11         | Pre-Retirement         | 50–60     | Sufficient   | 101,251–202,500        | 0           | 0–2 (adult children, >18) | Moderate savings; retirement, marriage goals.         |
| W12         | Pre-Retirement         | 50–60     | Good         | >202,500               | +           | 0–2 (adult children, >18) | Strong savings; robust retirement planning.           |
| W13         | Retirement             | 60+       | Low          | 0–101,250              | -           | 0–1 (spouse, adults)      | Reliant on savings/pension; preservation focus.       |
| W14         | Retirement             | 60+       | Sufficient   | 101,251–202,500        | 0           | 0–1 (spouse, adults)      | Stable income; balanced retirement spending.          |
| W15         | Retirement             | 60+       | Good         | >202,500               | +           | 0–1 (spouse, adults)      | High savings; comfortable retirement lifestyle.       |

#### Blue-Collar Profiles
| Category ID | Life Cycle Stage       | Age Range | Income Level | Income Range (₹/month) | Sufficiency | Dependents                | Financial Context                                      |
|-------------|------------------------|-----------|--------------|------------------------|-------------|---------------------------|-------------------------------------------------------|
| B1          | Young Adult            | 22–30     | Low          | 0–12,000               | -           | 0–1 (none or spouse)      | Minimal savings; high debt risk.                      |
| B2          | Young Adult            | 22–30     | Sufficient   | 12,001–20,000          | 0           | 0–1 (none or spouse)      | Limited savings; emergency fund, small retirement.    |
| B3          | Young Adult            | 22–30     | Good         | >20,000                | +           | 0–1 (none or spouse)      | Moderate savings; home purchase, retirement plans.    |
| B4          | Young Family           | 28–35     | Low          | 0–18,000               | -           | 1–2 (children, 0–7)       | Tight budget; debt reduction, emergency fund focus.   |
| B5          | Young Family           | 28–35     | Sufficient   | 18,001–30,000          | 0           | 1–2 (children, 0–7)       | Modest savings; education, home purchase goals.       |
| B6          | Young Family           | 28–35     | Good         | >30,000                | +           | 1–2 (children, 0–7)       | Decent savings; education, home, retirement planning. |
| B7          | Mid-Career Family      | 35–50     | Low          | 0–27,000               | -           | 2–3 (children, 8–18)      | High debt risk; education, marriage focus.            |
| B8          | Mid-Career Family      | 35–50     | Sufficient   | 27,001–45,000          | 0           | 2–3 (children, 8–18)      | Balanced savings; education, marriage, retirement.    |
| B9          | Mid-Career Family      | 35–50     | Good         | >45,000                | +           | 2–3 (children, 8–18)      | Strong savings; multiple goals.                       |
| B10         | Pre-Retirement         | 50–60     | Low          | 0–40,500               | -           | 0–2 (adult children, >18) | Minimal savings; urgent retirement, debt challenges.  |
| B11         | Pre-Retirement         | 50–60     | Sufficient   | 40,501–67,500          | 0           | 0–2 (adult children, >18) | Modest savings; retirement, marriage goals.           |
| B12         | Pre-Retirement         | 50–60     | Good         | >67,500                | +           | 0–2 (adult children, >18) | Decent savings; comfortable retirement planning.      |
| B13         | Retirement             | 60+       | Low          | 0–40,500               | -           | 0–1 (spouse, adults)      | Limited savings; preservation focus.                  |
| B14         | Retirement             | 60+       | Sufficient   | 40,501–67,500          | 0           | 0–1 (spouse, adults)      | Stable savings; modest retirement lifestyle.          |
| B15         | Retirement             | 60+       | Good         | >67,500                | +           | 0–1 (spouse, adults)      | High savings; secure retirement lifestyle.            |

#### Notes for Developers
- **Age Derivation**: Calculate age as Current Year – Birth Year – (1 if Current Month/Day < Birth Month/Day). During lock, use age at Plan in Action Date (e.g., DOB 15/03/1970, Plan in Action Date 01/07/2025 → Age 55).
- **Category Assignment**: Map based on occupation, age, individual income, and dependents, fixed during lock.
- **Plan Lock**: Freeze profile, savings rate, and goals for three years. Allow savings increases by adjustment rate (or fallback rate in economic slowdown).
- **Profile Transitions**: On significant income changes (>10%) or post-lock, reassign profile (e.g., B8 to B7) with 6–12 month transition blending parameters (e.g., adjustment rate 3% to 2% → 2.5% for 6 months).
- **AI Integration**: Predict life events (e.g., job change, 60% probability) to adjust profiles proactively.
- **Compliance**: Log profile assignments and transitions in `financial_plans.audit_log` for SEBI audits.
- **Dynamic Queries**: Use category IDs in SQL/API calls (e.g., `SELECT goals FROM financial_goals WHERE category_id = 'B8'`).

**Combined Version Note**: Investors see profile ID (e.g., B8, “Mid-Career Family, high education focus”) in reports, with no access to predictive signals or profile editing.

---

### 4. Income Level Methodology for 2025
#### Overview
Income levels (Low, Sufficient, Good) are defined for White-Collar and Blue-Collar investors across life cycle stages for 2025, based on individual monthly income. Levels are fixed during the three-year plan lock, but income updates may trigger profile transitions.

#### Base Income Thresholds (Young Adult)
- **White-Collar**: Low < ₹1,000/day → ₹30,000/month.
- **Blue-Collar**: Low < ₹400/day → ₹12,000/month.

#### Progression Across Life Cycle Stages
The Low income threshold scales by 1.5 per stage:
- Young Family: Low = Young Adult Low × 1.5.
- Mid-Career Family: Low = Young Family Low × 1.5.
- Pre-Retirement: Low = Mid-Career Family Low × 1.5.
- Retirement: Low = Pre-Retirement Low.

#### Income Bands
- **White-Collar**:
  - Low: ₹0 – Low Upper Limit.
  - Sufficient: (Low Upper Limit + ₹1) – (Low Upper Limit × 2).
  - Good: > (Low Upper Limit × 2).
- **Blue-Collar**:
  - Low: ₹0 – Low Upper Limit.
  - Sufficient: (Low Upper Limit + ₹1) – (Low Upper Limit × 5/3).
  - Good: > (Low Upper Limit × 5/3).

#### Income Levels (2025)
**White-Collar**:
| Life Cycle Stage    | Income Level | Monthly Income Range (₹) |
|---------------------|--------------|--------------------------|
| Young Adult         | Low          | 0–30,000                 |
|                     | Sufficient   | 30,001–60,000            |
|                     | Good         | >60,000                  |
| Young Family        | Low          | 0–45,000                 |
|                     | Sufficient   | 45,001–90,000            |
|                     | Good         | >90,000                  |
| Mid-Career Family   | Low          | 0–67,500                 |
|                     | Sufficient   | 67,501–135,000           |
|                     | Good         | >135,000                 |
| Pre-Retirement      | Low          | 0–101,250                |
|                     | Sufficient   | 101,251–202,500          |
|                     | Good         | >202,500                 |
| Retirement          | Low          | 0–101,250                |
|                     | Sufficient   | 101,251–202,500          |
|                     | Good         | >202,500                 |

**Blue-Collar**:
| Life Cycle Stage    | Income Level | Monthly Income Range (₹) |
|---------------------|--------------|--------------------------|
| Young Adult         | Low          | 0–12,000                 |
|                     | Sufficient   | 12,001–20,000            |
|                     | Good         | >20,000                  |
| Young Family        | Low          | 0–18,000                 |
|                     | Sufficient   | 18,001–30,000            |
|                     | Good         | >30,000                  |
| Mid-Career Family   | Low          | 0–27,000                 |
|                     | Sufficient   | 27,001–45,000            |
|                     | Good         | >45,000                  |
| Pre-Retirement      | Low          | 0–40,500                 |
|                     | Sufficient   | 40,501–67,500            |
|                     | Good         | >67,500                  |
| Retirement          | Low          | 0–40,500                 |
|                     | Sufficient   | 40,501–67,500            |
|                     | Good         | >67,500                  |

#### Notes for Developers
- Retain income level during lock, even if income changes, unless profile transition is triggered.
- **AI Integration**: Validate income inputs (e.g., flag ₹1,00,000 for B8, suggest correction to ₹40,000) and predict income changes (e.g., promotion, 60% probability) for goal adjustments.
- Store income history in `investors.financial_history` for profile reassessments.

**Combined Version Note**: Investors view income level in reports (e.g., “B8, Sufficient Income”) but cannot modify inputs.

---

### 5. Investor Profiling and Data Collection
#### 5.1 Investor Profile and Risk Assessment Form
**Key Fields**:
- Name, Investor ID, DOB, Mobile Number, Email, Monthly Income, Spouse’s Income, Occupation, Urban/Rural Status, Dependents, Home Ownership, Rent Amount, EMI Amount, Current Emergency Fund, Risk Assessment Questions, Plan in Action Date, Economic Condition, Predictive Signals, Notification Consent.

**Progressive Onboarding**:
- Implement a step-by-step form, starting with essential fields (Name, DOB, Income, Occupation) and revealing others (e.g., Dependents) based on responses.
- UI: Wizard-style interface with collapsible sections, validated in real-time by AI.

**Enhanced AI Error Detection**:
- Flag subtle inconsistencies (e.g., ₹1,00,000 income for B1 profile, suggesting ₹12,000 with 85% confidence).
- Prompt: “Income seems high for Blue-Collar Young Adult. Verify or adjust.”
- Store in `investors.validation_results` (JSONB).

**Risk Scoring**:
- 5–10: Risk-Averse.
- 11–15: Moderate.
- 16–25: Aggressive.

**Privacy**:
- Use Investor ID in reports, mask sensitive data, encrypt per DPDP Act, log consent.

#### 5.2 Profile Assignment
- **Process**: Map investor data to one of 30 profiles based on occupation, age, individual monthly income, and dependents, fixed during plan lock.
- **Life Cycle Stages**:
  - Young Adult (22–30).
  - Young Family (28–35).
  - Mid-Career Family (35–50).
  - Pre-Retirement (50–60).
  - Retirement (60+).
- **Dependent Deductions**:
  - Calculate dependent age dynamically (Current Year – Birth Year – (1 if Current Month/Day < Birth Month/Day)).
  - During lock, use ages at Plan in Action Date.
  - Deduction rates: 1–5 years (5%), 6–10 years (7.5%), 11+ years (10%), capped at 30% of Household Income.
- **Example**: Priya Patel (age 45, Blue-Collar, ₹36,000/month, 2 dependents aged 8 and 10, Plan in Action Date 01/07/2025) → B8 (Mid-Career Family, Sufficient Income).

#### 5.3 Income Updates and Profile Transitions
**Mechanisms**:
- Annual Health Checks, Ad-Hoc Updates, CAS Triggers, Automated Triggers.

**Communication**:
- Notify profile transitions clearly:
  - English: “Profile changed to B7 due to higher LTI (33.78%). Consider value funds for stability.”
  - Hindi: “प्रोफाइल B7 में बदला गया क्योंकि LTI (33.78%) बढ़ा। स्थिरता के लिए वैल्यू फंड्स पर विचार करें।”
- Explain: “Value funds reduce risk during economic slowdowns.”

**AI Validation**:
- Cross-check income with economic indicators (e.g., GDP <4% prompts conservative adjustments).

**Storage**:
- **Current Income**: Update `investors.financial_details`.
- **Income History**: Log in `investors.financial_history`.
- **Metrics Recalculation**:
  - Loan-to-Income (LTI).
  - Disposable Income Ratio.
  - Emergency Fund Coverage.
- **Profile Transitions**:
  - Log in `investors.profile_history`.

**Compliance**:
- Encrypt income data per DPDP Act.
- Log updates in `financial_plans.audit_log`.

#### 5.4 Error Handling
**Enhanced AI Handling**:
- For invalid income: Suggest corrections based on profile norms and Economic Update data (e.g., “Income ₹1,00,000 invalid for B8; suggest ₹40,000 due to economic slowdown”).
- For duplicate mobile: AI suggests identity verification.

#### JSON Schema
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string", "example": "Priya Patel"},
    "investor_id": {"type": "string", "example": "INV-20250511-0002"},
    "dob": {"type": "string", "format": "date"},
    "financial_details": {
      "self_income": {"type": "number", "example": 27000},
      "spouse_income": {"type": "number", "example": 10000, "nullable": true},
      "total_household_income": {"type": "number", "example": 37000},
      "mobile_number": {"type": "string", "pattern": "^[6-9][0-9]{9}$", "example": "9876543210"},
      "email": {"type": "string", "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", "nullable": true, "example": "priya.patel@example.com"},
      "updated_date": {"type": "string", "format": "date", "example": "2025-05-11"},
      "notification_consent": {
        "sms_allowed": {"type": "boolean", "default": false},
        "email_allowed": {"type": "boolean", "default": false}
      }
    },
    "financial_history": {
      "type": "array",
      "items": {
        "self_income": {"type": "number"},
        "spouse_income": {"type": "number", "nullable": true},
        "total_household_income": {"type": "number"},
        "mobile_number": {"type": "string", "pattern": "^[6-9][0-9]{9}$"},
        "email": {"type": "string", "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", "nullable": true},
        "update_date": {"type": "string", "format": "date"},
        "source": {"type": "string", "enum": ["Investor", "MFD", "ITR", "CAS"]}
      }
    },
    "financial_metrics": {
      "lti": {"type": "number"},
      "disposable_income_ratio": {"type": "number"},
      "emergency_fund_coverage": {"type": "number"}
    },
    "profile_history": {
      "type": "array",
      "items": {
        "profile_id": {"type": "string"},
        "start_date": {"type": "string", "format": "date"},
        "end_date": {"type": "string", "format": "date", "nullable": true},
        "reason": {"type": "string"}
      }
    },
    "occupation": {"type": "string", "enum": ["White-Collar", "Blue-Collar"]},
    "urban_rural_status": {"type": "string", "enum": ["Urban", "Rural"]},
    "dependents": {
      "type": "array",
      "items": {
        "dob": {"type": "string", "format": "date"},
        "gender": {"type": "string", "enum": ["Male", "Female", "Other"]},
        "relation": {"type": "string", "enum": ["Son", "Daughter", "Minor Brother", "Minor Sister"]}
      }
    },
    "home_ownership": {"type": "boolean"},
    "rent_amount": {"type": "number", "minimum": 0},
    "emi_amount": {"type": "number", "minimum": 0},
    "emergency_fund": {"type": "number", "minimum": 0},
    "risk_assessment_score": {"type": "number", "minimum": 5, "maximum": 25},
    "plan_in_action_date": {"type": "string", "format": "date"},
    "lock_status": {"type": "boolean", "default": true},
    "economic_condition": {"type": "string", "enum": ["Normal", "Slowdown"], "default": "Normal"},
    "predictive_signals": {
      "family_planning": {"type": "string", "enum": ["Yes", "No", "Maybe"]},
      "job_stability": {"type": "string", "enum": ["Low", "Medium", "High"]}
    }
  },
  "required": ["name", "investor_id", "dob", "financial_details", "occupation", "urban_rural_status", "home_ownership", "rent_amount", "emi_amount", "plan_in_action_date", "financial_details.mobile_number"]
}
```

#### Notes for Developers
- Implement **Financial Details** tab for income updates.
- Add CAS parsing with `pdfplumber` (~95% accuracy).
- Ensure `plan_in_action_date` defaults to Plan Creation Date.
- Validate Disposable Income to prevent negative values.
- **AI Integration**:
  - Store validation results in `investors.validation_results`.
  - Use predictive signals for life event forecasting.
- **APIs**:
  - `POST /validate-inputs?investor_id=X`.
  - `POST /update-income?investor_id=X&self_income=Y&spouse_income=Z`.

**Combined Version Note**: Investors view validated data (e.g., “Income: ₹37,000, verified”) in reports but cannot edit or access predictive signals.

---

### 6. Financial Goals and Prioritization
#### Goal Identification and Prioritization
**Natural Language Input**:
- Allow free-text goal descriptions (e.g., “Save for child’s education”). NLP categorizes into types (Education, Retirement) and assigns timelines/amounts (e.g., Education: 7 years, ₹5,00,000).
- UI: Text box in **Goals** tab, processed via `POST /parse-goals` API.

**AI-Driven Adjustments**:
- Use Economic Update data (e.g., inflation >6%) to adjust goal amounts (e.g., increase Education target by 5%).
- Recommend value/dividend yield funds for short-term goals, contra funds for long-term goals during slowdowns.
- Store in `financial_plans.ai_recommendations`.

**Savings Capacity and Allocation**:
- **Household Income**: Monthly Income + Spouse’s Monthly Income.
- **Dependent Deduction**:
  - 1–5 years: 5% of Household Income.
  - 6–10 years: 7.5%.
  - 11+ years: 10%.
  - Capped at 30%.
- **Disposable Income**: Household Income – Rent – EMI – Dependent Deduction, capped at 70% to ensure living expenses.
- **Savings Calculation**:
  - Apply savings rate (Section 8).
  - Minimum: 10% of Household Income if Disposable Income > ₹0.
  - Round: Nearest ₹100 (<₹4,000), ₹500 (≥₹4,000).
- **Allocation**:
  - Prioritize Debt Reduction, Emergency Fund.
  - Allocate to goals via AI recommendations or default ratio (Education 45%, Marriage 35%, Retirement 20%).
  - Minimums: White-Collar ₹1,000/month, Blue-Collar ₹300/month per goal.
- **SIP Calculation**:
  - Use future value formula:
    \[
    FV = P \times \left( \frac{(1 + r)^n - 1}{r} \right) \times (1 + r)
    \]
    - \( FV \): Target amount (e.g., ₹5,00,000).
    - \( P \): Monthly savings.
    - \( r \): Monthly return rate (annual / 12).
    - \( n \): Months (timeline × 12).
  - Scenarios: Best-Case (upper return), Base-Case (midpoint), Worst-Case (lower return).
  - Example: Education (₹5,00,000, 7 years, Value Fund):
    - Base-Case (12% → 1%): ₹1,500/month.
    - Worst-Case (8% → 0.6667%): ₹1,700/month.
    - Best-Case (14% → 1.1667%): ₹1,400/month.

#### Investment Product Selection
- Debt Reduction: Ultra Short/Low Duration Funds (5.0–6.5%).
- Short-Term Goals: Dividend Yield/Value Funds (7.0–12.0%).
- Medium-Term Goals: Balanced Advantage/Value Funds (6.0–12.0%).
- Long-Term Goals: Contra/Multi Cap Funds (9.0–16.0%).
- Risk Adjustment:
  - Risk-Averse: Dividend Yield/Value Funds (worst-case).
  - Moderate: Balanced Advantage/Value Funds (base-case).
  - Aggressive: Contra/Multi Cap Funds (best-case).

#### Notes for Developers
- Store goals in `financial_plans.goals`:
  ```json
  {
    "goal_type": "Education",
    "amount": 500000,
    "timeline": 7,
    "sip": {
      "worst_case": 1700,
      "base_case": 1500,
      "best_case": 1400
    },
    "fund": "Value Fund",
    "ai_recommendation": {
      "priority": 1,
      "rationale": "High LTI limits savings",
      "confidence": 0.92
    }
  }
  ```
- **AI Integration**:
  - API: `POST /ai-prompt` for goal prioritization.
  - API: `POST /calculate-sip?goal_amount=X&timeline=Y&return_rate=Z`.

**Combined Version Note**: Investors see AI-adjusted goals in reports (e.g., “Education prioritized”).

---

### 7. Specific Financial Goals
#### Goal Types and Parameters
| Goal            | Timeline       | Target Amount (₹, 2025) | Priority Factors                     |
|-----------------|----------------|-------------------------|--------------------------------------|
| Debt Reduction  | 3–5 years      | Varies (EMI reduction)  | EMI >20% Household Income            |
| Emergency Fund  | 1–3 years      | 3–6 months expenses     | Income stability, dependents         |
| Education       | 3–15 years     | 5,00,000–20,00,000      | Child’s age, urban/rural status      |
| Home Purchase   | 5–10 years     | 4,00,000–20,00,000      | Home ownership, income level         |
| Marriage        | 5–15 years     | 5,00,000–15,00,000      | Child’s age, cultural expectations   |
| Retirement      | 10–30 years    | 50,00,000–2,00,00,000   | Age, income, existing savings        |
| Self-Education  | 1–5 years      | 1,00,000–5,00,000       | Career stage, income level           |

#### Adjustments
- **Urban/Rural**: Rural goals 20–30% lower.
- **Income Level**: Higher income targets upper amounts.
- **AI Integration**: Adjust goals based on predictive insights (e.g., delay Marriage) and economic indicators (e.g., inflation >6%).

#### Notes for Developers
- Fix timelines using dependent ages at Plan in Action Date.
- Store in `financial_plans.goals`.

**Combined Version Note**: Investors see goal details in reports (e.g., “Marriage delayed to 2029”).

---

### 8. Recommended Savings Rates for Investors
#### Slab Structure
**Blue-Collar**:
| Disposable Income (₹) | Savings Rate (%) | Rural (+3%) |
|-----------------------|------------------|-------------|
| ≤15,000               | 10               | 13          |
| 15,001–25,000         | 15               | 18          |
| 25,001–30,000         | 20               | 23          |
| >30,000               | 25               | 28          |

**White-Collar**:
| Disposable Income (₹) | Savings Rate (%) | Rural (+3%) |
|-----------------------|------------------|-------------|
| ≤15,000               | 15               | 18          |
| 15,001–30,000         | 17               | 20          |
| 30,001–45,000         | 20               | 23          |
| >45,000               | 25               | 28          |

#### Modifiers
- Home Ownership: +2%.
- No EMI: +1%.
- Education/Marriage Goals Completed: +1% per dependent (max +3%).
- Spouse Income Ratio:
  - White-Collar: <20% (+0.5%), 20–50% (+1%), >50% (+2%).
  - Blue-Collar: <20% (+0.3%), 20–50% (+0.7%), >50% (+1%).

#### Calculation Logic
1. Calculate Household Income: Investor + Spouse Income.
2. Dependent Deduction: Capped at 30%.
3. Disposable Income: Household Income – Rent – EMI – Deduction, capped at 70%.
4. Savings Rate: Apply slab rate, add modifiers.
5. Savings:
   - Disposable Income × Rate, minimum 10% Household Income.
   - Increase annually by adjustment rate (or fallback in economic slowdown).
   - Round: Nearest ₹100 (<₹4,000), ₹500 (≥₹4,000).
6. Output:
   - Savings Amount (₹).
   - Blended Rate: Savings / Household Income × 100.
   - Feasibility Index: \( \frac{\text{Disposable Income} - \text{Savings}}{\text{Disposable Income}} \times 100 \).

#### Example: Priya Patel (B8, Urban, 2025)
- Household Income: ₹37,000 (₹27,000 self, ₹10,000 spouse).
- Deduction: 2 dependents (8y, 10y) → 2 × 10% × ₹37,000 = ₹7,400.
- Disposable Income: ₹37,000 – ₹12,000 (rent) – ₹12,500 (EMI) – ₹7,400 = ₹5,100.
- Savings Rate: 10% (≤₹15,000) + 1% (spouse 20–50%) = 11%.
- Savings: ₹5,100 × 11% = ₹561 → ₹3,700 (10% × ₹37,000).
- Blended Rate: ₹3,700 / ₹37,000 = 10%.
- Feasibility Index: \( \frac{5,100 - 3,700}{5,100} \times 100 = 27.45\% \).

#### Notes for Developers
- API: `POST /calculate-savings?disposable_income=X&urban_rural=Y`.

**Combined Version Note**: Investors see savings in reports (e.g., “₹3,700/month, 27.45% feasible”).

---

### 9. Annual Savings Adjustment Rates
#### Adjustment Rates
| Profile ID | Base Rate (%) | Fallback Rate (%) | Conditions           |
|------------|---------------|-------------------|----------------------|
| W1         | 7             | 3.5               | Economic Slowdown    |
| W2         | 6             | 3.0               | Economic Slowdown    |
| W3         | 5             | 2.5               | Economic Slowdown    |
| W4         | 6             | 3.0               | Economic Slowdown    |
| W5         | 5             | 2.5               | Economic Slowdown    |
| W6         | 4             | 2.0               | Economic Slowdown    |
| W7         | 5             | 2.5               | Economic Slowdown    |
| W8         | 4             | 2.0               | Economic Slowdown    |
| W9         | 3             | 1.5               | Economic Slowdown    |
| W10        | 4             | 2.0               | Economic Slowdown    |
| W11        | 3             | 1.5               | Economic Slowdown    |
| W12        | 2             | 1.0               | Economic Slowdown    |
| W13        | 3             | 1.5               | Economic Slowdown    |
| W14        | 2             | 1.0               | Economic Slowdown    |
| W15        | 1             | 0.5               | Economic Slowdown    |
| B1         | 3             | 1.5               | Economic Slowdown    |
| B2         | 3             | 1.5               | Economic Slowdown    |
| B3         | 2             | 1.0               | Economic Slowdown    |
| B4         | 3             | 1.5               | Economic Slowdown    |
| B5         | 3             | 1.5               | Economic Slowdown    |
| B6         | 2             | 1.0               | Economic Slowdown    |
| B7         | 2             | 1.0               | Economic Slowdown    |
| B8         | 3             | N/A               | N/A                  |
| B9         | 2             | 1.0               | Economic Slowdown    |
| B10        | 2             | 1.0               | Economic Slowdown    |
| B11        | 2             | 1.0               | Economic Slowdown    |
| B12        | 1             | 0.5               | Economic Slowdown    |
| B13        | 2             | 1.0               | Economic Slowdown    |
| B14        | 1             | 0.5               | Economic Slowdown    |
| B15        | 1             | 0.5               | Economic Slowdown    |

#### Modifiers
- Home Ownership: +0.5%.
- No EMI: +0.5%.
- Education/Marriage Completed: +0.5% per dependent (max +1.5%).
- Rural: +0.5%.
- Economic Slowdown: Triggered by Economic Update indicators (e.g., GDP <4%), applies fallback rates for low-income profiles (W1, W4, W7, W10, W13, B1, B4, B7, B10, B13).

**Notes**:
- Notify: “Economic slowdown (GDP <4%) sets savings rate to 1.0%. Consider value funds.”
- API: `POST /set-economic-mode?investor_id=X&mode=economic_slowdown`.

---

### 10. Emergency Fund Requirements
#### Calculation
- Essential Expenses: Household Income – Savings.
- Target: 3 months (low income), 4.5 months (sufficient), 6 months (good).
- AI adjusts based on job stability (e.g., 6 months for low stability) and economic indicators (e.g., unemployment >5%).

#### Notes for Developers
- Store in `financial_plans.goals`.

**Combined Version Note**: Investors see details in reports (e.g., “₹50,000, 2 years”).

---

### 11. Risk Tolerance Assessment
#### 11.1 Overview
Assesses risk via a five-question survey (scored 1–5 each, total 5–25), enhanced with dynamic scoring and stress testing.

#### 11.2 AI Integration
- Validates risk inputs (e.g., flags Aggressive for B7, suggests Moderate).
- Stores in `investors.validation_results`.

#### 11.3 Dynamic Risk Scoring
**Economic Adjustments**:
- Economic Slowdown (GDP <4%): -3 points.
- High Inflation (>6%): -2 points.

**Components**:
- **Baseline Score**: Survey (5–25).
- **Goal-Specific Adjustments**:
  - Short-term goals (<3 years): -2 points.
  - High LTI (>25%): -3 points.
  - Income drop (>10%): -2 points.
- **Behavioral Adjustments (CAS, Optional)**:
  - ≥3 missed SIPs: -2 points.
  - ≥1 unplanned redemption: -3 points.
  - ≥2 lumpsums/year: +2 points.
- **Total Score**: 0–25 (Risk-Averse: 0–10, Moderate: 11–15, Aggressive: 16–25).

**Process**:
- Recalculate scores using Economic Update data (e.g., slowdown shifts Priya’s score from 12 to 7).
- UI: “New Score: 7 (Risk-Averse). Recommend dividend yield funds?”
- Tamil: “புதிய மதிப்பீடு: 7 (இடர்-வெறுப்பு). டிவிடெண்ட் யீல்ட் நிதிகள் பரிந்துரைக்கப்படுகின்றனவா?”

#### 11.4 Stress Testing
**Scenarios**:
- Income drop (20%), market downturn (-30%), economic slowdown (GDP <4%).
- Example: Priya’s Education SIP: ₹1,500 (base) → ₹1,800 (worst-case, slowdown).

**Output**:
- Recommend value/dividend yield funds for stability, contra funds for recovery scenarios.
- Store in `investors.risk_adjustment_log`.

#### 11.5 Historical Risk Score Tracking
- Store in `investors.risk_adjustment_log`:
  ```json
  {
    "type": "array",
    "items": {
      "score": {"type": "number", "example": 7},
      "rating": {"type": "string", "example": "Risk-Averse"},
      "adjustment_date": {"type": "string", "format": "date"},
      "factors": {"type": "array", "example": ["Income Drop", "LTI", "Economic Slowdown"]},
      "confidence": {"type": "number", "example": 0.95}
    }
  }
  ```

#### 11.6 Error Handling
- **Inconsistent Risk Score**:
  - Error: “Score 20 inconsistent for B7 (high LTI).”
  - Resolution: AI suggests 10; MFD adopts.
- **Missing Survey**:
  - Error: “Risk questions incomplete.”
  - Resolution: Use default (Moderate, 12).
- **Flowchart**:
  ```mermaid
  graph TD
      A[Start: Collect Survey] --> B{All Questions Answered?}
      B -- Yes --> C[Calculate Baseline Score]
      B -- No --> D[Error: Missing Answers]
      D --> E[Use Default Score: 12]
      C --> F[Apply Adjustments]
      F --> G{Valid Score?}
      G -- Yes --> H[Store Score]
      G -- No --> I[Error: Inconsistent]
      I --> J[AI Suggests Score]
      J --> K[MFD Adopts]
  ```

#### Notes for Developers
- API: `POST /calculate-risk-score?investor_id=X`.

**Combined Version Note**: Investors see risk profile in reports (e.g., “Risk-Averse, Score 7”).

---

### 12. Indicative Returns of Mutual Fund Schemes
#### Returns Table
| Scheme                    | Return Range (%) | Base-Case (%) |
|---------------------------|------------------|---------------|
| Overnight Fund            | 4.0–5.0          | 4.5           |
| Ultra Short Duration Fund | 5.0–6.0          | 5.5           |
| Low Duration Fund         | 5.5–6.5          | 6.0           |
| Short Duration Fund       | 6.0–7.0          | 6.5           |
| Debt Fund                 | 5.5–6.5          | 6.0           |
| Large Cap Fund            | 8.0–12.0         | 10.0          |
| Multi Cap Fund            | 10.0–14.0        | 12.0          |
| Balanced Advantage Fund   | 7.0–11.0         | 9.0           |
| Hybrid Equity Fund        | 8.0–12.0         | 10.0          |
| Value Fund                | 10.0–14.0        | 12.0          |
| Dividend Yield Fund       | 8.0–11.0         | 9.5           |
| Contra Fund               | 12.0–16.0        | 14.0          |

#### AI Integration
- Refine returns using market trends and Economic Update data (e.g., 80% confidence for 12% Value Fund during slowdown).

#### Notes for Developers
- API: `GET /fund-returns?scheme=X&scenario=S`.

**Combined Version Note**: Investors see ranges in reports (e.g., “Value Fund: 10–14%”).

---

### 13. Mutual Fund Investment Options Based on Goals
#### Overview
Investment options are mapped to risk profiles and goals, updated to include value, dividend yield, and contra funds for economic slowdowns.

#### Updated Fund Options
| Fund Type                | Risk Profile       | Expected Returns (Normal) | Expected Returns (Slowdown) | Suitable Goals                     |
|--------------------------|--------------------|---------------------------|-----------------------------|------------------------------------|
| Value Fund               | Risk-Averse, Moderate | 10–14%                    | 8–12%                       | Debt Reduction, Emergency Fund, Education, Home Purchase, Marriage |
| Dividend Yield Fund      | Risk-Averse        | 8–11%                     | 7–10% (3–5% dividends)      | Debt Reduction, Emergency Fund, Self-Education |
| Contra Fund              | Moderate, Aggressive | 12–16%                    | 9–13% (12–15% post-recovery)| Retirement, Marriage, Education    |
| Multi Cap Fund           | Moderate, Aggressive | 10–14%                    | 8–12%                       | Retirement, Education              |
| Balanced Advantage Fund  | Risk-Averse, Moderate | 7–11%                     | 6–9%                        | Home Purchase, Marriage            |
| Ultra Short Duration Fund| Risk-Averse        | 5–6.5%                    | 4.5–6%                      | Emergency Fund, Self-Education     |

**Notes**:
- **Value Funds**: Invest in undervalued stocks with strong fundamentals, ideal for stability during slowdowns (GDP <4%).
- **Dividend Yield Funds**: Focus on high-dividend companies, providing income for short-term goals.
- **Contra Funds**: Target out-of-favor sectors, suitable for long-term goals with recovery potential.
- **Economic Slowdown Adjustments**: Shift allocations to value/dividend yield funds for Risk-Averse profiles, contra funds for Aggressive profiles post-slowdown.
- **API**: `POST /recommend-funds?investor_id=X&economic_condition=slowdown`.

**Example**:
- Priya (B7, Risk-Averse):
  - Debt Reduction: 50% Dividend Yield Fund (₹1,850/month).
  - Emergency Fund: 30% Dividend Yield, 20% Value Fund (₹1,110 + ₹740/month).
  - Education: 50% Value Fund (₹1,500/month).

#### Notes for Developers
- Store in `financial_plans.investment_recommendations`.

**Combined Version Note**: Investors see allocations in reports.

---

### 14. Plan Lock Mechanism
#### Overview
Locks plan for three years from Plan in Action Date, allowing savings adjustments.

#### Locked Elements
- Profile, savings rate, goals, investment recommendations, adjustment rate.

#### Adjustments
- Increase savings/SIPs annually by adjustment rate (or fallback in economic slowdown).
- Optional dynamic adjustments based on Economic Update data, controlled by MFDs.

#### Unlock Conditions
- Investor/MFD request.
- Feasibility Index < -10%.
- Income drop >20%.

#### Notes for Developers
- API: `POST /unlock-plan?investor_id=X&reason=Y`.

**Combined Version Note**: Investors see lock status in reports.

---

### 15. Feasibility Analysis
#### Calculation
- Feasibility Index = \( \frac{\text{Disposable Income} - \text{Savings}}{\text{Disposable Income}} \times 100 \).
- Categories: >80% (Highly Feasible), 20–80% (Moderately), <20% (Adjust if < -10%).

#### Adjustments
- Unlock plan, extend timelines, reduce amounts, or reallocate savings.

#### Notes for Developers
- API: `GET /feasibility?plan_id=X`.

**Combined Version Note**: Investors see Index in reports.

---

### 16. Annual Health Checks
#### 16.1 Overview
Assess plan alignment annually without altering locked structure unless necessary, incorporating version control, triggers, and backward compatibility.

#### 16.2 Components
- Recalculate Feasibility Index, goal progress, risk scores.
- Detect life changes (e.g., income drop >10%, new dependents).
- Use Economic Update data to assess slowdown impacts.
- AI predicts life events (e.g., job change, 60% probability).

**Economic Integration**:
- Fetch GDP, IIP, CPI from Economic Update to adjust recommendations (e.g., suggest value funds if GDP <4%).
- API: `GET /economic-indicators`.

**Reminders**:
- Notify: “Annual health check due in 30 days. We’ll review goals and economic conditions.”
- Bengali: “বার্ষিক স্বাস্থ্য পরীক্ষা ৩০ দিনের মধ্যে। আমরা আপনার লক্ষ্য এবং অর্থনৈতিক অবস্থা পর্যালোচনা করব।”

#### 16.3 Version Control for Annual Updates
- **Process**:
  - Plans reference versioned income bands (e.g., 2025 bands).
  - MFDs toggle: “Use Latest Bands (2025)” or “Retain Original (e.g., 2024)”.
- **Storage**: In `financial_plans`:
  ```json
  {
    "income_band_version": {"type": "string", "example": "2025"}
  }
  ```

#### 16.4 Automated Update Triggers
- **Triggers**:
  - Income Change: >10%.
  - LTI Change: >5%.
  - CAS Patterns: ≥3 missed SIPs, ≥1 unplanned redemption.
  - Life Events: New dependent, loan repayment.
- **UI**: Flag in **Investor Selection Panel**: “Reassessment Recommended”.

#### 16.5 Backward Compatibility
- Use default bands (2025) if latest bands unavailable.
- Notify MFD: “Using default income bands.”

#### 16.6 Error Handling
- **Missing Update Data**:
  - Error: “Income update missing.”
  - Resolution: Prompt MFD to collect.
- **Invalid Metrics**:
  - Error: “Feasibility Index < -10%.”
  - Resolution: Unlock plan.

#### Notes for Developers
- Schedule checks annually from Plan in Action Date.
- **APIs**:
  - `POST /health-check?plan_id=X`.
  - `POST /reassess-plan?investor_id=X&version=Y`.

**Combined Version Note**: Investors receive updated reports post-checks.

---

### 17. App Integration Logic Flow
#### 17.1 Data Collection
Collect personal, financial, risk, income, and predictive signals data via the app.

#### 17.2 Real-Time Validation
**Implementation**:
- Validate inputs with AI, using Economic Update data (e.g., flag savings > income during slowdown).
- Alerts: “Savings ₹5,000 exceeds disposable income in slowdown; adjust to ₹3,700?”

#### 17.3 Scenario Analysis Tool
**Implementation**:
- Add sliders for slowdown scenarios (e.g., GDP <4%, inflation >6%).
- Example: “If GDP drops to 3%, emergency fund lasts 5 months with dividend yield funds.”
- Visuals: Bar charts (Chart.js) showing goal impacts.

#### 17.4 AI API Resilience
- Cache precomputed AI insights in `financial_plans.ai_cache`.
- Fallback: Use default recommendations.
- Notify MFD: “AI unavailable; using cached insights.”

#### 17.5 Plan Generation and UI/UX
**UI Enhancements**:
- **Personalized Dashboards**: Show savings allocation (e.g., “50% Dividend Yield Fund”), goal progress, and Economic Update highlights (e.g., “GDP: 4.2%, declining”).
- **Mobile Optimization**: Responsive design, touch-friendly, <2s load times.
- **Educational Content**: Videos/articles in **Learn** tab (e.g., “Value Funds in Economic Slowdowns”).
- **AI Chatbot**: Answers “What’s a value fund?” or “How’s the economy?” using Economic Update data.
- **Simplified Language**: Use “stable funds” for value/dividend yield funds, with tooltips (e.g., “Value Fund: Stocks with strong value, low risk”).
- **What’s New Section**: Highlights “Added Value Funds for slowdown protection.”
- **Accessibility**: High-contrast text, ARIA labels, multilingual support.

**APIs**:
- `POST /generate-dashboard?investor_id=X`.
- `POST /chatbot-query?investor_id=X&query=Y`.

#### 17.6 Error Handling
- **API Failure**:
  - Error: “AI API unavailable.”
  - Resolution: Use cached insights.
- **Invalid Inputs**:
  - Error: “Negative Disposable Income” or “Invalid mobile number.”
  - Resolution: Adjust inputs.
- **Flowchart**:
  ```mermaid
  graph TD
      A[Start: Data Input] --> B{Valid Inputs?}
      B -- Yes --> C[Call AI API]
      B -- No --> D[Error: Invalid Input]
      D --> E[Show Alert]
      E --> F[MFD Adjusts]
      C --> G{API Success?}
      G -- Yes --> H[Generate Plan]
      G -- No --> I[Use Cached Insights]
      I --> H
  ```

**Combined Version Note**: Investors access read-only portal.

---

**End of Part 1**

*Part 2 covers communication, economic updates, MFD guidance, data storage, and additional components.*