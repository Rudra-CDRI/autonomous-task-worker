import company_system
import json
import os

# Ensure we start with a clean slate for the test
company_system.reset_records()

def print_result(desc, result):
    print(f"--- {desc} ---")
    print(json.dumps(result, indent=2))
    print()

print("Testing Fake Company System by Hand\n")

# 1. Good call
res1 = company_system.create_invoice("Acme Corp", 1500.50, "2026-11-05")
print_result("Good Call", res1)

# 2. Bad date
res2 = company_system.create_invoice("Beta Services", 200.00, "11/05/2026")
print_result("Bad Date", res2)

# 3. Unapproved vendor
res3 = company_system.create_invoice("Acme Corporation Ltd", 500.00, "2026-12-01")
print_result("Unapproved Vendor", res3)

# 4. Duplicate
res4 = company_system.create_invoice("Acme Corp", 1500.50, "2026-11-05")
print_result("Duplicate", res4)

# 5. List records
records = company_system.list_invoices()
print_result("All Invoices in System", records)
