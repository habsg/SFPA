# Master for Allocation for Education of Dependents

## Purpose
This document outlines the funding strategy for dependents’ education expenses (Class 11/12 and 4-year undergraduate degree) for all dependents (sons, daughters, minor siblings), regardless of gender. It uses the Urban/Rural Status from the `Investor Profile and Risk Assessment Form` to adjust costs, with rural expenses ~40% lower.

## Scope
- **Target Dependents**: All dependents listed in the `Investor Profile and Risk Assessment Form` (artifact ID: `94a08765-01b9-4a51-a160-68d1a21591f6`).
- **Education Levels**: Class 11/12 (2 years), 4-year graduation (e.g., B.Tech, BA, B.Com).
- **Integration**: Aligns with `Master Document: Mutual Fund Investment Options Based on Goals`, `Master Document: Indicative Returns of Mutual Fund Schemes`, and `Application Logic Documentation for Financial Planning.md`.

## Education Funding Framework

### 1. Data Collection
- **Inputs**:
  - **Dependent’s Age**: From DOB (dd/mm/yyyy) in the `Investor Profile and Risk Assessment Form`, calculate age as of 09/05/2025.
  - **Relation**: Son, daughter, minor brother/sister (from Gender and context).
  - **Investor Profile**: W1–W15 (White-Collar) or B1–B15 (Blue-Collar).
  - **Urban/Rural Status**: From `urban_rural` field (Urban/Rural dropdown).
- **Timeline Calculation**:
  - Class 11/12: Starts at age 16 (2 years, e.g., 2027–2029 if age 14 in 2025).
  - Graduation: Starts at age 18 (4 years, e.g., 2029–2033).
  - Example: Dependent DOB 10/05/2011 → Age 14 in 2025 → Class 11/12 in 2027, Graduation in 2029.

### 2. Target Amounts
- **Base Costs (2025, Urban)**:
  - **Class 11/12 (2 years)**: ₹1,00,000 (₹50,000/year, covering tuition, books, coaching).
  - **Graduation (4 years)**: ₹4,00,000 (₹1,00,000/year, covering tuition, hostel, expenses).
- **Rural Adjustment**: 40% lower.
  - Class 11/12: ₹60,000 (₹30,000/year).
  - Graduation: ₹2,40,000 (₹60,000/year).
- **Inflation Adjustment**: Apply 5% annual inflation from 2025 to the start year.
  - Formula: Adjusted Cost = Base Cost × (1 + 0.05)^(Start Year – 2025).
  - Example: Urban Graduation starting 2029 (4 years away) → ₹4,00,000 × 1.05^4 = ₹4,86,202 (rounded to ₹4,86,200).
- **Total Cost per Dependent**:
  - Urban: ₹1,00,000 (Class 11/12) + ₹4,00,000 (Graduation) = ₹5,00,000 (before inflation).
  - Rural: ₹60,000 + ₹2,40,000 = ₹3,00,000 (before inflation).

### 3. Savings Allocation
- **Allocation Rule**:
  - Education is a medium-term goal (3–7 years) unless timeline < 3 years (then short-term), per `Application Logic Documentation for Financial Planning.md`.
  - Allocate savings after Debt Reduction and Emergency Fund, using the 45/35/20 ratio (45% to Education) when data is incomplete or timelines are long.
  - For multiple dependents, sum adjusted costs and calculate total monthly savings needed.
- **Monthly Savings Calculation**:
  - Use future value formula: Monthly Savings = FV × (r/m) / [(1 + r/m)^(n×m) – 1], where FV = Adjusted Cost, r = Expected return, n = Years to start, m = 12.
  - Example: Urban Graduation, ₹4,86,200 in 2029, 7.7% return (Hybrid Fund), 4 years:
    - Monthly Savings = ₹4,86,200 × (0.077/12) / [(1 + 0.077/12)^(4×12) – 1] ≈ ₹8,900.
- **Minimum Allocation**:
  - White-Collar: ₹1,000/month or 10% of ideal savings per dependent.
  - Blue-Collar: ₹300/month or 10% of ideal savings per dependent.

### 4. Investment Options
- **Fund Selection**:
  - **Timeline < 3 years**: Ultra Short Duration Funds (6%).
  - **Timeline 3–7 years**: Debt-Oriented Hybrid Funds (7.7%) or Large Cap Equity Funds (9.9%).
  - **Timeline > 7 years**: Multi Cap Funds (12%) for Aggressive investors.
- **Risk Profile**:
  - Risk-Averse: Prioritize Debt or Conservative Hybrid Funds.
  - Moderate: Balance Hybrid and Large Cap Funds.
  - Aggressive: Include Multi Cap Funds for longer timelines.
- **Example**: W5 investor, 5-year timeline, Moderate risk: 50% Hybrid Fund (7.7%), 50% Large Cap Fund (9.9%).

### 5. Reporting
- **Investor Guide**: List Education per dependent in goals table, with target year, amount, and monthly savings.
- **Year-Wise Investment Objectives**: Show yearly savings and growth for each dependent’s education.
- **AI Insights**: Prompt: “For a W5 investor with two dependents aged 14 and 12, highlight education funding risks.” Output: “Limited savings capacity may delay funding for the second dependent’s graduation.”

## Conclusion
This master ensures equitable education funding for all dependents, with urban/rural adjustments based on the `Investor Profile and Risk Assessment Form`. It supports the 30 investor profiles and balances education with other financial goals.