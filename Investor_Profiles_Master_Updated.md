# Investor Profiles Master (Updated)

## Purpose
This document defines 30 investor profiles for White-Collar and Blue-Collar investors, categorized by life cycle stages and income levels, to standardize references across financial planning documents (e.g., communication framework, financial goals master). Each profile is assigned a unique category ID (W for White-Collar, B for Blue-Collar) to facilitate dynamic content generation and ensure consistency. Profiles align with life cycle stages from artifact_id: c4f92cd3-14c7-4450-998c-9430ff158bad. Income levels are now based on the derived ranges in `income_level_master_2025.md`.

## Data Points
- **Monthly Income**: Determines income level (Low, Sufficient, Good) based on `income_level_master_2025.md`.
- **Date of Birth (DOB)**: Derives age to assign life cycle stage.
- **Number and DOB of Dependents**: Determines family responsibilities.
- **Occupation**: White-Collar or Blue-Collar.
- **Existing Loans and Monthly Loan Repayment**: Assesses debt impact on sufficiency.

## Life Cycle Stages
- **Young Adult**: Age 22–30 (DOB 08/05/1995–08/05/2003), 0–1 dependents.
- **Young Family**: Age 28–35 (DOB 08/05/1990–08/05/1997), young children (age 0–7).
- **Mid-Career Family**: Age 35–50 (DOB 08/05/1975–08/05/1990), children age 8–18.
- **Pre-Retirement**: Age 50–60 (DOB 08/05/1965–08/05/1975), adult children (age > 18).
- **Retirement**: Age 60+ (DOB before 08/05/1965), typically no minor dependents.

## Investor Profiles

### White-Collar Profiles
| Category ID | Life Cycle Stage       | Age Range | Income Level (₹/month)      | Sufficiency | Dependents                | Financial Context                                      |
|-------------|------------------------|-----------|-----------------------------|-------------|---------------------------|-------------------------------------------------------|
| W1          | Young Adult            | 22–30     | Low (0 - 30,000)            | -           | 0–1 (none or spouse)      | Limited savings; starting career, possible student debt. |
| W2          | Young Adult            | 22–30     | Sufficient (30,001 - 60,000)| 0           | 0–1 (none or spouse)      | Moderate savings capacity; building emergency fund.    |
| W3          | Young Adult            | 22–30     | Good (> 60,000)             | +           | 0–1 (none or spouse)      | High savings potential; early retirement planning.    |
| W4          | Young Family           | 28–35     | Low (0 - 45,000)            | -           | 1–2 (young children, 0–7) | Tight budget; focus on emergency fund, education.     |
| W5          | Young Family           | 28–35     | Sufficient (45,001 - 90,000)| 0           | 1–2 (young children, 0–7) | Balanced savings; home purchase, education goals.     |
| W6          | Young Family           | 28–35     | Good (> 90,000)             | +           | 1–2 (young children, 0–7) | Strong savings; aggressive education, retirement plans. |
| W7          | Mid-Career Family      | 35–50     | Low (0 - 67,500)            | -           | 2–3 (children, 8–18)      | High expenses; education, marriage, debt challenges.  |
| W8          | Mid-Career Family      | 35–50     | Sufficient (67,501 - 135,000)| 0           | 2–3 (children, 8–18)      | Stable savings; education, marriage, retirement focus. |
| W9          | Mid-Career Family      | 35–50     | Good (> 135,000)            | +           | 2–3 (children, 8–18)      | High savings; multiple goals, early retirement push.  |
| W10         | Pre-Retirement         | 50–60     | Low (0 - 101,250)           | -           | 0–2 (adult children, >18) | Limited savings; urgent retirement planning.          |
| W11         | Pre-Retirement         | 50–60     | Sufficient (101,251 - 202,500)| 0         | 0–2 (adult children, >18) | Moderate savings; retirement, possible marriage goals. |
| W12         | Pre-Retirement         | 50–60     | Good (> 202,500)            | +           | 0–2 (adult children, >18) | Strong savings; robust retirement planning.           |
| W13         | Retirement             | 60+       | Low (0 - 101,250)           | -           | 0–1 (spouse, adult children) | Reliant on savings/pension; focus on preservation.   |
| W14         | Retirement             | 60+       | Sufficient (101,251 - 202,500)| 0         | 0–1 (spouse, adult children) | Stable income; balanced retirement spending.         |
| W15         | Retirement             | 60+       | Good (> 202,500)            | +           | 0–1 (spouse, adult children) | High savings; comfortable retirement lifestyle.      |

