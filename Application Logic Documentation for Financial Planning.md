# Application Logic Documentation for Financial Planning

## 1. Introduction
This document outlines the core logic used by the financial planning application to generate personalized financial plans for investors. It details investor profiling, goal prioritization, savings assessment, and investment allocation, based on master documents and user-provided data.

## 2. Investor Profiling and Initial Data Collection
1. **Data Collection**: Investor data is collected using the `Investor Profile and Risk Assessment Form` (artifact ID: `94a08765-01b9-4a51-a160-68d1a21591f6`).
2. **Profile ID Assignment**: Based on Occupation, Age (from DOB), Monthly Income, and Dependents, map to one of 30 profiles (W1–W15, B1–B15) in `Investor_Profiles_Master_Updated.markdown`.
3. **Urban/Rural Status**: Use `urban_rural` field to adjust costs for education, marriage, and retirement goals.
4. **Risk Profile Assessment**: Risk score (5–25) determines Risk-Averse, Moderate, or Aggressive profile.
5. **Financial Goals Identification**: Retrieve standard goals, amounts, and timelines from `Master_Document_Financial_Goals_by_Investor_Profile_Aligned.markdown` and new masters (`Master for Debt Reduction Plan`, `Master for Allocation for Education of Dependents`, `Master for Allocation for Marriage (of Daughters)`, `Master for Allocation towards Retirement Fund`).

## 3. Goal Prioritization Logic
The application prioritizes goals based on urgency, essential nature, and data availability:
1. **Debt Reduction (Highest Priority)**:
   - **Trigger**: Loan-to-Income Ratio (LTI) > 20%, per `Master for Debt Reduction Plan`.
   - **Objective**: Reduce LTI to ≤ 10% within 3–5 years.
   - **Action**: Allocate 50% of Total Monthly Savings (or more) until target is met. Use Ultra Short/Low Duration Funds.
2. **Emergency Fund**:
   - **Objective**: Build 3–6 months of expenses, per `Master Emergency Fund Requirement Document`.
   - **Action**: Prioritized after Debt Reduction, ensuring liquidity.
3. **Other Goals (Education, Marriage, Retirement, Home Purchase, Self-Education)**:
   - **Context**: When data is complete (e.g., dependents’ ages from `DOB and Gender of Dependents`, urban/rural from `urban_rural`), prioritize based on timeline and urgency:
     - **Short-Term (< 3 years)**: High priority (e.g., Education for a 16-year-old dependent).
     - **Medium-Term (3–7 years)**: Moderate priority (e.g., Home Purchase, Self-Education).
     - **Long-Term (> 7 years)**: Lower priority (e.g., Retirement, Marriage for young daughters).
   - **Incomplete Data or Long Timelines**: When dependent data is missing or timelines are long (> 7 years), allocate remaining savings after Debt Reduction and Emergency Fund in a 45/35/20 ratio:
     - **Education (45%)**: Per `Master for Allocation for Education of Dependents`, assuming 1–2 dependents if none specified.
     - **Marriage (35%)**: Per `Master for Allocation for Marriage (of Daughters)`, assuming 1 daughter if none specified.
     - **Retirement (20%)**: Per `Master for Allocation towards Retirement Fund`.
   - **Self-Education**: For Young Adult investors (22–28), per `Self-Education Goal Mechanism`, prioritize as short/medium-term if specified by MFD.
   - **Home Purchase**: Per `Target Home Loan Down Payment Amount Calculation`, typically medium/long-term.

## 4. Savings Capacity Assessment and Allocation
1. **Calculate Disposable Income**: 
   - Disposable Income = Monthly Income – Monthly Loan Repayment.
2. **Determine Applicable Savings Rate**: 
   - Base rate from `Recommended Savings Rates Master for Investors_Updated.markdown`.
   - Adjustments from `Master for Annual Savings Adjustment Rates_Updated.markdown` (e.g., +1% for home ownership).
3. **Calculate Total Monthly Savings**: 
   - Total Monthly Savings = Disposable Income × Adjusted Savings Rate.
4. **Allocate Savings to Prioritized Goals**: 
   - Start with Debt Reduction (50% if LTI > 20%), then Emergency Fund.
   - For Education, Marriage, Retirement (incomplete data/long timelines):
     - Allocate 45% to Education, 35% to Marriage, 20% to Retirement.
     - Example: W5 investor, ₹2,000 remaining savings after Debt Reduction/Emergency Fund:
       - Education: ₹2,000 × 45% = ₹900.
       - Marriage: ₹2,000 × 35% = ₹700.
       - Retirement: ₹2,000 × 20% = ₹400.
   - For specific goals (e.g., Education for a 14-year-old), calculate monthly savings using future value formula and allocate directly.
5. **Minimum Allocation Rule**:
   - **White-Collar**: ₹1,000/month or 10% of ideal savings per goal.
   - **Blue-Collar**: ₹300/month or 10% of ideal savings per goal.
   - Scale down primary goal (e.g., Debt Reduction) if needed to meet minimums, extending timelines.

## 5. Investment Product Selection
- Select funds per `Master Document: Mutual Fund Investment Options Based on Goals` and `Master Document: Indicative Returns of Mutual Fund Schemes`, adjusted by risk profile:
  - **Debt Reduction**: Ultra Short/Low Duration Funds (6–7.7%).
  - **Education (Short/Medium-Term)**: Debt-Oriented Hybrid or Large Cap Funds (7.7–9.9%).
  - **Marriage/Retirement (Long-Term)**: Multi Cap or Balanced Advantage Funds (10–12%).
- Example: W5 investor, Moderate risk, 5-year Education goal: 50% Hybrid Fund (7.7%), 50% Large Cap Fund (9.9%).

## 6. Output Generation
- **Year-Wise Investment Objectives**: Details savings and investments per goal (`Master_Document_Year_Wise_Investment_Objectives_Aligned.markdown`).
- **Goal Comparison Document**: Compares ideal vs. achievable goals, noting 45/35/20 allocations for uncertain goals.
- **Returns and Asset Allocation Comparison Document**: Compares required vs. expected returns.

## 7. AI Augmentation
- Per `Use of AI by the App.markdown`, AI provides narrative insights (e.g., risks of high LTI delaying Education funding), validated against app logic.

## 8. Review and Updates
- Review annually to align with market conditions, regulatory changes, and new master documents. Updated to include `urban_rural` field for cost adjustments.