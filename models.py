from datetime import datetime
from flask_login import UserMixin
from .app import db, login_manager

roles = ('ADMIN', 'SALES', 'OPS')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(120))
    role = db.Column(db.String(20), default='SALES')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lead_code = db.Column(db.String(20), unique=True)
    source = db.Column(db.String(120))
    event_type = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    event_date = db.Column(db.String(20))
    guest_count = db.Column(db.Integer)
    budget_min = db.Column(db.Integer)
    budget_max = db.Column(db.Integer)
    stage = db.Column(db.String(40), default='New')
    probability = db.Column(db.Integer, default=10)
    owner = db.Column(db.String(120))
    notes = db.Column(db.Text)
    next_action = db.Column(db.String(200))
    next_action_due = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    events = db.relationship('Event', backref='lead', lazy=True)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_code = db.Column(db.String(20), unique=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('lead.id'), nullable=True)
    status = db.Column(db.String(40), default='Tentative')
    name = db.Column(db.String(200))
    event_type = db.Column(db.String(80))
    venue_space = db.Column(db.String(120))
    event_date = db.Column(db.String(20))
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    guest_count = db.Column(db.Integer)
    package = db.Column(db.String(120))
    food_service = db.Column(db.String(120))
    bar_service = db.Column(db.String(120))
    contract_status = db.Column(db.String(40), default='Draft')
    assigned_manager = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    invoices = db.relationship('Invoice', backref='event', lazy=True)
    tasks = db.relationship('Task', backref='event', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    related_type = db.Column(db.String(20))  # Lead or Event
    related_id = db.Column(db.Integer)
    title = db.Column(db.String(200))
    owner = db.Column(db.String(120))
    due_date = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Open')
    priority = db.Column(db.String(20), default='Medium')
    notes = db.Column(db.Text)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_code = db.Column(db.String(20), unique=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    issue_date = db.Column(db.String(20))
    due_date = db.Column(db.String(20))
    subtotal = db.Column(db.Float, default=0)
    tax_percent = db.Column(db.Float, default=0)
    service_fee_percent = db.Column(db.Float, default=0)
    gratuity_percent = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    amount_paid = db.Column(db.Float, default=0)
    balance_due = db.Column(db.Float, default=0)
    payment_schedule = db.Column(db.String(255))
    stripe_payment_link = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('LineItem', backref='invoice', lazy=True)

class LineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))
    item = db.Column(db.String(200))
    qty = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_code = db.Column(db.String(20), unique=True)
    type = db.Column(db.String(20))  # Client or Vendor
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    company = db.Column(db.String(120))
    role = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(50))
    zip = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
