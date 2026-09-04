import csv

with open("invoices.csv", "r") as file:
    invoices = list(csv.DictReader(file))

with open("transactions.csv", "r") as file:
    transactions = list(csv.DictReader(file))

print("INVOICES:")
for invoice in invoices:
    print(invoice)

print("\nTRANSACTIONS:")
for transaction in transactions:
    print(transaction)
