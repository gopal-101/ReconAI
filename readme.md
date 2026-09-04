    ReconAI

ReconAI is a small project I made to help with invoice and payment reconciliation.

The idea is simple: upload an invoices CSV and a transactions CSV, and the application checks which payments match which invoices.

For exact matches, it matches them automatically. If there is a small difference in the amount, Gemini is used to look at the case and suggest whether it is likely a match or should be reviewed.

Features
Upload invoices and transactions using CSV files
Find exact matches
Check small payment differences using Gemini
Show cases that need manual review
View the reconciliation results
Download the results as a CSV file

How it works
Upload the invoice and transaction files.
The application compares customers and payment amounts.
Exact matches are marked as matched.
Small differences are sent to Gemini for analysis.
Uncertain cases are kept for review.
The results can be downloaded as a CSV file.

Test Result
I tested the application with 100 records.
Exact matches: 94
AI matches: 1
Needs review: 5

Technologies
Python
Streamlit
Pandas
Google Gemini API

Files-
app.py — main Streamlit application
ai_agent.py — Gemini analysis for ambiguous cases
generate_data.py — generates sample invoice and transaction data
read_data.py — reads and processes the data
reconciliation.py — handles the reconciliation and matching logic
invoices.csv — sample invoice data
transactions.csv — sample transaction data
.gitignore — files that should not be uploaded to GitHub
requirements.txt — Python packages needed for the project

Running the project
Install the required packages:
pip install streamlit pandas google-genai
Set the GEMINI_API_KEY environment variable with your Gemini API key.
Then run:
streamlit run app.py
The application will open in the browser.

Note
The API key is kept outside the code using an environment variable and is not included in this repository.