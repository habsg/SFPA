# Detailed Development Plan: Comprehensive Financial Planning Application

This document outlines the detailed development plan for implementing the full Comprehensive Financial Planning Framework (2025) into the Streamlit application. This plan builds upon the initial analysis and suggestions and aligns with the master framework documents.

## Guiding Principles:

*   **Phased Implementation:** Break down the development into manageable phases, focusing on foundational elements first.
*   **Incremental Testing:** Test each module and feature thoroughly as it's developed.
*   **Framework Adherence:** Ensure all development aligns with the specifications in "Comprehensive Financial Planning Framework (2025) (MFD version) - Part 1 & 2".
*   **Modularity:** Design components to be as modular as possible for easier maintenance and future upgrades.
*   **Compliance and Security:** Integrate security and compliance (DPDP Act, SEBI) requirements from the outset.

## Development Phases and Tasks:

### Phase 1: Core Framework Enhancements & Database Foundation

*   **Objective:** Establish a robust data backend and implement core investor profiling and risk assessment.
*   **Tasks:**
    1.  **Database Setup/Migration (PostgreSQL):**
        *   Set up a PostgreSQL database instance.
        *   Define and create the complete database schema based on Framework Part 1 (Sec 5.4 JSON Schema) and Part 2 (Sec 23), including tables for `investors` (with `financial_history`, `profile_history`, `validation_results`, `consent_log`), `financial_plans` (with `goals`, `ai_recommendations`, `audit_log`), `economic_indicators`.
        *   Refactor existing `app.py` database functions (`init_db`) to connect to and interact with PostgreSQL. Use an ORM like SQLAlchemy if appropriate for managing models.
    2.  **Full Investor Profiling Logic:**
        *   Implement the 30 Investor Profiles (W1-W15, B1-B15) as defined in Framework Part 1, Sec 3.
        *   Develop the `assign_profile` function to accurately map investors based on occupation, age (dynamic calculation), individual income, and dependents.
        *   Implement the detailed Income Level Methodology (Framework Part 1, Sec 4).
        *   Implement logic for profile transitions, including income updates and post-lock re-profiling (Framework Part 1, Sec 5.3).
        *   Enhance the investor input form in `app.py` for progressive onboarding and to capture all required fields (e.g., predictive signals, notification consent).
    3.  **Enhanced Risk Assessment Module:**
        *   Revise `calculate_risk_score` to align with the comprehensive methodology in Framework Part 1, Sec 11 (Dynamic Risk Scoring, factors like emergency fund adequacy, debt burden, life cycle, income stability, dependents, market experience).
        *   Implement historical risk score tracking within the `investors` table or a related table.
        *   Lay groundwork for future AI validation and stress testing inputs.
    4.  **Basic Financial Goal Management:**
        *   Develop UI elements for MFDs to manually input investor financial goals (type, amount, timeline) as per Framework Part 1, Sec 6 & 7.
        *   Store goals in the `financial_plans.goals` structure.
        *   Implement a basic SIP calculation (without full best/worst/base case scenarios initially, but with the formula from Framework Part 1, Sec 6).

### Phase 2: Economic Data Integration and Initial Dashboards

*   **Objective:** Integrate real economic data and provide initial dashboard views for MFDs and investors.
*   **Tasks:**
    1.  **Economic Update Module:**
        *   Identify and integrate APIs for key economic indicators (GDP, IIP, CPI, etc.) from sources like MOSPI, RBI (Framework Part 2, Sec 19.2).
        *   Develop scripts/jobs for scheduled monthly data fetching and storage in the `economic_indicators` table.
        *   Store historical economic data for trend analysis.
    2.  **MFD Economic Dashboard:**
        *   Create a new page/section in the Streamlit app for the MFD Economic Dashboard (`/mfd-dashboard/economic-insights`).
        *   Display current values of key economic indicators.
        *   Implement basic trend graphs (e.g., using Plotly Express, already imported) for selected indicators.
    3.  **Initial Investor Dashboard:**
        *   Develop the "Investor Dashboard" page to show basic information: current profile, calculated risk score and rating, and a list of their entered financial goals.

### Phase 3: Foundational AI Integration

*   **Objective:** Introduce initial AI capabilities for validation and analysis.
*   **Tasks:**
    1.  **AI for Input Validation:**
        *   Integrate basic AI/rule-based checks for investor input validation (e.g., flagging inconsistencies like very high income for a typically low-income profile) as per Framework Part 1, Sec 5.1 & 5.4.
        *   Store validation results/flags.
    2.  **AI for Economic Trend Analysis (Basic):**
        *   Develop simple models or rules to identify basic trends in the stored economic data (e.g., consecutive decline/increase in GDP).
        *   Display these basic AI-driven insights on the MFD Economic Dashboard.

