# Master for Automatic HTML Conversion of Guides

## Purpose
This guide defines the process for the app to automatically convert investor guides, such as the "Guide for the Mutual Fund Distributor (MFD)" (artifact_id: ceedbd82-bb30-442d-9335-f83a507abfc0), from Markdown to HTML, applying a clean and organized format. The process ensures consistency in presentation across all investor cases, featuring hierarchical headings, tables, bullet points, visual elements like charts, and uniform styling for enhanced readability and professionalism.

## 1. Overview of the Conversion Process
- **Objective**: Automate the conversion of Markdown-based investor guides into HTML, ensuring a standardized format for all investor cases.
- **Scope**: Applies to all documents tagged as investor guides (e.g., "Guide for the MFD," "Guide for the Investor").
- **Expected Outcome**: HTML documents with consistent styling, including headings, tables, bullet points, charts, and a professional layout.

## 2. Format Specifications
- **Headings**:
  - `h1`: Document title, 28px, centered, color #1F2A44, with a bottom border.
  - `h2`: Main sections, 20px, color #1F2A44.
  - `h3`: Subsections, 16px, color #1F2A44.
- **Tables**:
  - Full-width, with 1px solid borders (color #E5E7EB).
  - Header background: #F9FAFB, text color: #1F2A44.
  - Centered text, 8px padding, 12px font size.
- **Bullet Points**:
  - Use `<ul>` and `<li>` elements.
  - Font size: 14px, with proper indentation.
- **Visual Elements**:
  - Include Chart.js bar charts for sections with scoring or distribution data (e.g., "Assessing Risk Tolerance").
  - Chart colors: Risk-Averse (#EF4444), Moderate (#F59E0B), Aggressive (#16A34A).
- **Styling**:
  - Content wrapper: Max-width 800px, centered.
  - Sections: Background #F9FAFB, 15px padding, 8px border-radius, subtle shadow (0 1px 3px rgba(0,0,0,0.1)).
  - Font: Inter for English, 14px for paragraphs.
  - Text: Color #4A4A4A, justified alignment, line-height 1.6.

## 3. Conversion Steps
### 3.1 Document Detection and Tagging
- Identify investor guides using metadata (e.g., artifact_id) or tags (e.g., "investor_guide").
- Use a configuration file or database to map tagged documents to the HTML conversion process.

### 3.2 Markdown-to-HTML Parsing
- Use a Markdown parser (e.g., `marked` in JavaScript or `python-markdown` in Python) to convert:
  - Headings (`#`, `##`, `###`) to `<h1>`, `<h2>`, `<h3>`.
  - Tables to `<table>` elements with specified styling.
  - Bullet points (`-`) to `<ul>` and `<li>`.
  - Inline formatting (e.g., **bold** to `<strong>`, *italics* to `<em>`).

### 3.3 Applying the HTML Template
- Embed the converted HTML into a predefined template with:
  - `<head>`: Include Chart.js (`https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js`) and Inter font (`https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap`).
  - `<style>`: Define CSS rules for headings, tables, bullet points, sections, and charts.
  - `<body>`: Use a wrapper div (`max-width: 800px`) to hold the content.
  - `<script>`: Add Chart.js scripts for chart rendering.

### 3.4 Dynamic Chart Integration
- Detect sections for charts (e.g., "Assessing Risk Tolerance") using keywords like "scoring" or "distribution".
- Inject a Chart.js bar chart with predefined data:
  - Labels: ["Risk-Averse (0-8)", "Moderate (9-14)", "Aggressive (15-20)"].
  - Data: [60, 30, 10] (hypothetical percentages).
  - Options: Responsive, with tooltips showing percentages, and labeled axes ("Risk Profile", "Percentage of Investors (%)").

### 3.5 Output Generation
- Combine the converted HTML with the template.
- Save the output as an HTML file (e.g., "Guide for the MFD.html").
- Ensure the output is accessible via the app’s UI or downloadable.

## 4. Ensuring Consistency Across Investor Cases
- **Tagging**: Tag all investor guides with "investor_guide" to trigger the conversion process.
- **Centralized Template**: Store the HTML template in a single location (e.g., app assets or database).
- **Dynamic Adjustments**: Add charts conditionally based on section content.

## 5. Example Pseudo-Code for Implementation
Below is a pseudo-code example for the app to execute the conversion process:
```
# Step 1: Identify the document
document = getDocumentById("ceedbd82-bb30-442d-9335-f83a507abfc0")
if "investor_guide" in document.tags:
    # Step 2: Convert Markdown to HTML
    html_content = markdownToHtml(document.content)

    # Step 3: Load the HTML template
    template = loadHtmlTemplate("investor_guide_template.html")

    # Step 4: Inject content and charts
    final_html = template
        .replace("{{CONTENT}}", html_content)
        .replace("{{CHART_SCRIPT}}", generateChartScript("riskChart", getRiskData()))

    # Step 5: Output the formatted HTML
    saveOutput(final_html, "Guide for the MFD.html")
```

## Conclusion
This guide ensures the app can automatically convert investor guides into HTML with a consistent, professional format, enhancing readability and user experience. By following these steps, the app maintains uniformity across all investor cases, streamlining the presentation of critical financial planning documents.