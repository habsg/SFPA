# Home Loan Borrowing Timeline Framework

## Purpose
This document provides a logical and analytical framework to determine the **timeline of borrowing** for a home loan (years until an investor is ready to borrow and purchase a home) for each of the 30 investor profiles (artifact_id: eb700d53-f04c-4e8e-bc63-e40fcaaf0639). It incorporates practical constraints from Indian banking policies, ensuring timelines are feasible given a maximum repayment age of 65 and a maximum tenure of 20 years. The framework caps borrowing at age 55 to guarantee at least a 10-year loan tenure and excludes retirement goal planning for investors above age 55. It supports an intuitive app to dynamically assign timelines based on life cycle stage, income sufficiency, debt levels, and competing goals.

## Rationale: Report on Home Loan Age Limits and Borrowing Methodology in India
- **Maximum Age for Home Loans**: Fixed at 65 years. Loans must be repaid by age 65.
- **Loan Tenure**: Capped at 20 years. For individuals aged 46 and above, tenure is 65 minus borrowing age; for those 45 and below, tenure is 20 years. Borrowing age is capped at 55 to ensure a minimum 10-year tenure.
- **Gender Treatment**: No differential age limits; special schemes for women (e.g., lower interest rates) do not affect tenure.
- **Tenure Table**:

| Borrowing Age | Maximum Tenure (Years) |
|---------------|------------------------|
| 30            | 20                     |
| 35            | 20                     |
| 40            | 20                     |
| 45            | 20                     |
| 46            | 19                     |
| 47            | 18                     |
| 48            | 17                     |
| 49            | 16                     |
| 50            | 15                     |
| 51            | 14                     |
| 52            | 13                     |
| 53            | 12                     |
| 54            | 11                     |
| 55            | 10                     |
| >55           | Not feasible (minimum 10-year tenure required) |

- **Practical Concern**: Borrowing after age 55 yields tenures <10 years, which is impractical. Timelines are adjusted to cap borrowing age at 55, ensuring sufficient repayment periods.

## Methodology
The timeline is determined by targeting a borrowing age range for each life cycle stage, adjusted for income sufficiency, debt, and competing goals, with a cap at age 55 to ensure a minimum 10-year tenure. Retirement goals are excluded for investors above age 55.

### Key Variables
- **Target Borrowing Age Range** (adjusted to cap at 55):
  - Young Adult (22–30): 32–35 years
  - Young Family (28–35): 35–40 years
  - Mid-Career Family (35–50): 40–50 years
  - Pre-Retirement (50–55): 50–55 years
  - Retirement (60+): Not feasible (borrowing age > 55)
- **Income Sufficiency** (per artifact_id: eb700d53-f04c-4e8e-bc63-e40fcaaf0639):
  - Low (-): Delay borrowing (increase timeline by 20%)
  - Sufficient (0): No change
  - Good (+): Accelerate borrowing (decrease timeline by 10%)
- **Loan-to-Income Ratio**:
  - High-debt (>20%): Delay borrowing by 20–50%
- **Competing Goals** (per artifact_id: 762c4d72-5c98-4adf-8f77-f045f6533d7b):
  - Add 1–3 years for Debt Reduction, Education, Marriage priorities (exclude Retirement for age > 55)

### Assignment Steps
1. **Calculate Base Timeline**:
   - For a given age, base timeline = max(0, Target Age Lower - Age) to min(Target Age Upper - Age, 55 - Age)
   - If Age ≥ 55, timeline = 0 (borrow immediately or not feasible)
2. **Adjust for Sufficiency**:
   - Low (-): Multiply timeline by 1.2
   - Good (+): Multiply timeline by 0.9
3. **Adjust for High-Debt**: If debt >20%, multiply timeline by 1.35 (midpoint of 20–50%)
4. **Adjust for Competing Goals**:
   - Add 1–3 years for Debt Reduction, Education, Marriage based on life cycle stage
   - Exclude Retirement goals for age > 55
5. **Feasibility Check**:
   - If Borrowing Age > 55, indicate "Not feasible"
   - If Borrowing Age = 55, note "Minimum 10-year tenure available"

## Profile-Specific Timelines
Timelines are calculated for typical ages in each stage, with adjustments. For precise calculations, use the app with specific investor data.

