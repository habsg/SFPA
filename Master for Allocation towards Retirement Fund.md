# Master for Allocation towards Retirement Fund

## Purpose
This document defines the strategy for funding retirement for the 30 investor profiles, tailored to life cycle stages. It uses the Urban/Rural Status from the `Investor Profile and Risk Assessment Form` to adjust costs and integrates with the financial planning app’s logic.

## Scope
- **Target Investors**: All profiles (W1–W15, B1–B15), with active savings for non-Retirement profiles (W1–W12, B1–B12).
- **Data Source**: `Investor Profile and Risk Assessment Form` for age, income, risk profile, and urban/rural status.
- **Integration**: Aligns with `Master for Annual Savings Adjustment Rates_Updated.markdown`, `Master Document: Mutual Fund Investment Options Based on Goals`, and `Application Logic Documentation for Financial Planning.md`.

## Retirement Funding Framework

### 1. Data Collection
- **Inputs**:
  - **Investor Age**: From DOB, calculate age as of 09/05/2025.
  - **Profile ID**: Determines life cycle stage and income level.
  - **Urban/Rural Status**: From `urban_rural` field (Urban/Rural dropdown).
- **Timeline Calculation**:
  - Default retirement age: 60 (adjustable by MFD, range: 55–65).
  - Example: Investor DOB 10/05/1980 → Age 45 in 2025 → Retirement in 2035 (age 60).

### 2. Target Amounts
- **Base Costs (2025, Urban)**:
  - **White-Collar**:
    - Young Adult/Mid-Career: ₹75,00,000 (25 years of expenses at ₹25,000/month, post-inflation).
    - Pre-Retirement: ₹50,00,000 (20 years at ₹20,833/month).
  - **Blue-Collar**:
    - Young Adult/Mid-Career: ₹50,00,000 (25 years at ₹16,667/month).
    - Pre-Retirement: ₹30,00,000 (20 years at ₹12,500/month).
- **Rural Adjustment**: 40% lower.
  - White-Collar: ₹45,00,000 (Young Adult/Mid-Career), ₹30,00,000 (Pre-Retirement).
  - Blue-Collar: ₹30,00,000 (Young Adult/Mid-Career), ₹18,00,000 (Pre-Retirement).
- **Inflation Adjustment**: 5% annually to retirement year.
  - Example: Urban White-Collar, ₹75,00,000 in 2035 (10 years) → ₹75,00,000 × 1.05^10 = ₹1,22,16,872 (rounded to ₹1,22,16,900).

### 3. Savings Allocation
- **Allocation Rule**:
  - Retirement is a long-term goal (>10 years for Young Adult/Mid-Career, 5–10 years for Pre-Retirement).
  - Allocate 20% of remaining savings (after Debt Reduction, Emergency Fund) per the 45/35/20 ratio when data is incomplete.
- **Monthly Savings Calculation**:
  - Example: Urban White-Collar, ₹1,22,16,900 in 2035, 12% return (Multi Cap Fund), 10 years:
    - Monthly Savings = ₹1,22,16,900 × (0.12/12) / [(1 + 0.12/12)^(10×12) – 1] ≈ ₹4,600.
- **Minimum Allocation**:
  - White-Collar: ₹1,000/month or 10% of ideal savings.
  - Blue-Collar: ₹300/month or 10% of ideal savings.

### 4. Investment Options
- **Fund Selection**:
  - **Timeline 5–10 years**: Balanced Advantage Funds (10%) or Large Cap Funds (9.9%).
  - **Timeline > 10 years**: Multi Cap Funds (12%) or Equity-Oriented Hybrid Funds (10.5%).
- **Risk Profile**:
  - Risk-Averse: Prioritize Balanced or Hybrid Funds.
  - Moderate: Mix Large Cap and Multi Cap Funds.
  - Aggressive: Emphasize Multi Cap Funds.
- **Example**: W9 investor, 15-year timeline, Moderate risk: 60% Multi Cap Fund (12%), 40% Balanced Advantage Fund (10%).

### 5. Reporting
- **Investor Guide**: Include Retirement in goals table, with target year, amount, and savings.
- **Year-Wise Investment Objectives**: Show yearly savings and growth.
- **AI Insights**: Prompt: “For a W9 investor aged 40, highlight retirement funding risks.” Output: “Market volatility may affect long-term returns; diversify with balanced funds.”

## Conclusion
This master ensures retirement planning is tailored to life cycle stages, with urban/rural adjustments based on the `Investor Profile and Risk Assessment Form`, supporting long-term financial security.