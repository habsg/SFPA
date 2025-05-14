# PostgreSQL Database Schema for Comprehensive Financial Planning Application

**Constraint:** All components must be free, open-source, and self-hostable.

This document outlines the proposed PostgreSQL database schema based on the "Comprehensive Financial Planning Framework (2025) (MFD version) - Part 1 & 2" and the user's constraint to use only free and open-source software.

## General Notes:

*   **Database System:** PostgreSQL (Free and Open-Source)
*   **JSONB Usage:** For flexible storage of structured or semi-structured data like history logs, complex objects (e.g., dependents, goals, AI recommendations).
*   **Timestamps:** Use `TIMESTAMPTZ` for all date/time fields to ensure timezone awareness.
*   **Primary Keys:** Typically `SERIAL PRIMARY KEY` for auto-incrementing IDs or `TEXT PRIMARY KEY` for predefined IDs like `investor_id`.
*   **Foreign Keys:** To be defined to maintain relational integrity where appropriate (e.g., linking financial plans to investors).
*   **Encryption:** Application-level encryption (using Fernet as in `app.py` or similar open-source libraries) will be handled for sensitive PII before storing it, even in JSONB fields. The database itself can also offer encryption at rest if configured.

## Table Definitions:

### 1. `investors` Table

Stores core investor profile information, financial details, history, and consent logs.

