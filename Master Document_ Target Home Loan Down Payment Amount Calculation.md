# Master Document: Target Home Loan Down Payment Amount Calculation

## Introduction and Purpose
This master document outlines the methodology for calculating the **Target Home Loan Down Payment Amount** for investors across 30 distinct profiles, as defined in the Investor Profiles Master (artifact_id: eb700d53-f04c-4e8e-bc63-e40fcaaf0639). It builds upon the Home Loan Borrowing Timeline Framework (artifact_id: 5230e4c9-067b-4050-a2fb-023f6a95786e), which determines the optimal number of years until an investor is ready to borrow for a home purchase. The down payment calculation is a critical component of financial planning, representing the initial capital required to secure a home loan, with the remainder financed through the loan itself.

The purpose of this document is to provide a standardized, data-driven approach to estimate the down payment amount, ensuring alignment with each investor's financial context, life cycle stage, and borrowing timeline. This framework supports an intuitive app that dynamically calculates the target down payment based on investor data, empowering users to plan effectively for home ownership.

## Key Variables
- **Current Monthly Income**: Representative income within profile ranges (e.g., W8: ₹1,00,000).
- **Annual Income Growth Rate**:
  - White-Collar: Low (-): 5%, Sufficient (0): 7%, Good (+): 9%
  - Blue-Collar: Low (-): 4%, Sufficient (0): 5%, Good (+): 6.5%
- **Borrowing Timeline and Tenure**: From Home Loan Borrowing Timeline Framework, capped at age 55 for a minimum 10-year tenure.
- **Future Monthly Income**:
  ```
  Future Income = Current Income × (1 + Growth Rate)^Timeline
  ```
- **Maximum EMI**: 50% of future monthly income.
- **EMI per Lakh** (9% interest, varies by tenure):
  - 20 years: ₹900
  - 18 years: ₹956
  - 17 years: ₹974
  - 16 years: ₹993
  - Computed dynamically using:
    ```
    EMI = [1,00,000 × (0.09/12) × (1 + 0.09/12)^n] / [(1 + 0.09/12)^n - 1], n = tenure in months
    ```
- **Loan Amount**:
  ```
  Loan Amount = Max EMI / EMI per Lakh × 1,00,000
  ```
- **Home Value**:
  ```
  Home Value = Loan Amount / 0.85
  ```
- **Down Payment**: 15% of Home Value.
- **Investment Return**: 10.75% annually for savings.
- **Savings Capacity**: White-Collar: 20–30%, Blue-Collar: 10–15%.

## Methodology
1. **Determine Typical Age**:
   - Young Adult: 25
   - Young Family: 30
   - Mid-Career Family: 40
   - Pre-Retirement: 55
   - Retirement: 65
2. **Assign Current Income**: Use representative values within profile ranges (see below).
3. **Fetch Timeline and Tenure**: From Home Loan Borrowing Timeline Framework, using midpoint of adjusted timeline range.
4. **Calculate Borrowing Age**:
   ```
   Borrowing Age = Typical Age + Timeline
   ```
5. **Project Future Income**:
   ```
   Future Income = Current Income × (1 + Growth Rate)^Timeline
   ```
6. **Calculate Max EMI**: 50% × Future Income.
7. **Determine EMI per Lakh**: Based on tenure.
8. **Calculate Loan Amount, Home Value, Down Payment**:
   ```
   Loan Amount = Max EMI / EMI per Lakh × 1,00,000
   Home Value = Loan Amount / 0.85
   Down Payment = Home Value × 0.15
   ```
9. **Estimate Annual Savings**:
   ```
   PMT = (Down Payment × 0.1075) / [(1.1075)^Timeline - 1]
   ```
10. **Feasibility Check**:
    - If Borrowing Age > 55, mark as infeasible.
    - If monthly savings > 20% of savings capacity, suggest extending timeline, reducing home value, or increasing down payment to 20%.