### Phase 4: Advanced Goal Management, Savings Logic & Plan Stability

*   **Objective:** Implement sophisticated goal management, savings calculations, and plan stability features.
*   **Tasks:**
    1.  **Advanced Financial Goal Management:**
        *   Explore NLP for goal input (Framework Part 1, Sec 6). If full NLP is too complex initially, implement highly structured input with clear categorization.
        *   Implement AI-driven goal adjustments based on economic updates and profile changes (Framework Part 1, Sec 6).
        *   Implement full SIP calculation with best-case, base-case, worst-case scenarios (Framework Part 1, Sec 6).
        *   Develop logic for investment product selection based on goals, risk, and economic conditions (Framework Part 1, Sec 6).
    2.  **Savings Calculation Logic:**
        *   Implement the Recommended Savings Rates slab structure and modifiers (Framework Part 1, Sec 8).
        *   Implement Annual Savings Adjustment Rates (base and fallback) (Framework Part 1, Sec 9).
        *   Calculate and display Disposable Income, Savings Amount, Blended Rate, and Feasibility Index.
    3.  **Plan Lock Mechanism & Annual Health Checks:**
        *   Implement the three-year Plan Lock mechanism (Framework Part 1, Sec 14).
        *   Design and implement the Annual Health Check process, including automated update triggers and version control (Framework Part 1, Sec 16).
        *   Implement Feasibility Analysis module (Framework Part 1, Sec 15).

### Phase 5: Communication, Reporting, and Compliance

*   **Objective:** Build out communication channels, reporting, and ensure compliance.
*   **Tasks:**
    1.  **Communication Framework:**
        *   Set up stubs for multilingual support (English, Hindi, Tamil, Bengali, Telugu, Marathi) - actual translations can be added iteratively (Framework Part 2, Sec 18).
        *   Develop a system for core notifications (app, placeholders for SMS/email) for events like profile transitions, risk score changes, plan updates.
        *   Implement consent management for communications (`investors.consent_log`).
    2.  **Report Generation:**
        *   Develop functionality to generate the Investor Guide (HTML/PDF) (Framework Part 2, Sec 20).
        *   Develop functionality to generate basic MFD reports and the standardized Investor Report (Framework Part 2, Sec 21, 22).
    3.  **Compliance and Privacy:**
        *   Implement comprehensive audit logging in `financial_plans.audit_log` for all critical actions (SEBI compliance) (Framework Part 1, Sec 3 & 5.3; Part 2, Sec 23).
        *   Ensure all data handling, especially encryption and data masking, aligns with DPDP Act, 2023.

### Phase 6: Full AI Capabilities and Advanced MFD Tools

*   **Objective:** Implement advanced AI features and complete MFD tooling.
*   **Tasks:**
    1.  **Advanced AI Features:**
        *   Implement Dynamic Risk Scoring adjustments based on AI insights (Framework Part 1, Sec 11.3).
        *   Develop predictive insights for life events (Framework Part 1, Sec 3 & 5.1).
        *   Integrate AI recommendations for investment choices and goal adjustments more deeply.
        *   Implement AI API resilience strategies (Framework Part 1, Sec 17.4).
    2.  **Full MFD Dashboard Functionality:**
        *   Complete the MFD Dashboard with investor selection panel, trigger badges, detailed plan management views, and action items (Framework Part 2, Sec 21).
        *   Implement functionality for MFDs to manually apply dynamic plan adjustments based on economic data (Framework Part 2, Sec 19.5).
    3.  **Stress Testing & Scenario Analysis:**
        *   Implement stress testing scenarios for risk assessment (Framework Part 1, Sec 11.4).
        *   Develop the Scenario Analysis Tool for MFDs (Framework Part 1, Sec 17.3).

### Ongoing Tasks (Across All Phases):

*   **Security:** Regularly review and implement security best practices.
*   **UI/UX Refinement:** Continuously improve the user interface and experience for both MFDs and (eventually) investors.
*   **Testing:** Unit tests, integration tests, and user acceptance testing (simulated by MFD persona).
*   **Documentation:** Maintain up-to-date code documentation and update the framework documentation if any deviations or clarifications arise.
*   **Dependency Management:** Keep `requirements.txt` (or equivalent for PostgreSQL drivers and other libraries) updated.

This detailed plan will be used to guide the development process. Each phase will be broken down further into specific coding tasks. Progress will be tracked against this plan and the `todo.md` file.
