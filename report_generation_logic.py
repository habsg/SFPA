# report_generation_logic.py

from datetime import datetime
from weasyprint import HTML, CSS # Removed FontConfiguration import

# --- Formatting Utilities ---
def format_currency(amount, currency_symbol="₹") -> str:
    """Formats a float as currency string, e.g., ₹1,23,456.78"""
    if amount is None:
        return f"{currency_symbol}N/A"
    try:
        amount = float(amount)
        if amount < 0:
            return f"-{currency_symbol}{-amount:,.2f}"
        return f"{currency_symbol}{amount:,.2f}"
    except (ValueError, TypeError):
        return f"{currency_symbol}N/A"

def format_percentage(value, decimals=2) -> str:
    """Formats a float (0.0 to 1.0) as a percentage string, e.g., 12.34%"""
    if value is None:
        return "N/A"
    try:
        return f"{float(value) * 100:.{decimals}f}%"
    except (ValueError, TypeError):
        return "N/A"

# --- HTML Report Generation (Framework Part 2, Sec 19) ---
def generate_investor_report_html(
    investor_data: dict,
    profile_details: dict,
    risk_assessment: dict,
    financial_goals: list,
    savings_summary: dict,
    asset_allocation_summary: dict, 
    action_plan: list, 
    economic_outlook: dict
) -> str:
    """
    Generates a comprehensive Investor Guide report in HTML format.
    """
    investor_name = investor_data.get("name", "N/A")
    investor_profile_id = profile_details.get("profile_id", "N/A")
    investor_profile_desc = profile_details.get("description", "N/A")
    risk_score = risk_assessment.get("total_score", "N/A")
    risk_rating = risk_assessment.get("risk_rating", "N/A")
    
    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = f"Financial Plan Investor Guide - {investor_data.get('name', 'N/A')}"

    html_content = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; color: #333; }}
            .container {{ max-width: 800px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            h1 {{ text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            h2 {{ border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .section {{ margin-bottom: 20px; }}
            .footer {{ text-align: center; margin-top: 30px; font-size: 0.9em; color: #777; }}
            .summary-box {{ background-color: #eaf2f8; padding: 15px; border-radius: 5px; margin-bottom:20px;}}
        </style>
    </head>
    <body>
        <div class=\"container\">
            <h1>{title}</h1>
            <p style=\"text-align:center; font-style:italic;\">Report Generated: {report_date}</p>

            <div class=\"section\">
                <h2>1. Investor Profile</h2>
                <p><strong>Name:</strong> {investor_name}</p>
                <p><strong>Profile ID:</strong> {investor_profile_id}</p>
                <p><strong>Profile Description:</strong> {investor_profile_desc}</p>
                <p><strong>Date of Birth:</strong> {investor_data.get('dob', 'N/A')}</p>
                <p><strong>Occupation:</strong> {investor_data.get('occupation', 'N/A')}</p>
                <p><strong>Contact:</strong> {investor_data.get('mobile_number', 'N/A')} | {investor_data.get('email', 'N/A')}</p>
            </div>

            <div class=\"section summary-box\">
                <h2>2. Risk Assessment Summary</h2>
                <p><strong>Overall Risk Score:</strong> {risk_score}/100</p>
                <p><strong>Risk Rating:</strong> {risk_rating}</p>
                <p><em>Note: This score reflects your capacity and tolerance for investment risk.</em></p>
            </div>

            <div class=\"section\">
                <h2>3. Financial Goals Overview</h2>
    """
    if financial_goals:
        html_content += """
                <table>
                    <thead>
                        <tr>
                            <th>Goal Type</th>
                            <th>Target Amount</th>
                            <th>Timeline (Years)</th>
                            <th>Priority</th>
                            <th>Suggested SIP (Base Case)</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        for goal in financial_goals:
            sip_base_case = goal.get('sip_scenarios', {}).get('sip_base_case', 'N/A')
            html_content += f"""
                        <tr>
                            <td>{goal.get('goal_type', 'N/A')}</td>
                            <td>{format_currency(goal.get('target_amount'))}</td>
                            <td>{goal.get('timeline_years', 'N/A')}</td>
                            <td>{goal.get('priority_rank', 'N/A')}</td>
                            <td>{format_currency(sip_base_case)}</td>
                        </tr>
            """
        html_content += """
                    </tbody>
                </table>
        """
    else:
        html_content += "<p>No financial goals have been defined yet.</p>"
    html_content += "</div>"

    html_content += f"""
            <div class=\"section summary-box\">
                <h2>4. Savings & Investment Potential</h2>
                <p><strong>Recommended Monthly Savings:</strong> {format_currency(savings_summary.get('final_monthly_savings_amount'))}</p>
                <p><strong>Disposable Monthly Income:</strong> {format_currency(savings_summary.get('disposable_monthly_income'))}</p>
                <p><strong>Savings Rate (of Disposable Income):</strong> {format_percentage(savings_summary.get('final_applicable_savings_rate'))}</p>
                <p><strong>Feasibility Index:</strong> {format_percentage(savings_summary.get('feasibility_index')/100 if savings_summary.get('feasibility_index') is not None else None)}</p>
            </div>
    """
    
    html_content += f"""
            <div class=\"section\">
                <h2>5. Suggested Asset Allocation</h2>
                <p><em>Detailed asset allocation based on your profile and goals:</em></p>
    """
    if asset_allocation_summary:
        html_content += "<table><thead><tr><th>Asset Class</th><th>Allocation</th></tr></thead><tbody>"
        for asset_class, allocation in asset_allocation_summary.items():
            html_content += f"<tr><td>{asset_class}</td><td>{allocation}</td></tr>"
        html_content += "</tbody></table>"
    else:
        html_content += "<p>Asset allocation details will be provided upon plan finalization.</p>"
    html_content += "</div>"

    html_content += f"""
            <div class=\"section\">
                <h2>6. Recommended Action Plan</h2>
    """
    if action_plan:
        html_content += "<ul>"
        for item in action_plan:
            html_content += f"<li>{item}</li>"
        html_content += "</ul>"
    else:
        html_content += "<p>Specific action steps will be outlined upon plan finalization.</p>"
    html_content += "</div>"

    html_content += f"""
            <div class=\"section\">
                <h2>7. Current Economic Outlook & Considerations</h2>
                <p><strong>GDP Growth Rate:</strong> {economic_outlook.get('gdp_growth_rate', 'N/A')}%</p>
                <p><strong>Inflation Rate (CPI):</strong> {economic_outlook.get('inflation_rate_cpi', 'N/A')}%</p>
                <p><strong>Repo Rate:</strong> {economic_outlook.get('repo_rate', 'N/A')}%</p>
                <p><em>Note: Economic conditions can impact investment returns. Regular reviews are advised.</em></p>
            </div>

            <div class=\"footer\">
                <p>Disclaimer: This financial plan is based on the information provided and current market understanding. Investment in securities market are subject to market risks. Read all the related documents carefully before investing. Past performance is not indicative of future results. Consult with your MFD for personalized advice.</p>
                <p>&copy; {datetime.now().year} Your Financial Planning Service</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# --- PDF Generation using WeasyPrint ---
def generate_pdf_report(html_content: str, output_pdf_path: str):
    """Converts HTML string to a PDF file using WeasyPrint."""
    try:
        # Use CSS for font definitions, including CJK fonts
        css_string = """
        @font-face {
            font-family: 'NotoSansCJK';
            src: url('file:///usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc');
        }
        @font-face {
            font-family: 'WenQuanYiZenHei';
            src: url('file:///usr/share/fonts/truetype/wqy/wqy-zenhei.ttc');
        }
        @page {
            size: A4;
            margin: 1.5cm;
        }
        body {
            font-family: 'NotoSansCJK', 'WenQuanYiZenHei', Arial, sans-serif;
        }
        /* Add any other PDF-specific styles here */
        """
        css = CSS(string=css_string) # Removed font_config from CSS call
        HTML(string=html_content).write_pdf(output_pdf_path, stylesheets=[css]) # Removed font_config from write_pdf call
        print(f"PDF report generated successfully at {output_pdf_path}")
        return True
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

if __name__ == "__main__":
    print("--- Test Report Generation Logic ---")

    sample_investor = {
        "name": "Priya Sharma", 
        "dob": "1985-07-15", 
        "occupation": "White-Collar",
        "mobile_number": "9876543210",
        "email": "priya.sharma@example.com"
    }
    sample_profile = {"profile_id": "W8", "description": "Established Professional, Moderate Growth Focus"}
    sample_risk = {"total_score": 65, "risk_rating": "Moderate Growth"}
    sample_goals = [
        {"goal_type": "Child Education", "target_amount": 1500000, "timeline_years": 10, "priority_rank": 1, "sip_scenarios": {"sip_base_case": 8500}},
        {"goal_type": "Retirement", "target_amount": 10000000, "timeline_years": 20, "priority_rank": 2, "sip_scenarios": {"sip_base_case": 15000}}
    ]
    sample_savings = {
        "final_monthly_savings_amount": 25000,
        "disposable_monthly_income": 75000,
        "final_applicable_savings_rate": 0.3333,
        "feasibility_index": 66.67
    }
    sample_asset_alloc = {"Equity (Large Cap)": "40%", "Equity (Mid/Small Cap)": "20%", "Debt (Long Term)": "30%", "Gold": "10%"}
    sample_actions = ["Initiate SIP of ₹8,500 in a diversified equity fund for Child Education.", "Increase retirement SIP to ₹15,000."]
    sample_econ = {"gdp_growth_rate": "6.5", "inflation_rate_cpi": "5.2", "repo_rate": "6.5"}

    html_output = generate_investor_report_html(
        sample_investor, sample_profile, sample_risk, sample_goals, 
        sample_savings, sample_asset_alloc, sample_actions, sample_econ
    )
    
    with open("/home/ubuntu/sample_report.html", "w", encoding="utf-8") as f:
        f.write(html_output)
    print("Sample HTML report saved to /home/ubuntu/sample_report.html")

    pdf_output_path = "/home/ubuntu/Sample_Investor_Guide.pdf"
    success = generate_pdf_report(html_output, pdf_output_path)
    if success:
        print(f"PDF generation successful. Report at: {pdf_output_path}")
    else:
        print(f"PDF generation failed.")

