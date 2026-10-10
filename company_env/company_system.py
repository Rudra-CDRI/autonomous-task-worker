import json
import os
import random
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDS_FILE = os.path.join(BASE_DIR, "records.json")
APPROVED_VENDORS = ["Acme Corp", "Beta Services", "Gamma Tech", "Delta Systems"]
FLAKY_MODE = False

def reset_records():
    if os.path.exists(RECORDS_FILE):
        os.remove(RECORDS_FILE)

def _load_records():
    if not os.path.exists(RECORDS_FILE):
        return []
    try:
        with open(RECORDS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def _save_records(records):
    with open(RECORDS_FILE, "w") as f:
        json.dump(records, f, indent=4)

def _generate_id():
    records = _load_records()
    if not records:
        return 1
    return max(r.get("id", 0) for r in records) + 1

def _validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def create_invoice(vendor, amount, due_date):
    if FLAKY_MODE and random.randint(1, 4) == 1:
        return {"error": "temporary error, try again"}
        
    try:
        amount = float(amount)
        if amount <= 0:
            return {"error": "Amount must be a positive number"}
    except ValueError:
        return {"error": "Amount must be a valid number"}

    if not _validate_date(due_date):
        return {"error": "due_date must be YYYY-MM-DD"}

    if vendor not in APPROVED_VENDORS:
        valid_list = ", ".join(APPROVED_VENDORS)
        return {"error": f"Vendor not approved. Valid vendors are: {valid_list}"}

    records = _load_records()
    
    # Duplicate check
    for r in records:
        if r.get("type") == "invoice" and r.get("vendor") == vendor and r.get("amount") == amount and r.get("due_date") == due_date:
            return {"error": "duplicate record"}
            
    new_record = {
        "id": _generate_id(),
        "type": "invoice",
        "vendor": vendor,
        "amount": amount,
        "due_date": due_date,
        "status": "pending"
    }
    
    records.append(new_record)
    _save_records(records)
    return {"success": True, "record": new_record}

def get_invoice(invoice_id):
    records = _load_records()
    for r in records:
        if r.get("type") == "invoice" and r.get("id") == invoice_id:
            return r
    return {"error": "Invoice not found"}

def list_invoices():
    records = _load_records()
    return [r for r in records if r.get("type") == "invoice"]

def create_expense(employee, amount, category, date):
    if FLAKY_MODE and random.randint(1, 4) == 1:
        return {"error": "temporary error, try again"}
        
    try:
        amount = float(amount)
        if amount <= 0:
            return {"error": "Amount must be a positive number"}
    except ValueError:
        return {"error": "Amount must be a valid number"}

    if not _validate_date(date):
        return {"error": "date must be YYYY-MM-DD"}

    records = _load_records()
    
    for r in records:
        if r.get("type") == "expense" and r.get("employee") == employee and r.get("amount") == amount and r.get("date") == date:
            return {"error": "duplicate record"}
            
    new_record = {
        "id": _generate_id(),
        "type": "expense",
        "employee": employee,
        "amount": amount,
        "category": category,
        "date": date,
        "status": "pending"
    }
    
    records.append(new_record)
    _save_records(records)
    return {"success": True, "record": new_record}
