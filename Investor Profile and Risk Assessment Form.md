# Investor Profile and Risk Assessment Form

## Purpose
This form collects essential data to build a comprehensive investor profile, assess risk tolerance, and tailor financial plans, including savings rates and investment objectives, for White-Collar and Blue-Collar investors. It supports goal-based planning, savings adjustments, and risk profiling while ensuring privacy in report generation.

## Form Structure

| Field/Question | Description | Input Type | Validation |
|----------------|-------------|------------|------------|
| **Name** | Investor’s full name (for identification and file naming only) | Text | Mandatory, non-empty; standardize to title case (e.g., “Rakesh Gupta”) |
| **Investor ID** | Unique identifier for the investor (auto-generated) | Text (Auto-generated) | Format: `INV-YYYYMMDD-NNNN` (e.g., `INV-20250509-0001`) or UUID-based (e.g., `INV-8f3k9d`) |
| **PAN (Optional)** | Investor’s Permanent Account Number (for financial integrations) | Text | Optional; 10 characters, format: AAAAA9999A; mask if displayed (e.g., “XXXXX1234F”) |
| **Date of Birth (DOB)** | Investor’s date of birth in dd/mm/yyyy format | Text | Mandatory; Format: dd/mm/yyyy (e.g., 15/03/1970); Age derived must be 18–100 as of 09/05/2025 |
| **Monthly Income (₹)** | Investor’s monthly income | Numeric | Positive number, e.g., 10000–1000000 |
| **Spouse’s Monthly Income (₹)** | Spouse’s monthly income to assess household savings capacity | Numeric | Optional; Positive number, e.g., 0–1000000 |
| **Occupation** | Investor’s occupation type | Dropdown | White-Collar/Blue-Collar |
| **Urban/Rural Status** | Investor’s living environment for cost adjustments | Dropdown | Mandatory; Urban/Rural |
| **Number of Dependents** | Number of financial dependents | Numeric | 0–10 |
| **DOB and Gender of Dependents** | Date of birth (dd/mm/yyyy) and gender of each dependent | Array of Pairs (DOB: Text, Gender: Dropdown) | DOB: Format dd/mm/yyyy (e.g., 10/05/2000); Age derived must be 0–100 as of 09/05/2025; Max 10 entries; Gender: Male/Female/Other |
| **Home Ownership** | Do you own a home or live with parents and do not plan to purchase one? | Dropdown | Yes/No |
| **Paying Rent** | Are you currently paying rent? | Dropdown | Yes/No |
| **Preferred Language** | Language for plan output | Dropdown | English/Hindi |
| **Market-Linked Investment Experience** | Has the investor ever invested in market-linked products (e.g., shares, equity funds)? | Dropdown | Yes/No |
| **Existing Loans** | Do you have existing loans? | Dropdown | Yes/No |
| **Monthly Loan Repayment (if Yes)** | What is your monthly loan repayment amount? (₹) | Numeric (Conditional) | Positive number, e.g., 0–500000; Required if Existing Loans is Yes |
| **Current Emergency Fund (₹)** | How much emergency fund (in ₹) do you currently have? | Numeric | Optional; Positive number, e.g., 0–10000000 |
| **Q1: Investment Experience** | How would you describe your investment experience? | Dropdown | 1: None / 2: Limited / 3: Moderate / 4: Good / 5: Extensive |
| **Q2: Comfort with Market Fluctuations** | How comfortable are you with market fluctuations? | Dropdown | 1: Not at all / 2: Slightly / 3: Neutral / 4: Comfortable / 5: Very comfortable |
| **Q3: Investment Horizon** | What is your investment horizon? | Dropdown | 1: <1 year / 2: 1–3 years / 3: 3–5 years / 4: 5–10 years / 5: >10 years |
| **Q4: Reaction to 20% Portfolio Drop** | How would you react to a 20% portfolio drop? | Dropdown | 1: Sell all / 2: Sell some / 3: Hold / 4: Hold and wait / 5: Buy more |
| **Q5: Financial Goal Priority** | What is your financial goal priority? | Dropdown | 1: Capital preservation / 2: Income stability / 3: Balanced growth / 4: Growth / 5: High growth |

### Risk Scoring
- **Score Calculation**: Sum of responses (1–5 per question), total range: 5–25.
- **Risk Profile**:
  - 5–10: Risk-Averse
  - 11–15: Moderate
  - 16–25: Aggressive

