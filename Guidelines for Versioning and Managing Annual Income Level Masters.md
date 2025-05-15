# Guidelines for Versioning and Managing Annual Income Level Masters

## 1. Introduction

This document provides guidelines for creating, managing, and utilizing annual versions of the Income Level Master. The primary goal is to ensure that income categorizations remain relevant over time and that new investors are assessed against the most current income benchmarks, while existing investor data can be maintained or updated as needed.

## 2. Creating a New Annual Income Level Master

At the beginning of each new year (or as deemed necessary due to significant economic shifts), a new Income Level Master should be created. The process is as follows:

*   **Review and Update Formula:** The `income_level_formula.md` should be reviewed. If the base thresholds (e.g., daily income for "Low" category) or the progression multipliers need adjustment for the new year, a new version of the formula document should be created (e.g., `income_level_formula_YYYY.md`, where YYYY is the new year).
*   **Generate New Master File:** Based on the (potentially updated) formula, a new Income Level Master file should be generated. This file must follow the naming convention: `income_level_master_YYYY.md` (e.g., `income_level_master_2026.md`).
*   **Content of New Master File:** The new master file should clearly state the year it applies to in its title and introductory text. The income range tables will be updated according to the new year's formula.

## 3. Updating the Investor Profiles Master

While the `Investor_Profiles_Master_Updated.markdown` defines the general structure of investor profiles, the specific income ranges it refers to for *new* investors should always point to the latest available annual Income Level Master.

*   **For New Investors:** Any system or process that assigns profiles to new investors must be configured to dynamically use the `income_level_master_YYYY.md` corresponding to the current year of the investor's onboarding or assessment.
*   **For Existing Investors:**
    *   **Option 1 (Retain Original Assessment):** By default, existing investors should retain the income level categorization they were assigned based on the Income Level Master active at the time of their initial assessment. This maintains historical consistency.
    *   **Option 2 (Periodic Re-assessment):** A policy can be implemented to periodically re-assess existing investors against a newer Income Level Master (e.g., every few years, or upon significant life events). This would require updating their profile to reflect the new income categorization.
*   **Documentation Reference:** The "Notes for Developers" section within `Investor_Profiles_Master_Updated.markdown` should be updated annually if the primary reference for *new* investor income levels changes. However, the core structure of the profiles themselves may not need annual changes unless the life cycle stages or other fundamental aspects are revised.

## 4. System Logic for Automatic Assignment (New Investors)

To ensure new investors are always assessed against the latest income data, the following logic should be implemented in any automated system:

1.  **Identify Current Year:** The system should determine the current calendar year.
2.  **Locate Latest Master:** The system should look for an Income Level Master file matching the pattern `income_level_master_YYYY.md`, where YYYY is the current year.
3.  **Fallback (If Current Year Master Not Found):** If a master file for the absolute current year is not yet available (e.g., early in January before the new master is published), the system should use the most recent previous year's master file available (e.g., if it's January 2027 and `income_level_master_2027.md` isn't ready, use `income_level_master_2026.md`). A notification should be triggered for administrators to create the current year's master.
4.  **Apply to New Investor:** The selected Income Level Master is then used to determine the income level (Low, Sufficient, Good) for the new investor based on their provided monthly income.

## 5. Archiving and Maintenance

*   All annual Income Level Master files (e.g., `income_level_master_2025.md`, `income_level_master_2026.md`, etc.) and their corresponding formula documents should be archived and maintained for historical reference and potential audits.
*   The `summary_report.md` should also be updated or a new one generated whenever a new annual master is created, detailing the changes and referencing the new files.

By following these guidelines, the income level categorization system can remain current, accurate, and adaptable to changing economic conditions over time.
