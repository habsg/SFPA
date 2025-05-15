# Master Document: Mutual Fund Investment Options Based on Goals

## Purpose
This document defines mutual fund schemes as investment types for financial goals, categorized by time horizon. It ensures that investments align with the duration and risk profile of goals, such as home purchase, children’s education, marriage, or retirement, for Indian investors.

## Framework

### Investment Options by Time Horizon
The following table maps mutual fund schemes to goal durations, with allocations as specified. All schemes are standard mutual fund categories available in India (e.g., SEBI-defined categories).

| Time Horizon           | Mutual Fund Schemes                         | Allocation        | Rationale                                                                 |
|------------------------|---------------------------------------------|-------------------|---------------------------------------------------------------------------|
| Less than 1 month      | Overnight Fund / Ultra Short Duration Fund  | 50% / 50%         | High liquidity, minimal risk for short-term or frequent withdrawals.       |
| Up to 1 year           | Ultra Short Duration Fund / Low Duration Fund | 50% / 50%        | Low risk, stable returns for near-term goals with moderate liquidity needs.|
| Up to 3 years          | Low Duration Fund / Floater Fund            | 50% / 50%         | Low to moderate risk, suitable for short- to medium-term goals.            |
| 3–5 years              | Hybrid Balanced Fund / Hybrid Equity Fund   | 50% / 50%         | Balanced risk, combining debt and equity for medium-term growth.           |
| 5–7 years              | Flexi Cap Fund / Multi Cap Fund             | 50% / 50%         | Diversified equity exposure, suitable for medium- to long-term growth.     |
| 7–10 years             | Multi Cap Fund / Mid Cap Fund               | 50% / 50%         | Higher equity risk, targeting growth for long-term goals.                  |
| More than 10 years     | Multi Cap Fund / Mid Cap Fund / Small Cap Fund | 40% / 40% / 20% | High-risk, high-return equity mix for long-term wealth creation.          |

### Notes
- **Scheme Definitions**:
  - **Overnight Fund**: Invests in overnight securities, offering high liquidity.
  - **Ultra Short Duration Fund**: Debt funds with Macaulay duration of 3–6 months.
  - **Low Duration Fund**: Debt funds with Macaulay duration of 6–12 months.
  - **Floater Fund**: Debt funds investing in floating-rate instruments, reducing interest rate risk.
  - **Hybrid Balanced Fund**: 40–60% equity, rest in debt, balancing growth and stability.
  - **Hybrid Equity Fund**: 65–80% equity, rest in debt, for moderate risk.
  - **Flexi Cap Fund**: Equity funds investing across market caps with flexibility.
  - **Multi Cap Fund**: Equity funds with mandated allocation across large, mid, and small caps.
  - **Mid Cap Fund**: Equity funds focused on mid-cap stocks (101st–250th by market cap).
  - **Small Cap Fund**: Equity funds focused on small-cap stocks (251st and below).
- **Allocation**: Equal splits (50%/50% or 40%/40%/20%) ensure diversification within the time horizon.
- **Application**: Use this mapping in investment plans by selecting schemes based on the goal’s timeline (e.g., 8-year education goal uses Multi Cap/Mid Cap).

## Integration with App
- **Input**: Goal time horizon (e.g., 5 years for home purchase).
- **Processing**: Map horizon to schemes and allocation (e.g., 5 years → Flexi Cap 50%, Multi Cap 50%).
- **Output**: Specify mutual fund schemes in investment plans (e.g., “Invest ₹2,000/month in Flexi Cap Fund”).
- **UI**: Display scheme names and allocations in plan tables, with tooltips explaining risk/liquidity.

## Notes for Developers
- **Validation**: Ensure time horizon is numeric and maps to a defined category.
- **Data Storage**: Store scheme mappings as a lookup table for dynamic plan generation.
- **Flexibility**: Allow overrides for specific investor preferences (e.g., prefer Ultra Short over Low Duration).

## Conclusion
This document provides a standardized mapping of mutual fund schemes to goal time horizons, ensuring appropriate risk and return profiles for Indian investors. It will guide investment type selection in year-wise financial plans.