# Master for Annual Savings Adjustment Rates (Updated for 30 Investor Profiles)

This master defines profile-specific annual adjustment rates for savings amounts, reflecting expected income growth and inflation for each of the 30 standard investor profiles. Rates are tailored to occupation, life cycle stage, and income level (as defined in `Investor_Profiles_Master_Updated.markdown` and `income_level_master_2025.md`). Modifiers based on home ownership, borrowing status, dependents’ goal completion, and spouse’s income are applied to these base rates. After each adjustment, savings are rounded: to the nearest ₹100 if less than ₹4,000, and to the nearest ₹500 if ₹4,000 or more.

## Annual Savings Adjustment Rates for Investor Profiles

| Profile ID | Life Cycle Stage       | Income Level (Sufficiency) | Monthly Income Range (₹)      | Proposed Annual Adjustment Rate (%) | Rationale                                                                 |
|------------|------------------------|----------------------------|-----------------------------|-------------------------------------|---------------------------------------------------------------------------|
| **W1**     | Young Adult            | Low (-)                    | 0 - 30,000                  | 7%                                  | Adapted from original Young Adult Low; reflects slower growth for low-income young professionals. |
| **W2**     | Young Adult            | Sufficient (0)             | 30,001 - 60,000             | 8%                                  | Adapted from original Young Adult Medium; standard rate for moderate growth. |
| **W3**     | Young Adult            | Good (+)                   | > 60,000                    | 9%                                  | Adapted from original Young Adult High; for rapid career progression. |
| **W4**     | Young Family           | Low (-)                    | 0 - 45,000                  | 6%                                  | Slightly lower than Young Adult Low due to increased family responsibilities. |
| **W5**     | Young Family           | Sufficient (0)             | 45,001 - 90,000             | 7%                                  | Slightly lower than Young Adult Sufficient due to increased family responsibilities. |
| **W6**     | Young Family           | Good (+)                   | > 90,000                    | 8%                                  | Slightly lower than Young Adult Good due to increased family responsibilities. |
| **W7**     | Mid-Career Family      | Low (-)                    | 0 - 67,500                  | 4%                                  | Adapted from original Mid-Career Low; reflects slower growth and family expenses. |
| **W8**     | Mid-Career Family      | Sufficient (0)             | 67,501 - 135,000            | 5%                                  | Adapted from original Mid-Career Medium; standard rate for stable income growth. |
| **W9**     | Mid-Career Family      | Good (+)                   | > 135,000                   | 6%                                  | Adapted from original Mid-Career High; for continued growth in high-income roles. |
| **W10**    | Pre-Retirement         | Low (-)                    | 0 - 101,250                 | 4%                                  | Adapted from original Pre-Retirement Low; to encourage retirement savings without strain. |
| **W11**    | Pre-Retirement         | Sufficient (0)             | 101,251 - 202,500           | 5%                                  | Adapted from original Pre-Retirement Medium; to boost retirement savings. |
| **W12**    | Pre-Retirement         | Good (+)                   | > 202,500                   | 6%                                  | Adapted from original Pre-Retirement High; to maximize savings. |
| **W13**    | Retirement             | Low (-)                    | 0 - 101,250                 | 0%                                  | Focus on preservation/decumulation, not accumulation. |
| **W14**    | Retirement             | Sufficient (0)             | 101,251 - 202,500           | 0%                                  | Focus on preservation/decumulation. |
| **W15**    | Retirement             | Good (+)                   | > 202,500                   | 0%                                  | Focus on preservation/decumulation. |
| **B1**     | Young Adult            | Low (-)                    | 0 - 12,000                  | 3%                                  | Adapted from original Young Adult Low; low rate for limited growth and tight budgets. |
| **B2**     | Young Adult            | Sufficient (0)             | 12,001 - 20,000             | 4%                                  | Adapted from original Young Adult Medium; to encourage saving as income stabilizes. |
| **B3**     | Young Adult            | Good (+)                   | > 20,000                    | 5%                                  | Adapted from original Young Adult High; moderate rate for better growth potential. |
| **B4**     | Young Family           | Low (-)                    | 0 - 18,000                  | 2.5%                                | Slightly lower than Young Adult Low due to increased family responsibilities. |
| **B5**     | Young Family           | Sufficient (0)             | 18,001 - 30,000             | 3.5%                                | Slightly lower than Young Adult Sufficient due to increased family responsibilities. |
| **B6**     | Young Family           | Good (+)                   | > 30,000                    | 4.5%                                | Slightly lower than Young Adult Good due to increased family responsibilities. |
| **B7**     | Mid-Career Family      | Low (-)                    | 0 - 27,000                  | 2%                                  | Adapted from original Mid-Career Low; minimal rate due to limited growth and family responsibilities. |
| **B8**     | Mid-Career Family      | Sufficient (0)             | 27,001 - 45,000             | 3%                                  | Adapted from original Mid-Career Medium; low rate to ensure feasibility. |
| **B9**     | Mid-Career Family      | Good (+)                   | > 45,000                    | 4%                                  | Adapted from original Mid-Career High; for better income stability. |
| **B10**    | Pre-Retirement         | Low (-)                    | 0 - 40,500                  | 2%                                  | Adapted from original Pre-Retirement Low; minimal rate as growth is limited. |
| **B11**    | Pre-Retirement         | Sufficient (0)             | 40,501 - 67,500             | 3%                                  | Adapted from original Pre-Retirement Medium; low rate to prioritize retirement savings. |
| **B12**    | Pre-Retirement         | Good (+)                   | > 67,500                    | 4%                                  | Adapted from original Pre-Retirement High; moderate rate to encourage increased savings. |
| **B13**    | Retirement             | Low (-)                    | 0 - 40,500                  | 0%                                  | Focus on preservation/decumulation. |
| **B14**    | Retirement             | Sufficient (0)             | 40,501 - 67,500             | 0%                                  | Focus on preservation/decumulation. |
| **B15**    | Retirement             | Good (+)                   | > 67,500                    | 0%                                  | Focus on preservation/decumulation. |

