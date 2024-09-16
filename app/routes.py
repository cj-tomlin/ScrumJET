from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template('index.html', title='ScrumJET')


@main_bp.route('/about')
def about():
    return render_template('about.html', title='About')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


@main_bp.route('/faq')
def faq():
    return render_template('faq.html', title='FAQ')