### Blue-Collar Profiles
| Category ID | Life Cycle Stage       | Age Range | Income Level (₹/month)     | Sufficiency | Dependents                | Financial Context                                      |
|-------------|------------------------|-----------|----------------------------|-------------|---------------------------|-------------------------------------------------------|
| B1          | Young Adult            | 22–30     | Low (0 - 12,000)           | -           | 0–1 (none or spouse)      | Minimal savings; basic living expenses, high debt risk. |
| B2          | Young Adult            | 22–30     | Sufficient (12,001 - 20,000)| 0           | 0–1 (none or spouse)      | Limited savings; emergency fund, small retirement goals. |
| B3          | Young Adult            | 22–30     | Good (> 20,000)            | +           | 0–1 (none or spouse)      | Moderate savings; early home purchase, retirement plans. |
| B4          | Young Family           | 28–35     | Low (0 - 18,000)           | -           | 1–2 (young children, 0–7) | Very tight budget; debt reduction, emergency fund focus. |
| B5          | Young Family           | 28–35     | Sufficient (18,001 - 30,000)| 0           | 1–2 (young children, 0–7) | Modest savings; education, home purchase goals.       |
| B6          | Young Family           | 28–35     | Good (> 30,000)            | +           | 1–2 (young children, 0–7) | Decent savings; education, home, retirement planning. |
| B7          | Mid-Career Family      | 35–50     | Low (0 - 27,000)           | -           | 2–3 (children, 8–18)      | High debt risk; education, marriage, survival focus.  |
| B8          | Mid-Career Family      | 35–50     | Sufficient (27,001 - 45,000)| 0           | 2–3 (children, 8–18)      | Balanced savings; education, marriage, retirement goals. |
| B9          | Mid-Career Family      | 35–50     | Good (> 45,000)            | +           | 2–3 (children, 8–18)      | Strong savings for education, marriage, retirement.   |
| B10         | Pre-Retirement         | 50–60     | Low (0 - 40,500)           | -           | 0–2 (adult children, >18) | Minimal savings; urgent retirement, debt challenges.  |
| B11         | Pre-Retirement         | 50–60     | Sufficient (40,501 - 67,500)| 0           | 0–2 (adult children, >18) | Modest savings; retirement, possible marriage goals.  |
| B12         | Pre-Retirement         | 50–60     | Good (> 67,500)            | +           | 0–2 (adult children, >18) | Decent savings; comfortable retirement planning.      |
| B13         | Retirement             | 60+       | Low (0 - 40,500)           | -           | 0–1 (spouse, adult children) | Reliant on limited savings; preservation focus.      |
| B14         | Retirement             | 60+       | Sufficient (40,501 - 67,500)| 0           | 0–1 (spouse, adult children) | Stable savings; modest retirement lifestyle.         |
| B15         | Retirement             | 60+       | Good (> 67,500)            | +           | 0–1 (spouse, adult children) | High savings; secure retirement lifestyle.           |

## Notes for Developers
- **Age Derivation**: Calculate age as of current date (e.g., 08/05/2025, DOB 15/03/1970 → Age = 55). Use DOB ranges to assign life cycle stage.
- **Category Assignment**: Map investor data (artifact_id: 91228f9a-35a0-4524-a828-0272c1c8b96c) to profiles using:
  - Occupation → Collar (White-Collar or Blue-Collar).
  - Age → Life Cycle Stage.
  - Monthly Income → Income Level (Low, Sufficient, Good) as per `income_level_master_2025.md`.
  - Example: Age 45, Blue-Collar, ₹37,000/month → B8 (Mid-Career Family, Sufficient).
- **Overlap Handling**: For ages in multiple stages (e.g., 28 in Young Adult and Young Family), prioritize based on dependents (e.g., young children → Young Family).
- **Dynamic Queries**: Use category IDs in SQL/API calls (e.g., `SELECT goals FROM financial_goals WHERE category_id = 'B8'`).
- **Sufficiency Logic**: Low (-): Insufficient for goals; Sufficient (0): Adequate for basic goals; Good (+): Strong for multiple goals.

## Conclusion
This master defines 30 investor profiles, providing a standardized framework for financial planning and communication. Category IDs (W1–W15, B1–B15) enable consistent referencing across documents, supporting dynamic content generation and tailored investor guides. Income levels are now aligned with the `income_level_master_2025.md`.
