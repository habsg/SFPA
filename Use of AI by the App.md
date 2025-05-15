# Use of AI by the App

## Purpose

This document outlines the integration of the Hugging Face free API into the financial planning app to enhance its analytical capabilities and report generation. The AI will operate within the parameters of existing master documents (e.g., Risk Assessment, Financial Goals, Year-Wise Investment Objectives) to provide deeper analysis, personalized insights, and narrative reports for Mutual Fund Distributors (MFDs) and investors.

## Role of AI in the App

- **Deeper Analysis**:
  - Analyze investor data (e.g., income, dependents, loans) to identify nuanced risks or opportunities not explicitly coded in the app’s rules.
  - Example: Highlighting that a Blue-Collar investor’s high Loan-to-Income Ratio and unstable income increase the risk of financial stress, suggesting a focus on debt reduction.
- **Personalized Insights**:
  - Generate tailored recommendations for each investor, such as fund allocations, risk mitigation strategies, or future financial risks.
  - Example: Suggesting a conservative fund allocation for a Risk-Averse investor while noting potential healthcare costs in 20 years.
- **Narrative Reports**:
  - Enhance reports (e.g., Guide for the MFD, Year-Wise Investment Objectives) with narrative summaries, risk warnings, and actionable advice.
  - Example: Adding an “AI Insights” section to the Guide for the MFD: “This investor’s high debt and limited savings suggest prioritizing debt reduction over aggressive equity investments.”
- **External Context**:
  - Consider external factors (e.g., market trends, inflation forecasts) to improve projections and recommendations, where applicable.

## Scope of AI Integration

- **Reports to Enhance**:
  - Guide for the MFD (artifact_id: ceedbd82-bb30-442d-9335-f83a507abfc0)
  - Year-Wise Investment Objectives (artifact_id: 762c4d72-5c98-4adf-8f77-f045f6533d7b)
  - Financial Goals by Investor Life Cycle Stages (artifact_id: c4f92cd3-14c7-4450-998c-9430ff158bad)
  - Risk Assessment of Investors by Occupation (artifact_id: 96c2e445-0520-483e-b78b-24801b859fa6)
- **Constraints**:
  - AI outputs must align with the app’s predefined frameworks:
    - Risk profiles must match the scoring system (0–20 scale: 0–8 Risk-Averse, 9–14 Moderate, 15–20 Aggressive).
    - Fund allocations must follow time horizon rules (e.g., no Small Cap Funds for goals &lt;10 years).
    - Goal timelines must adhere to Financial Goals definitions (e.g., Blue-Collar home purchase: 10–15 years, 12–18 if high-debt).
  - AI insights are supplementary and must be cross-checked with app logic to ensure consistency.

## Technical Implementation

- **API Selection**:
  - **Hugging Face Free API**: Chosen for its free tier, open-source models, and flexibility for text generation and analysis.
  - **Model**: Use a text generation model like `gpt2` or a fine-tuned financial model (if available on Hugging Face Hub) for narrative insights.
- **Integration Steps**:
  1. **Authentication**:
     - Sign up on Hugging Face Hub, generate an API token, and store it securely in the app’s backend (e.g., as an environment variable).
  2. **API Endpoint**:
     - Use the inference endpoint: `https://api-inference.huggingface.co/models/{model_name}` (e.g., `gpt2`).
  3. **Input Data**:
     - Extract data from the Investor Profile Form (artifact_id: 91228f9a-35a0-4524-a828-0272c1c8b96c), such as:
       - Age, Occupation, Monthly Income, Number of Dependents, Ages, and Gender of Dependents, Home Ownership, Existing Loans, Monthly Loan Repayment.
       - Risk questionnaire answers (e.g., Reaction to 10% Loss, Investment Preference, Financial Cushion).
     - Pull relevant data from other master documents (e.g., Financial Goals timelines, Risk Assessment scores).
  4. **Prompt Design**:
     - Use prompts defined in the “Master Prompt for the App for Each Individual Report” (artifact_id: b2e5f8c0-5d3f-4b7e-a1c4-3f9d2e7c6a0b) to guide the AI.
     - Example Prompt: “Given a 32-year-old Blue-Collar investor with ₹25,000 monthly income, 2 dependents, and a 20% Loan-to-Income Ratio, suggest additional risks to highlight in the Guide for the MFD.”
  5. **Process Output**:
     - Parse the AI’s response (e.g., JSON format) to extract insights.
     - Cross-check with app logic (e.g., ensure AI-suggested risk profile matches the app’s score).
     - Integrate into reports as an “AI Insights” section or narrative summary.
- **Example Code**:

  ```javascript
  const axios = require('axios');
  const API_TOKEN = process.env.HUGGINGFACE_API_TOKEN;
  const API_URL = 'https://api-inference.huggingface.co/models/gpt2';
  
  async function generateAIInsight(prompt) {
    try {
      const response = await axios.post(API_URL, { inputs: prompt, parameters: { max_length: 200 } }, {
        headers: { Authorization: `Bearer ${API_TOKEN}` }
      });
      return response.data[0].generated_text;
    } catch (error) {
      console.error('Error calling Hugging Face API:', error);
      return 'Unable to generate AI insight.';
    }
  }
  
  const investorData = {
    age: 32,
    occupation: 'Blue-Collar',
    income: 25000,
    dependents: 2,
    loanToIncomeRatio: 0.2
  };
  const prompt = `Given a ${investorData.age}-year-old ${investorData.occupation} investor with ₹${investorData.income} monthly income, ${investorData.dependents} dependents, and a ${investorData.loanToIncomeRatio * 100}% Loan-to-Income Ratio, suggest additional risks to highlight in the Guide for the MFD.`;
  generateAIInsight(prompt).then(insight => console.log('AI Insight:', insight));
  ```

## Guidelines for AI Use

- **Consistency**:
  - AI outputs must align with master document frameworks (e.g., Risk Assessment scores, Financial Goals timelines).
  - Example: If the AI suggests a Moderate risk profile but the app scores the investor as Risk-Averse (score: 5), override the AI suggestion with the app’s score.
- **Explainability**:
  - AI insights must be interpretable for MFDs (e.g., “The AI suggests focusing on debt reduction due to the investor’s high Loan-to-Income Ratio and limited savings.”).
  - Avoid overly technical or vague outputs (e.g., “Optimize portfolio with a 60/40 split” without context).
- **Data Privacy**:
  - Anonymize investor data before sending to the API (e.g., remove names, use IDs).
  - Use secure API calls (HTTPS) and comply with regulations (e.g., GDPR).
- **Error Handling**:
  - If the API fails (e.g., rate limits, downtime), fallback to the app’s default logic without AI insights.
  - Log errors for debugging (e.g., “Hugging Face API rate limit exceeded”).

## Conclusion

The Hugging Face API integration enhances the app’s ability to generate deeper, personalized reports while adhering to the frameworks defined in the master documents. By providing narrative insights, risk analysis, and tailored recommendations, the AI ensures that MFDs and investors receive more actionable and context-aware financial plans.