## Representative Incomes
- **White-Collar**:
  - Young Adult: W1: ₹20,000, W2: ₹45,000, W3: ₹80,000
  - Young Family: W4: ₹30,000, W5: ₹67,500, W6: ₹120,000
  - Mid-Career Family: W7: ₹45,000, W8: ₹100,000, W9: ₹180,000
  - Pre-Retirement: W10: ₹60,000, W11: ₹150,000, W12: ₹250,000
  - Retirement: W13: ₹60,000, W14: ₹150,000, W15: ₹250,000
- **Blue-Collar**:
  - Young Adult: B1: ₹8,000, B2: ₹16,000, B3: ₹25,000
  - Young Family: B4: ₹12,000, B5: ₹24,000, B6: ₹40,000
  - Mid-Career Family: B7: ₹18,000, B8: ₹36,000, B9: ₹60,000
  - Pre-Retirement: B10: ₹25,000, B11: ₹50,000, B12: ₹80,000
  - Retirement: B13: ₹25,000, B14: ₹50,000, B15: ₹80,000

## Down Payment Targets for All 30 Profiles
The table below uses the midpoint of adjusted timeline ranges from the Home Loan Borrowing Timeline Framework (artifact_id: 5230e4c9-067b-4050-a2fb-023f6a95786e), with tenure derived as min(20, 65 - Borrowing Age). White-Collar growth rates are 5%/7%/9%.

| Category ID | Life Cycle Stage       | Typical Age | Income (₹/month) | Timeline (Years) | Borrowing Age | Tenure (Years) | Down Payment (₹) | Annual Savings (₹) |
|-------------|------------------------|-------------|------------------|------------------|---------------|----------------|------------------|-------------------|
| W1          | Young Adult            | 25          | 20,000           | 10.2             | 35.2          | 20             | 3,79,394         | 13,364            |
| W2          | Young Adult            | 25          | 45,000           | 8.5              | 33.5          | 20             | 9,07,242         | 37,242            |
| W3          | Young Adult            | 25          | 80,000           | 7.65             | 32.65         | 20             | 17,11,774        | 84,462            |
| W4          | Young Family           | 30          | 30,000           | 9.6              | 39.6          | 20             | 4,95,652         | 24,440            |
| W5          | Young Family           | 30          | 67,500           | 8.5              | 38.5          | 20             | 11,31,781        | 55,803            |
| W6          | Young Family           | 30          | 120,000          | 8.1              | 38.1          | 20             | 19,57,304        | 96,494            |
| W7          | Mid-Career Family      | 40          | 45,000           | 7.2              | 47.2          | 17             | 5,24,515         | 53,806            |
| W8          | Mid-Career Family      | 40          | 100,000          | 7                | 47            | 18             | 13,66,036        | 139,879           |
| W9          | Mid-Career Family      | 40          | 180,000          | 6.3              | 46.3          | 18             | 26,51,984        | 306,832           |
| W10         | Pre-Retirement         | 55          | 60,000           | 0.6              | 55.6          | 10             | Infeasible       | N/A               |
| W11         | Pre-Retirement         | 55          | 150,000          | 0.5              | 55.5          | 10             | Infeasible       | N/A               |
| W12         | Pre-Retirement         | 55          | 250,000          | 0.45             | 55.45         | 10             | Infeasible       | N/A               |
| W13         | Retirement             | 65          | 60,000           | 0                | 65            | 0              | Infeasible       | N/A               |
| W14         | Retirement             | 65          | 150,000          | 0                | 65            | 0              | Infeasible       | N/A               |
| W15         | Retirement             | 65          | 250,000          | 0                | 65            | 0              | Infeasible       | N/A               |
| B1          | Young Adult            | 25          | 8,000            | 13.75            | 38.75         | 20             | 1,89,027         | 5,599             |
| B2          | Young Adult            | 25          | 16,000           | 8.5              | 33.5          | 20             | 3,95,723         | 11,719            |
| B3          | Young Adult            | 25          | 25,000           | 7.65             | 32.65         | 20             | 7,42,413         | 21,985            |
| B4          | Young Family           | 30          | 12,000           | 11.1             | 41.1          | 20             | 2,21,737         | 8,704             |
| B5          | Young Family           | 30          | 24,000           | 8.5              | 38.5          | 20             | 4,63,519         | 18,199            |
| B6          | Young Family           | 30          | 40,000           | 8.1              | 38.1          | 20             | 8,78,876         | 34,507            |
| B7          | Mid-Career Family      | 40          | 18,000           | 8.7              | 48.7          | 16             | 2,92,189         | 14,452            |
| B8          | Mid-Career Family      | 40          | 36,000           | 7                | 47            | 18             | 5,84,378         | 28,904            |
| B9          | Mid-Career Family      | 40          | 60,000           | 6.3              | 46.3          | 18             | 11,05,735        | 54,697            |
| B10         | Pre-Retirement         | 55          | 25,000           | 0.8              | 55.8          | 10             | Infeasible       | N/A               |
| B11         | Pre-Retirement         | 55          | 50,000           | 0.5              | 55.5          | 10             | Infeasible       | N/A               |
| B12         | Pre-Retirement         | 55          | 80,000           | 0.45             | 55.45         | 10             | Infeasible       | N/A               |
| B13         | Retirement             | 65          | 25,000           | 0                | 65            | 0              | Infeasible       | N/A               |
| B14         | Retirement             | 65          | 50,000           | 0                | 65            | 0              | Infeasible       | N/A               |
| B15         | Retirement             | 65          | 80,000           | 0                | 65            | 0              | Infeasible       | N/A               |