| Category ID | Life Cycle Stage       | Typical Age | Base Timeline (Years) | Adjusted Timeline (Years) | Notes (High-Debt, Goals) |
|-------------|------------------------|-------------|-----------------------|---------------------------|--------------------------|
| W1          | Young Adult            | 25          | 7–10                  | 8.4–12 (Low, +20%)        | -                        |
| W2          | Young Adult            | 25          | 7–10                  | 7–10                      | -                        |
| W3          | Young Adult            | 25          | 7–10                  | 6.3–9 (Good, -10%)        | -                        |
| W4          | Young Family           | 30          | 5–10                  | 7.2–12 (Low, +20%, +1 Education) | Education               |
| W5          | Young Family           | 30          | 5–10                  | 6–11 (Sufficient, +1 Education) | Education              |
| W6          | Young Family           | 30          | 5–10                  | 5.4–10.8 (Good, -10%, +1 Education) | Education          |
| W7          | Mid-Career Family      | 40          | 0–10                  | 2.4–12 (Low, +20%, +2 Education/Marriage) | Education, Marriage |
| W8          | Mid-Career Family      | 40          | 0–10                  | 2–12 (Sufficient, +2 Education/Marriage) | Education, Marriage |
| W9          | Mid-Career Family      | 40          | 0–10                  | 1.8–10.8 (Good, -10%, +2 Education/Marriage) | Education, Marriage |
| W10         | Pre-Retirement         | 55          | 0                    | 0–1.2 (Low, +20%, +1 Marriage) | Marriage, Retirement excluded |
| W11         | Pre-Retirement         | 55          | 0                    | 0–1 (Sufficient, +1 Marriage) | Marriage, Retirement excluded |
| W12         | Pre-Retirement         | 55          | 0                    | 0–0.9 (Good, -10%, +1 Marriage) | Marriage, Retirement excluded |
| W13         | Retirement             | 65          | 0                    | 0 (Not feasible)          | Suggest alternatives     |
| W14         | Retirement             | 65          | 0                    | 0 (Not feasible)          | Suggest alternatives     |
| W15         | Retirement             | 65          | 0                    | 0 (Not feasible)          | Suggest alternatives     |
| B1          | Young Adult            | 25          | 7–10                  | 11.3–16.2 (Low, +20%, High-debt +35%) | High-debt likely  |
| B2          | Young Adult            | 25          | 7–10                  | 7–10                      | -                        |
| B3          | Young Adult            | 25          | 7–10                  | 6.3–9 (Good, -10%)        | -                        |
| B4          | Young Family           | 30          | 5–10                  | 8.7–13.5 (Low, +20%, +1 Education, High-debt +35%) | Education, High-debt |
| B5          | Young Family           | 30          | 5–10                  | 6–11 (Sufficient, +1 Education) | Education           |
| B6          | Young Family           | 30          | 5–10                  | 5.4–10.8 (Good, -10%, +1 Education) | Education       |
| B7          | Mid-Career Family      | 40          | 0–10                  | 3.2–14.2 (Low, +20%, +2 Education/Marriage, High-debt +35%) | Education, Marriage, High-debt |
| B8          | Mid-Career Family      | 40          | 0–10                  | 2–12 (Sufficient, +2 Education/Marriage) | Education, Marriage, High-debt |
| B9          | Mid-Career Family      | 40          | 0–10                  | 1.8–10.8 (Good, -10%, +2 Education/Marriage) | Education, Marriage |
| B10         | Pre-Retirement         | 55          | 0                    | 0–1.6 (Low, +20%, +1 Marriage, High-debt +35%) | Marriage, Retirement excluded, High-debt |
| B11         | Pre-Retirement         | 55          | 0                    | 0–1 (Sufficient, +1 Marriage) | Marriage, Retirement excluded |
| B12         | Pre-Retirement         | 55          | 0                    | 0–0.9 (Good, -10%, +1 Marriage) | Marriage, Retirement excluded |
| B13         | Retirement             | 65          | 0                    | 0 (Not feasible)          | Suggest alternatives     |
| B14         | Retirement             | 65          | 0                    | 0 (Not feasible)          | Suggest alternatives     |
| B15         | Retirement             | 65          | 0                    | 0 (Not feasible)          | Suggest alternatives     |

**Notes**:
- **High-Debt**: Assumed for Blue-Collar Low-income profiles (B1, B4, B7, B10, B13), extending timelines by 35%.
- **Goal Adjustments**: Education and Marriage delays are added; Retirement goals excluded for age > 55.
- **Retirement Profiles**: Borrowing not feasible post-55; app suggests savings or rental options.

## Notes for App Developers
- **Input Data**: Fetch age, occupation, income, loan repayment, dependents from investor profile data (artifact_id: 91228f9a-35a0-4524-a828-0272c1c8b96c).
- **Logic**:
  - Determine life cycle stage and category ID
  - Calculate base timeline: max(0, Target Age Lower - Age) to min(Target Age Upper - Age, 55 - Age)
  - Adjust for sufficiency, debt, and goals (exclude Retirement for age > 55)
  - If Borrowing Age > 55, display "Not feasible with current plan"
  - If Borrowing Age = 55, display "Minimum 10-year tenure available"
- **Output**:
  - "Plan to borrow in X years (20XX), with Y years tenure"
  - Example: For a 40-year-old B8, timeline 7 years → "Borrow in 7 years (2032), with 18 years tenure"
- **Features**:
  - Timeline slider with warnings (e.g., "Borrowing at age 55 allows only 10 years tenure")
  - Goal conflict alerts (e.g., "Education savings may delay borrowing")

## Conclusion
This framework ensures borrowing timelines are practical, adhering to India’s home loan age limit of 65, a maximum tenure of 20 years, and a borrowing age cap at 55 for a minimum 10-year tenure. Retirement goals are excluded for investors above 55, aligning with financial planning priorities. It provides a clear methodology for assigning timelines, enabling an intuitive app to guide investors effectively.