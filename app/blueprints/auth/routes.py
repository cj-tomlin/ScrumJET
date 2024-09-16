from flask import Blueprint, render_template, redirect, url_for
from .forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Auth logic
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Registration logic
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
