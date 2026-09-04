import os
import json
from google import genai


def analyze_case(invoice, payment):

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return {
            "decision": "review",
            "confidence": 0,
            "reason": "Gemini API key is not configured."
        }

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are a financial reconciliation assistant.

Analyze whether this payment likely belongs to this invoice.

INVOICE:
Invoice ID: {invoice["invoice_id"]}
Customer: {invoice["customer"]}
Amount: ₹{invoice["amount"]}

PAYMENT:
Transaction ID: {payment["transaction_id"]}
Customer: {payment["customer"]}
Amount: ₹{payment["amount"]}

Determine whether this is likely a valid match.

Return ONLY valid JSON:

{{
    "decision": "likely_match" or "review",
    "confidence": 0,
    "reason": "short explanation"
}}

Be conservative. If there is insufficient evidence, choose "review".
"""

        response = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        text = response.output_text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        result = json.loads(text)

        return {
            "decision": result.get("decision", "review"),
            "confidence": result.get("confidence", 0),
            "reason": result.get("reason", "")
        }

    except Exception as e:
        return {
            "decision": "review",
            "confidence": 0,
            "reason": f"AI error: {str(e)}"
        }