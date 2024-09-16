from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_migrate import current

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return render_template('admin/dashboard.html')
    return "Unauthorized", 403
