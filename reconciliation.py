import csv

# Read invoices
with open("invoices.csv", "r") as file:
    invoices = list(csv.DictReader(file))

# Read transactions
with open("transactions.csv", "r") as file:
    transactions = list(csv.DictReader(file))


# Counters
matched_count = 0
possible_count = 0
review_count = 0

print("=" * 50)
print("        ReconAI Financial Reconciliation")
print("=" * 50)

# Check every invoice
for invoice in invoices:

    invoice_customer = invoice["customer"]
    invoice_amount = float(invoice["amount"])

    best_match = None
    smallest_difference = float("inf")

    # Compare with every transaction
    for transaction in transactions:

        transaction_customer = transaction["customer"]
        transaction_amount = float(transaction["amount"])

        # Compare customers
        if invoice_customer.lower() == transaction_customer.lower():

            difference = abs(invoice_amount - transaction_amount)

            if difference < smallest_difference:
                smallest_difference = difference
                best_match = transaction

    # Decide the result
    if best_match is None:

        review_count += 1

        print(
            invoice["invoice_id"],
            "→ NO PAYMENT FOUND ❌"
        )

    elif smallest_difference == 0:

        matched_count += 1

        print(
            invoice["invoice_id"],
            "→",
            best_match["transaction_id"],
            "→ MATCHED ✅"
        )

    elif smallest_difference <= 100:

        possible_count += 1

        print(
            invoice["invoice_id"],
            "→",
            best_match["transaction_id"],
            "→ POSSIBLE MATCH ⚠️",
            "| Difference: ₹",
            smallest_difference
        )

    else:

        review_count += 1

        print(
            invoice["invoice_id"],
            "→",
            best_match["transaction_id"],
            "→ REVIEW ❌",
            "| Difference: ₹",
            smallest_difference
        )


# Final summary
print()
print("=" * 50)
print("                SUMMARY")
print("=" * 50)

print("Total invoices:", len(invoices))
print("Matched:", matched_count)
print("Possible matches:", possible_count)
print("Needs review:", review_count)