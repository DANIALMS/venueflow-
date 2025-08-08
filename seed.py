from werkzeug.security import generate_password_hash
from .app import db
from .models import User, Lead, Event, Invoice, LineItem, Task

def run_seed():
    db.drop_all(); db.create_all()
    admin = User(email="admin@example.com", password_hash=generate_password_hash("changeme"), name="Admin", role="ADMIN")
    db.session.add(admin); db.session.commit()

    lead = Lead(first_name="Alex", last_name="Rivera", email="alex@example.com", phone="303-555-1200",
                source="Website", event_type="Wedding", event_date="2026-06-20", guest_count=150,
                budget_min=15000, budget_max=25000, stage="Qualified", next_action="Call to qualify", next_action_due="2025-08-09")
    db.session.add(lead); db.session.commit()
    lead.lead_code = f"L-{lead.id:04d}"

    event = Event(name="Rivera Wedding", event_type="Wedding", venue_space="Grand Hall", event_date="2026-06-20",
                  start_time="16:00", end_time="23:00", guest_count=150, package="Gold Wedding",
                  food_service="TPC In-house", bar_service="In-house", status="Tentative", contract_status="Draft",
                  assigned_manager="Saqib", lead=lead)
    db.session.add(event); db.session.commit()
    event.event_code = f"E-{event.id:04d}"

    inv = Invoice(event_id=event.id, issue_date="2025-08-08", due_date="2025-08-22", tax_percent=8.0)
    db.session.add(inv); db.session.commit()
    inv.invoice_code = f"INV-{inv.id:04d}"
    item = LineItem(invoice_id=inv.id, item="Gold Wedding Package", qty=1, unit_price=18000, total=18000)
    db.session.add(item); db.session.commit()
    inv.subtotal = 18000; inv.total = 18000*1.08; inv.balance_due = inv.total; db.session.commit()

    task = Task(title="Call lead to qualify", owner="Saqib", due_date="2025-08-09", status="Open", priority="High")
    db.session.add(task); db.session.commit()