**Notes**:
- **Timelines**: Midpoint of adjusted ranges from Home Loan Borrowing Timeline Framework (e.g., W8: 2–12 years → 7 years).
- **Tenure**: Derived as min(20, 65 - Borrowing Age), ensuring ≥10 years.
- **Infeasible Cases**: Pre-Retirement (W10–W12, B10–B12) and Retirement profiles are infeasible if Borrowing Age > 55.
- **High-Debt**: Assumed for B1, B4, B7, B8, B10.

## Example Calculation: W8 (Mid-Career Family, Sufficient, White-Collar)
- **Typical Age**: 40
- **Income**: ₹1,00,000/month
- **Growth Rate**: 7%
- **Timeline**: 7 years (midpoint of 2–12)
- **Borrowing Age**: 40 + 7 = 47
- **Tenure**: min(20, 65 - 47) = 18 years
- **Future Income**: ₹1,00,000 × (1.07)^7 ≈ ₹1,60,578
- **Max EMI**: 50% × ₹1,60,578 = ₹80,289
- **EMI per Lakh (18 years)**: ≈ ₹956
- **Loan Amount**: ₹80,289 / ₹956 × 1,00,000 ≈ ₹83,94,560
- **Home Value**: ₹83,94,560 / 0.85 ≈ ₹98,75,953
- **Down Payment**: ₹98,75,953 × 0.15 ≈ ₹14,81,393
- **Annual Savings**:
  ```
  PMT = (14,81,393 × 0.1075) / [(1.1075)^7 - 1] ≈ 1,59,250 / 0.987 ≈ ₹1,61,347
  ```

## Handling Infeasible Scenarios
- **Borrowing Age > 55**: Suggest savings, smaller properties, or rental.
- **High Savings Requirement**: If savings > 20% of capacity, recommend:
  - Extend timeline by 1–2 years (if Borrowing Age ≤ 55).
  - Reduce home value by 10–20%.
  - Increase down payment to 20%.

## App Integration Notes
- **Input Data**: Fetch category ID, age, income, loan repayment, timeline, and tenure from investor data and Home Loan Borrowing Timeline Framework.
- **Logic**:
  - Compute future income, loan amount, home value, and down payment.
  - Check feasibility against savings capacity and tenure.
- **Output**:
  - "Target Home Value: ₹X lakh, Down Payment: ₹Y lakh, Save ₹Z/month over T years."
  - Alerts: "Borrowing at age 55 allows only 10 years tenure."
- **Features**:
  - Custom inputs for income or home value.
  - Scenario analysis for timeline adjustments.

## Conclusion
This document provides a dynamic, profile-specific approach to calculate the Target Home Loan Down Payment Amount, using White-Collar growth rates (5%/7%/9%) and timelines from the Home Loan Borrowing Timeline Framework. It ensures feasibility by capping borrowing at age 55, supporting an intuitive app for effective home ownership planning.