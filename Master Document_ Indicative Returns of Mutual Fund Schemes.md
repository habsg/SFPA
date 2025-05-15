# Master Document: Indicative Returns of Mutual Fund Schemes

## Purpose
This document provides fixed indicative annual returns for mutual fund schemes used in financial planning calculations for Indian investors. The returns are specified for app-based computations as of May 06, 2025, and reflect typical post-expense ratio performance for each scheme.

## Framework

### Indicative Returns
The following table lists mutual fund schemes with their indicative annualized returns and descriptions, as provided for use in investment planning calculations.

| Mutual Fund Scheme            | Indicative Annual Return (%) | Description                                                                 |
|-------------------------------|-----------------------------|-----------------------------------------------------------------------------|
| Overnight Fund                | 4.5                         | Invests in overnight securities, offering high liquidity.                   |
| Ultra Short Duration Fund     | 5.5                         | Debt funds with Macaulay duration of 3–6 months.                            |
| Low Duration Fund             | 6.0                         | Debt funds with Macaulay duration of 6–12 months.                           |
| Floater Fund                  | 6.5                         | Debt funds investing in floating-rate instruments, reducing interest rate risk. |
| Hybrid Balanced Fund          | 8.0                         | 40–60% equity, rest in debt, balancing growth and stability.                |
| Hybrid Equity Fund            | 9.0                         | 65–80% equity, rest in debt, for moderate risk.                             |
| Flexi Cap Fund                | 10.0                        | Equity funds investing across market caps with flexibility.                 |
| Multi Cap Fund                | 12.0                        | Equity funds with mandated allocation across large, mid, and small caps.    |
| Mid Cap Fund                  | 13.0                        | Equity funds focused on mid-cap stocks (101st–250th by market cap).         |
| Small Cap Fund                | 14.0                        | Equity funds focused on small-cap stocks (251st and below by market cap).   |

### Notes
- **Return Basis**:
  - Returns are fixed as specified, representing post-expense ratio annualized performance (e.g., net of 0.5–2% expense ratios typical for Indian mutual funds).
  - Intended for use in future value and savings calculations, assuming stable market conditions as of 2025.
- **Usage**:
  - Apply returns in financial formulas, e.g., Future Value: FV = PV × (1 + r)^n or PMT × [((1 + r)^n - 1) / r], where r = annual return / 12 (monthly), n = months.
  - Example: ₹1,000/month in Flexi Cap Fund (10%) for 5 years yields FV ≈ ₹77,437 (compounded monthly).
- **Scheme Definitions**:
  - All schemes align with SEBI-defined mutual fund categories in India.
  - Returns reflect the risk profile: low for debt funds (4.5–6.5%), moderate for hybrids (8–9%), high for equity funds (10–14%).
- **Modification**: Users may adjust returns via app settings if specific fund performance deviates, but these values are defaults.

## Integration with App
- **Input**: Link schemes to goals via time horizon (e.g., from a companion mapping document).
- **Processing**: Use indicative returns for savings calculations (e.g., ₹1,000/month at 6% for 3 years).
- **Output**: Display returns in plan details (e.g., “Flexi Cap Fund, expected 10%”).
- **UI**: Provide input fields for users to override returns, with validation (e.g., 0–20% range).

## Notes for Developers
- **Data Storage**: Store schemes, returns, and descriptions in a table with fields for return percentage and category.
- **Validation**: Ensure returns are numeric and applied correctly in calculations (e.g., 4.5% as 0.045 annually).
- **Flexibility**: Support user-defined returns while defaulting to these values for consistency.

## Conclusion
This document provides fixed indicative returns for mutual fund schemes, enabling accurate financial planning calculations for Indian investors. The specified returns (e.g., 4.5% for Overnight Fund, 14% for Small Cap Fund) ensure standardized app computations, with flexibility for user modifications.