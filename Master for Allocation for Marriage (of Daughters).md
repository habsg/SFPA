# Master for Allocation for Marriage (of Daughters)

## Purpose
This document defines the funding strategy for marriage expenses of daughters, based on their ages from the `Investor Profile and Risk Assessment Form`. It uses the Urban/Rural Status to adjust costs and aligns with the 30 investor profiles in `Investor_Profiles_Master_Updated.markdown`.

## Scope
- **Target Dependents**: Daughters listed in the `Investor Profile and Risk Assessment Form` (artifact ID: `94a08765-01b9-4a51-a160-68d1a21591f6`), identified by DOB and Gender (Female).
- **Goal**: Fund marriage expenses (e.g., ceremony, dowry, gifts).
- **Integration**: Aligns with `Master Document: Mutual Fund Investment Options Based on Goals`, `Master Document: Indicative Returns of Mutual Fund Schemes`, and `Application Logic Documentation for Financial Planning.md`.

## Marriage Funding Framework

### 1. Data Collection
- **Inputs**:
  - **Daughter’s Age**: From DOB in the `Investor Profile and Risk Assessment Form`, calculate age as of 09/05/2025.
  - **Investor Profile**: W1–W15 or B1–B15.
  - **Urban/Rural Status**: From `urban_rural` field (Urban/Rural dropdown).
- **Timeline Calculation**:
  - Default marriage age: 25 (adjustable by MFD, range: 21–30).
  - Example: Daughter DOB 10/05/2011 → Age 14 in 2025 → Marriage in 2036 (age 25).

### 2. Target Amounts
- **Base Costs (2025)**:
  - **Urban**:
    - White-Collar: ₹5,00,000 (covering ceremony, jewelry, gifts).
    - Blue-Collar: ₹3,00,000 (simpler ceremonies).
  - **Rural**: 40% lower.
    - White-Collar: ₹3,00,000.
    - Blue-Collar: ₹1,80,000.
- **Inflation Adjustment**: 5% annually.
  - Formula: Adjusted Cost = Base Cost × (1 + 0.05)^(Target Year – 2025).
  - Example: Urban White-Collar, ₹5,00,000 in 2036 (11 years) → ₹5,00,000 × 1.05^11 = ₹8,55,258 (rounded to ₹8,55,300).

### 3. Savings Allocation
- **Allocation Rule**:
  - Marriage is a long-term goal (>7 years) unless timeline < 7 years (then medium-term).
  - Allocate 35% of remaining savings (after Debt Reduction, Emergency Fund) per the 45/35/20 ratio when data is incomplete.
- **Monthly Savings Calculation**:
  - Example: Urban White-Collar, ₹8,55,300 in 2036, 12% return (Multi Cap Fund), 11 years:
    - Monthly Savings = ₹8,55,300 × (0.12/12) / [(1 + 0.12/12)^(11×12) – 1] ≈ ₹2,600.
- **Minimum Allocation**:
  - White-Collar: ₹1,000/month or 10% of ideal savings per daughter.
  - Blue-Collar: ₹300/month or 10% of ideal savings per daughter.

### 4. Investment Options
- **Fund Selection**:
  - **Timeline < 7 years**: Debt-Oriented Hybrid Funds (7.7%) or Large Cap Funds (9.9%).
  - **Timeline ≥ 7 years**: Multi Cap Funds (12%) or Balanced Advantage Funds (10%).
- **Risk Profile**:
  - Risk-Averse: Prioritize Hybrid or Balanced Funds.
  - Moderate: Mix Large Cap and Multi Cap Funds.
  - Aggressive: Emphasize Multi Cap Funds.
- **Example**: B6 investor, 10-year timeline, Aggressive risk: 70% Multi Cap Fund (12%), 30% Balanced Advantage Fund (10%).

### 5. Reporting
- **Investor Guide**: Include Marriage per daughter in goals table, with target year, amount, and savings.
- **Year-Wise Investment Objectives**: Show yearly savings and growth.
- **AI Insights**: Prompt: “For a B6 investor with a daughter aged 14, highlight marriage funding risks.” Output: “Long timeline increases market risk; consider balanced funds for stability.”

## Conclusion
This master ensures daughters’ marriage expenses are planned effectively, with urban/rural adjustments based on the `Investor Profile and Risk Assessment Form`, supporting balanced financial planning.