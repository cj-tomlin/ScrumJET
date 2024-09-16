from flask import Blueprint, render_template, redirect, url_for
from app.models import Event

events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def list_events():
    events = Event.query.all()
    return render_template('events/event_list.html', events=events)


@events_bp.route('/events/<int:id>')
def event_detail(id):
    event = Event.query.get_or_404(id)
    return render_template('events/event_detail.html', event=events)