### Privacy Requirements
- **Name Usage**: The investor’s name is collected for identification and file naming during bulk generation (e.g., `Guide_Rakesh_Gupta_INV-20250509-0001.pdf`). It must not appear in the report content. Use “Dear Investor” as the salutation in the report.
- **Dependent Names**: Do not collect dependent names. Use generic terms like “son,” “daughter,” “parents,” “spouse,” etc., in the report content (e.g., “your daughter’s education”).
- **PAN Handling**: The PAN is optional and used for financial integrations (e.g., KYC checks). Do not include it in the report content. If displayed, mask it (e.g., “XXXXX1234F”). Secure PAN data per the Digital Personal Data Protection Act (DPDP Act, 2023), and obtain explicit consent for its use.
- **Investor ID**: Auto-generate a unique investor ID during form submission. Include the ID in the report header (e.g., “Investor ID: INV-20250509-0001”) and use it in filenames for identification.

## Notes for Developers
- **Data Validation**:
  - Numeric fields (e.g., Monthly Income, Spouse’s Monthly Income, Monthly Loan Repayment) must be non-negative.
  - Investor’s DOB must be in dd/mm/yyyy format; derive age as of 09/05/2025 (e.g., DOB 15/03/1970 → Age = 2025 - 1970 = 55 years). Age must be 18–100.
  - Dependents’ DOB must be in dd/mm/yyyy format; derive age as of 09/05/2025 (e.g., DOB 10/05/2000 → Age = 2025 - 2000 = 25 years). Age must be 0–100.
  - Ensure Monthly Loan Repayment ≤ Monthly Income.
  - Urban/Rural Status must be selected (Urban or Rural).
- **Dynamic Use**:
  - Derive investor’s age from DOB as of 09/05/2025 to determine life cycle stage (e.g., Young Adult: 22–30) per artifact_id: c4f92cd3-14c7-4450-998c-9430ff158bad.
  - Derive dependents’ ages from their DOBs as of 09/05/2025 to set goal timelines (e.g., education at age 16 for Class 11/12, marriage at age 25 for daughters) per artifact_id: c4f92cd3-14c7-4450-998c-9430ff158bad.
  - Use Urban/Rural Status to adjust costs for education, marriage, and retirement goals per `Master for Allocation for Education of Dependents`, `Master for Allocation for Marriage (of Daughters)`, and `Master for Allocation towards Retirement Fund`.
  - Calculate Loan-to-Income Ratio = Monthly Loan Repayment / Monthly Income to identify high-debt investors (> 20%).
  - Use Spouse’s Monthly Income to compute Spouse-to-Investor Income Ratio = Spouse’s Monthly Income / Monthly Income, applying modifiers to savings rates per `Recommended Savings Rates Master` and `Master for Annual Savings Adjustment Rates`.
  - Use Occupation to apply White-Collar/Blue-Collar specific rates and goals.
  - Use Risk Score to adjust investment allocations (e.g., risk-averse investors favor low-duration funds) per artifact_id: 96c2e445-0520-483e-b78b-24801b859fa6.
- **Form Design**:
  - Use HTML/CSS for layout, JavaScript for conditional fields (e.g., show Monthly Loan Repayment if Existing Loans is Yes).
  - Provide real-time validation (e.g., alert if repayment > income, invalid DOB format, Urban/Rural not selected), dynamic fields, and tooltips (e.g., “Select Urban if living in a city, Rural otherwise”).
- **Storage**:
  - Store responses in a structured database (e.g., SQL table: `investor_profiles`).
  - Example: `INSERT INTO investor_profiles (investor_id, name, pan, dob, monthly_income, spouse_monthly_income, occupation, urban_rural, dependents, existing_loans, loan_repayment, ...) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ...);`
  - Structure as JSON: `{"investor_id": "INV-20250509-0001", "name": "Rakesh Gupta", "pan": "XXXXX1234F", "dob": "15/03/1970", "monthly_income": 100000, "spouse_monthly_income": 50000, "occupation": "White-Collar", "urban_rural": "Urban", "dependents": [{"dob": "10/05/2000", "gender": "Female"}], "existing_loans": "No"}`.
- **Scalability**:
  - Update CSV/Google Forms formats (artifact_id: 9639dfc3-cc04-42c2-82be-c4d8ba94a787) to include new field: `urban_rural`.
- **Privacy Compliance**:
  - Ensure compliance with the DPDP Act, 2023, by securing personal data (e.g., name, PAN) and obtaining explicit consent for its use.

## Conclusion
This updated form captures the investor’s and dependents’ dates of birth, urban/rural status, and other critical data to enable accurate profile assignment, goal planning, and cost adjustments. It ensures compliance with privacy requirements and supports tailored financial plans for White-Collar and Blue-Collar investors.