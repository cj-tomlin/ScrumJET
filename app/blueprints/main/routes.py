from flask import Blueprint, render_template
from datetime import datetime
from app.models import Announcement, Course, Article, Event

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(3).all()
    featured_courses = Course.query.order_by(Course.created_at.desc()).limit(3).all()
    latest_articles = Article.query.filter_by(published=True).order_by(Article.created_at.desc()).limit(3).all()
    upcoming_events = Event.query.filter(Event.start_date >= datetime.utcnow()).order_by(Event.start_date).limit(3).all()
    
    return render_template('index.html', 
                          title='ScrumJET',
                          announcements=announcements,
                          featured_courses=featured_courses,
                          latest_articles=latest_articles,
                          upcoming_events=upcoming_events)

@main_bp.route('/about')
def about():
    return render_template('about.html', title='About')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')

@main_bp.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')
