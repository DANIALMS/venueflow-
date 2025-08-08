from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from .models import Event

calendar_bp = Blueprint('calendar', __name__, template_folder='templates')

@calendar_bp.route('/calendar')
@login_required
def calendar_view():
    return render_template('calendar.html')

@calendar_bp.route('/api/events')
@login_required
def events_feed():
    # FullCalendar expects ISO date fields: start, end, title, id
    events = Event.query.all()
    feed = []
    for e in events:
        feed.append({
            "id": e.id,
            "title": f"{e.name} ({e.venue_space})",
            "start": f"{e.event_date}T{e.start_time or '00:00'}",
            "end": f"{e.event_date}T{e.end_time or '23:59'}",
            "extendedProps": {"status": e.status, "contract": e.contract_status}
        })
    return jsonify(feed)
