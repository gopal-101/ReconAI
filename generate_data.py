import csv
import random

customers = [
    "Rahul", "Priya", "Amit", "Neha", "Arjun",
    "Simran", "Rohan", "Ananya", "Karan", "Isha",
    "Vikram", "Meera", "Aditya", "Pooja", "Nikhil",
    "Sneha", "Varun", "Kavya", "Manish", "Riya"
]

invoices = []
transactions = []

for i in range(1, 101):

    customer = random.choice(customers)
    amount = random.choice([
        1000, 1500, 2000, 2500, 3000,
        5000, 7500, 10000, 15000, 20000
    ])

    invoice_id = f"INV{i:03d}"
    transaction_id = f"PAY{i:03d}"

    invoices.append({
        "invoice_id": invoice_id,
        "customer": customer,
        "amount": amount
    })

    # Most payments match exactly
    if i % 10 != 0:
        payment_amount = amount

    # Some have small differences
    else:
        payment_amount = amount - random.choice([50, 100, 150])

    transactions.append({
        "transaction_id": transaction_id,
        "customer": customer,
        "amount": payment_amount
    })


with open("invoices.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["invoice_id", "customer", "amount"]
    )
    writer.writeheader()
    writer.writerows(invoices)


with open("transactions.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["transaction_id", "customer", "amount"]
    )
    writer.writeheader()
    writer.writerows(transactions)


print("Created 100 invoices and 100 transactions.")