## Adjustment Rate Modifiers
Adjust annual adjustment rates based on the following conditions (cumulative):
- **Home Ownership = Yes and Not Paying Rent**: +1% to adjustment rate.
- **No Loans (Monthly Loan Repayment = 0)**: +0.5% to adjustment rate.
- **Education/Marriage Goals Completed** (per dependent, e.g., daughter’s DOB 10/05/2000 → Age 25 as of 08/05/2025, education funded): +0.5% to adjustment rate.
- **Spouse Income (Spouse-to-Investor Income Ratio)**:
  - **White-Collar**:
    - Ratio < 20%: +0.2%.
    - Ratio 20%–50%: +0.5%.
    - Ratio > 50%: +1%.
  - **Blue-Collar**:
    - Ratio < 20%: +0.1%.
    - Ratio 20%–50%: +0.2%.
    - Ratio > 50%: +0.5%.

### Example for Pre-Retirement, Low Income (Profile W10 or B10)
This example uses a hypothetical White-Collar investor (W10) with a base rate of 4%.
- **Baseline (W10)**: 4%.
- **With Modifiers** (Home Ownership = Yes, No Rent, No Loans, Daughter’s Education Completed, Spouse Income ₹50,000, Investor Income for W10 could be e.g. ₹80,000):
  - Daughter’s DOB: 10/05/2000 → Age = 2025 - 2000 = 25 years (as of 08/05/2025), education completed.
  - Spouse-to-Investor Income Ratio: ₹50,000 / ₹80,000 = 62.5% → +1% (White-Collar).
  - Total Modifiers: +1% (Home Ownership) + 0.5% (No Loans) + 0.5% (Education Completed) + 1% (Spouse Income) = +3%.
  - Adjusted Rate for W10: 4% + 3% = 7%.

## Implementation Notes
- **Dynamic Application**: Derive the investor’s age from DOB (dd/mm/yyyy format) as of 08/05/2025. Derive dependents’ ages from their DOBs as of 08/05/2025 to determine goal completion. Apply the rate corresponding to the investor's Profile ID (W1-W15, B1-B15) and then apply modifiers based on home ownership, borrowing status, dependents’ goal status, and spouse’s income.
- **Rounding**: After adjustment:
  - Nearest ₹100 if < ₹4,000.
  - Nearest ₹500 if ≥ ₹4,000.
- **Example**:
  - Investor Profile W10, with an adjusted rate of 7% and current savings of ₹28,000:
    - Year 1: ₹28,000.
    - Year 2: ₹28,000 × 1.07 = ₹29,960 → ₹30,000 (nearest ₹500).
- **Customization**: Adjust rates further based on individual factors (e.g., promotions) during consultations.

## Conclusion
This updated master provides annual savings adjustment rates for all 30 standard investor profiles. It derives dependents’ ages from their DOBs for accurate assessment of goal completion for adjustment rate modifiers and incorporates spouse’s income alongside other factors to create tailored rates. This structure ensures comprehensive coverage and alignment with the `Investor_Profiles_Master_Updated.markdown`.
