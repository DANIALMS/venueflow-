from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash
from flask_login import login_required
from io import BytesIO
from xhtml2pdf import pisa
from .models import Event, Invoice, LineItem
from .app import db

beo_bp = Blueprint('beo', __name__, template_folder='templates')

@beo_bp.route('/beo/<int:event_id>')
@login_required
def beo_view(event_id):
    e = Event.query.get_or_404(event_id)
    inv = Invoice.query.filter_by(event_id=e.id).first()
    items = LineItem.query.filter_by(invoice_id=inv.id).all() if inv else []
    # Defaults for blanks
    context = {"event": e, "invoice": inv, "items": items}
    return render_template('beo/view.html', **context)

@beo_bp.route('/beo/<int:event_id>/calc', methods=['POST'])
@login_required
def beo_calc(event_id):
    # Accepts AJAX post to compute totals; returns JSON (front-end already handles math; keep endpoint for future server calc)
    return {"ok": True}

@beo_bp.route('/beo/<int:event_id>/pdf')
@login_required
def beo_pdf(event_id):
    e = Event.query.get_or_404(event_id)
    inv = Invoice.query.filter_by(event_id=e.id).first()
    items = LineItem.query.filter_by(invoice_id=inv.id).all() if inv else []
    html = render_template('beo/pdf.html', event=e, invoice=inv, items=items)
    pdf_io = BytesIO()
    pisa.CreatePDF(src=html, dest=pdf_io)
    pdf_io.seek(0)
    filename = f"BEO_{e.event_code or e.id}.pdf"
    return send_file(pdf_io, mimetype='application/pdf', as_attachment=True, download_name=filename)
