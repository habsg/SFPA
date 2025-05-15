# Methodology for Defining Income Levels (-/0/+) for Year 2025

This document outlines the formula and rules used to define income levels (Low, Sufficient, Good, corresponding to -, 0, + sufficiency) for White-Collar and Blue-Collar investors across different life cycle stages in the Indian context, specifically for the year 2025. The methodology is based on initial user-provided daily income benchmarks and a progressive scaling factor for life cycle advancements.

## 1. Base "Low" Income Thresholds for Young Adult Stage (Monthly)

The foundation for "Low" income is derived from the user's daily income suggestions, converted to monthly figures (assuming 30 days per month):

*   **White-Collar (WC) - Young Adult (Age 22-30):**
    *   User suggestion: < ₹1000/day
    *   Calculated "Low" (-): Income up to **₹30,000 per month**.
*   **Blue-Collar (BC) - Young Adult (Age 22-30):**
    *   User suggestion: < ₹400/day
    *   Calculated "Low" (-): Income up to **₹12,000 per month**.

Let `L_upper(stage)` denote the upper limit of the "Low" income band for a given life cycle stage.
So, `L_upper(WC, Young Adult) = ₹30,000` and `L_upper(BC, Young Adult) = ₹12,000`.

## 2. Progression of "Low" Income Threshold Across Life Cycle Stages

The upper limit of the "Low" income band (`L_upper`) is adjusted upwards for subsequent life cycle stages to reflect potential career growth and increased financial responsibilities. A multiplier of **1.5** is applied for each advancement:

*   `L_upper(Young Family) = L_upper(Young Adult) * 1.5`
*   `L_upper(Mid-Career Family) = L_upper(Young Family) * 1.5`
*   `L_upper(Pre-Retirement) = L_upper(Mid-Career Family) * 1.5`
*   `L_upper(Retirement) = L_upper(Pre-Retirement)` (No further increase for the Retirement stage)

## 3. Defining "Sufficient" (0) and "Good" (+) Income Bands

Once `L_upper(stage)` is determined for each category and life cycle stage, the "Sufficient" (0) and "Good" (+) income bands are defined as follows:

*   **For White-Collar (WC) Investors:**
    *   **Low (-):** ₹0 – `L_upper(stage)`
    *   **Sufficient (0):** (`L_upper(stage)` + ₹1) – (`L_upper(stage)` * 2)
    *   **Good (+):** > (`L_upper(stage)` * 2)

*   **For Blue-Collar (BC) Investors:**
    *   **Low (-):** ₹0 – `L_upper(stage)`
    *   **Sufficient (0):** (`L_upper(stage)` + ₹1) – (`L_upper(stage)` * 5/3)  (Note: For BC Sufficient (0) upper bound, results of `L_upper(stage) * 5/3` will be used directly, e.g. 12000 * 5/3 = 20000)
    *   **Good (+):** > (`L_upper(stage)` * 5/3)

This systematic approach ensures that income levels are defined consistently across all investor profiles, rooted in the initial benchmarks and scaled logically for different life phases. The resulting income bands will be used to create the "Income Level Master" table.
