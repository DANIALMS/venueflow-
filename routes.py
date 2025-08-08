from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from .app import db
from .models import Lead, Event, Task, Invoice, LineItem
from .forms import LeadForm, EventForm, TaskForm, InvoiceForm, LineItemForm
import math

main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
@login_required
def dashboard():
    stages = ['New','Qualified','Toured','Proposal','Contract Sent','Booked','Won','Lost']
    columns = {s: Lead.query.filter_by(stage=s).order_by(Lead.created_at.desc()).all() for s in stages}
    open_tasks = Task.query.filter_by(status='Open').order_by(Task.due_date.asc()).limit(10).all()
    upcoming_events = Event.query.order_by(Event.event_date.asc()).limit(10).all()
    return render_template('dashboard.html', columns=columns, open_tasks=open_tasks, upcoming_events=upcoming_events, stages=stages)

# Leads
@main_bp.route('/leads')
@login_required
def leads():
    q = request.args.get('q','')
    query = Lead.query
    if q:
        like = f"%{q}%"
        query = query.filter( (Lead.first_name.ilike(like)) | (Lead.last_name.ilike(like)) | (Lead.email.ilike(like)) )
    leads = query.order_by(Lead.created_at.desc()).all()
    return render_template('leads/list.html', leads=leads, q=q)

@main_bp.route('/leads/new', methods=['GET','POST'])
@login_required
def lead_new():
    form = LeadForm()
    if form.validate_on_submit():
        lead = Lead(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data,
                    source=form.source.data, event_type=form.event_type.data, event_date=form.event_date.data,
                    guest_count=form.guest_count.data, budget_min=form.budget_min.data, budget_max=form.budget_max.data,
                    stage=form.stage.data, next_action=form.next_action.data, next_action_due=form.next_action_due.data, notes=form.notes.data)
        db.session.add(lead); db.session.commit()
        lead.lead_code = f"L-{lead.id:04d}"; db.session.commit()
        flash('Lead created','success')
        return redirect(url_for('main.leads'))
    return render_template('leads/form.html', form=form, title='New Lead')

@main_bp.route('/leads/<int:lead_id>', methods=['GET','POST'])
@login_required
def lead_detail(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    form = LeadForm(obj=lead)
    if form.validate_on_submit():
        form.populate_obj(lead)
        db.session.commit()
        flash('Lead updated','success')
        return redirect(url_for('main.lead_detail', lead_id=lead.id))
    events = Event.query.filter_by(lead_id=lead.id).all()
    return render_template('leads/detail.html', form=form, lead=lead, events=events)

# Events
@main_bp.route('/events')
@login_required
def events():
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template('events/list.html', events=events)

@main_bp.route('/events/new', methods=['GET','POST'])
@login_required
def event_new():
    form = EventForm()
    if form.validate_on_submit():
        e = Event(name=form.name.data, event_type=form.event_type.data, venue_space=form.venue_space.data,
                  event_date=form.event_date.data, start_time=form.start_time.data, end_time=form.end_time.data,
                  guest_count=form.guest_count.data, package=form.package.data, food_service=form.food_service.data,
                  bar_service=form.bar_service.data, status=form.status.data, contract_status=form.contract_status.data,
                  assigned_manager=form.assigned_manager.data)
        db.session.add(e); db.session.commit()
        e.event_code = f"E-{e.id:04d}"; db.session.commit()
        flash('Event created','success')
        return redirect(url_for('main.events'))
    return render_template('events/form.html', form=form, title='New Event')

@main_bp.route('/events/<int:event_id>', methods=['GET','POST'])
@login_required
def event_detail(event_id):
    e = Event.query.get_or_404(event_id)
    form = EventForm(obj=e)
    inv = Invoice.query.filter_by(event_id=e.id).first()
    items = []
    if inv:
        items = LineItem.query.filter_by(invoice_id=inv.id).all()
    if form.validate_on_submit():
        form.populate_obj(e); db.session.commit(); flash('Event updated','success')
        return redirect(url_for('main.event_detail', event_id=e.id))
    return render_template('events/detail.html', form=form, event=e, invoice=inv, items=items)

# Tasks
@main_bp.route('/tasks', methods=['GET','POST'])
@login_required
def tasks():
    form = TaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, owner=form.owner.data, due_date=form.due_date.data, status=form.status.data, priority=form.priority.data)
        db.session.add(t); db.session.commit()
        flash('Task added','success')
        return redirect(url_for('main.tasks'))
    tasks = Task.query.order_by(Task.due_date.asc()).all()
    return render_template('tasks/list.html', form=form, tasks=tasks)

# Invoices
@main_bp.route('/events/<int:event_id>/invoice/new', methods=['GET','POST'])
@login_required
def invoice_new(event_id):
    e = Event.query.get_or_404(event_id)
    form = InvoiceForm()
    if form.validate_on_submit():
        inv = Invoice(event_id=e.id, issue_date=form.issue_date.data, due_date=form.due_date.data,
                      tax_percent=form.tax_percent.data or 0, service_fee_percent=form.service_fee_percent.data or 0,
                      gratuity_percent=form.gratuity_percent.data or 0)
        db.session.add(inv); db.session.commit()
        inv.invoice_code = f"INV-{inv.id:04d}"; db.session.commit()
        flash('Invoice created','success')
        return redirect(url_for('main.event_detail', event_id=e.id))
    return render_template('invoices/form.html', form=form, event=e)

@main_bp.route('/invoice/<int:inv_id>/item', methods=['POST'])
@login_required
def invoice_add_item(inv_id):
    inv = Invoice.query.get_or_404(inv_id)
    form = LineItemForm()
    if form.validate_on_submit():
        li = LineItem(invoice_id=inv.id, item=form.item.data, qty=form.qty.data or 1, unit_price=form.unit_price.data or 0)
        li.total = (li.qty or 1) * (li.unit_price or 0)
        inv.subtotal = sum([x.total for x in inv.items]) + li.total
        inv.total = inv.subtotal * (1 + (inv.tax_percent or 0)/100 + (inv.service_fee_percent or 0)/100 + (inv.gratuity_percent or 0)/100)
        inv.balance_due = (inv.total or 0) - (inv.amount_paid or 0)
        from .app import db
        db.session.add(li); db.session.commit()
        flash('Line item added','success')
    return redirect(url_for('main.event_detail', event_id=inv.event_id))
