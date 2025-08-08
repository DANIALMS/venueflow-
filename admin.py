from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/')
@login_required
def index():
    if current_user.role != 'ADMIN':
        return render_template('403.html'), 403
    return render_template('admin.html')