```sql
CREATE TABLE investors (
    investor_id TEXT PRIMARY KEY, -- e.g., INV-YYYYMMDD-NNNN
    name TEXT NOT NULL,
    dob DATE NOT NULL, -- Date of Birth
    occupation TEXT, -- 'White-Collar', 'Blue-Collar'
    urban_rural_status TEXT, -- 'Urban', 'Rural'
    home_ownership BOOLEAN,
    rent_amount NUMERIC(10, 2) DEFAULT 0.00,
    emi_amount NUMERIC(10, 2) DEFAULT 0.00,
    current_emergency_fund NUMERIC(12, 2) DEFAULT 0.00,
    market_linked_experience TEXT, -- 'Yes', 'No'
    plan_in_action_date DATE, -- Date the plan is activated
    current_profile_id TEXT, -- e.g., W1, B8
    lock_status BOOLEAN DEFAULT TRUE,
    economic_condition TEXT DEFAULT 'Normal', -- 'Normal', 'Slowdown'
    
    -- Financial Details (encrypted at application level if sensitive, stored as JSONB)
    financial_details JSONB, -- Includes self_income, spouse_income, total_household_income, mobile_number, email, updated_date
    
    -- Historical Data (arrays of objects)
    financial_history JSONB, -- Array of {self_income, spouse_income, ..., update_date, source}
    profile_history JSONB, -- Array of {profile_id, start_date, end_date, reason}
    risk_score_history JSONB, -- Array of {score, rating, date, assessment_details}

    -- AI & Validation
    predictive_signals JSONB, -- {family_planning, job_stability}
    validation_results JSONB, -- Stores AI validation flags/suggestions for inputs

    -- Consent and Logs
    consent_log JSONB, -- Array of {action, sms_allowed, email_allowed, timestamp}

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

**Notes for `investors` table:**
*   `financial_details`: Contains current income, contact info. Sensitive fields like mobile/email should be encrypted by the application before storing in this JSONB.
*   `risk_score_history`: Will store the calculated risk score, the corresponding rating (e.g., "Low (Conservative)"), the date of assessment, and potentially the answers or key factors contributing to that score.

### 2. `financial_plans` Table

Stores details about financial goals, investment recommendations, and AI-driven suggestions for each investor.

```sql
CREATE TABLE financial_plans (
    plan_id SERIAL PRIMARY KEY,
    investor_id TEXT NOT NULL REFERENCES investors(investor_id) ON DELETE CASCADE,
    plan_version INTEGER DEFAULT 1,
    plan_creation_date DATE DEFAULT CURRENT_DATE,
    last_health_check_date DATE,
    next_health_check_date DATE,

    -- Goals (array of objects)
    goals JSONB, -- Array of {goal_id, goal_type, target_amount, current_corpus, timeline_years, priority, sip_details {worst_case, base_case, best_case}, recommended_fund_type, status, ai_recommendation {priority_rationale, confidence}}

    -- Investment Allocations (could be part of goals or separate)
    -- For simplicity, initial investment recommendations can be within the 'goals' JSONB.
    -- A more complex setup might have a separate 'investments' table linked to goals.

    -- AI Recommendations for the overall plan
    ai_plan_recommendations JSONB, -- General AI insights or adjustments for the plan

    -- Audit Log for this specific plan version (changes to goals, savings, etc.)
    -- More granular audit logs for SEBI might be a separate dedicated table if very detailed logging is needed per action.
    plan_audit_log JSONB, -- Array of {timestamp, action, user_type (MFD/System), details, old_value, new_value}

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

**Notes for `financial_plans` table:**
*   Each investor can have multiple plan versions over time, especially after annual health checks or significant life events.
*   `goals`: Each goal object will contain all relevant details including SIP calculations for different scenarios and the fund type suggested.

### 3. `economic_indicators` Table

Stores monthly economic data used for analysis and dashboard displays.

```sql
CREATE TABLE economic_indicators (
    indicator_id SERIAL PRIMARY KEY,
    data_date DATE NOT NULL, -- e.g., 2025-05-01 (first day of the month for which data applies)
    indicator_name TEXT NOT NULL, -- e.g., 'GDP_Growth_Rate', 'CPI_Inflation'
    indicator_value NUMERIC(10, 2),
    source TEXT, -- e.g., 'MOSPI API', 'RBI Data Feed'
    unit TEXT, -- e.g., '%', 'INR Crores'
    
    -- Optional: Store raw data or more details if needed
    raw_data JSONB,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (data_date, indicator_name) -- Ensure only one value per indicator per date
);
```

**Alternative for `economic_indicators` (wide format, one row per month):**
```sql
CREATE TABLE monthly_economic_summary (
    summary_id SERIAL PRIMARY KEY,
    data_month DATE NOT NULL UNIQUE, -- e.g., 2025-05-01, representing May 2025
    gdp_growth_rate NUMERIC(5,2),
    iip_growth NUMERIC(5,2),
    cpi_inflation NUMERIC(5,2),
    core_sector_growth NUMERIC(5,2),
    bank_credit_growth NUMERIC(5,2),
    unemployment_rate NUMERIC(5,2),
    forex_reserves_usd_billion NUMERIC(10,2),
    inr_usd_depreciation_percentage NUMERIC(5,2),
    gst_collections_inr_lakh_crore NUMERIC(10,2),
    automobile_sales_units INTEGER,
    stock_market_index_points NUMERIC(10,2),
    rural_demand_indicator_value NUMERIC(10,2), -- e.g., tractor sales
    global_economic_indicator_value NUMERIC(10,2),
    -- Add other indicators as needed
    data_sources JSONB, -- Store sources for each indicator for the month
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```
**Consideration for `economic_indicators`:** The wide format (`monthly_economic_summary`) might be simpler for querying if all indicators are typically fetched together for a given month. The long format (`economic_indicators`) is more flexible if the number or type of indicators changes frequently or if not all indicators are available every month.
Given the framework's mention of specific indicators, the `monthly_economic_summary` (wide format) might be more practical for the MFD dashboard and AI analysis, assuming a consistent set of indicators is tracked monthly. Data sources can be a JSONB field listing sources for that month's data points.

### 4. `audit_log_global` Table (Optional - for very detailed SEBI compliance)

For comprehensive, system-wide audit trails beyond individual plan changes.

```sql
CREATE TABLE audit_log_global (
    log_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT, -- MFD ID or 'SYSTEM'
    investor_id_context TEXT, -- If action relates to a specific investor
    action_type TEXT NOT NULL, -- e.g., 'LOGIN', 'INVESTOR_CREATE', 'DATA_EXPORT', 'SETTINGS_CHANGE'
    details JSONB, -- Specifics of the action, IP address, etc.
    status TEXT -- 'SUCCESS', 'FAILURE'
);
```
**Note:** The `plan_audit_log` within `financial_plans` might be sufficient if SEBI requirements focus on plan modifications. A global log is for broader system actions.

## Data Source Considerations (Free & Open-Source Constraint):

*   **Economic Indicators:** Prioritize official government APIs (e.g., data.gov.in, MOSPI, RBI if they offer free tiers/public data access) or reliable public data sources that can be scraped (ethically and respecting terms of service) if direct APIs are not available or are paid. This may require building custom scrapers or parsers.
*   **AI Features:** Utilize open-source Python libraries for NLP (e.g., spaCy, NLTK), machine learning (scikit-learn), and rule-based systems. Complex AI models requiring significant cloud compute (like large language models for free-form text analysis beyond basic keyword matching) might need to be simplified or implemented with smaller, locally runnable open-source models if performance allows.

This schema provides a foundation. It will be refined as development progresses and specific query patterns emerge. The use of JSONB offers flexibility for evolving data structures within these core tables.
